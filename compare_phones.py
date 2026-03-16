#!/usr/bin/env python3
"""
Mobile Deals Comparison Tool
Compares brand-new, unlocked smartphones above £300 from Samsung, Apple, OnePlus
and Google Pixel – filtered for good specs and ranked by value for money.

Usage:
    python3 compare_phones.py                   # full comparison table + best buys
    python3 compare_phones.py --min-price 500   # override minimum price
    python3 compare_phones.py --brand Samsung   # filter by brand
    python3 compare_phones.py --sort price      # sort by: price | rating | saving
"""

import argparse
import sys
from phones_data import PHONES

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None

PRICE_TIERS = [
    (300, 500, "Budget Flagship (£300–£500)"),
    (500, 750, "Mid Flagship (£500–£750)"),
    (750, 1000, "Premium Flagship (£750–£1,000)"),
    (1000, 9999, "Ultra Premium (£1,000+)"),
]

BEST_BUY_CATEGORIES = [
    ("best_value",       "🏆 Best Overall Value"),
    ("best_camera",      "📸 Best Camera"),
    ("best_battery",     "🔋 Best Battery Life"),
    ("best_ai",          "🤖 Best AI / Software"),
    ("best_compact",     "📱 Best Compact"),
    ("best_budget",      "💰 Best Under £500"),
    ("highest_rated",    "⭐ Highest Rated"),
]


def filter_phones(phones, min_price=300, brand=None):
    """Return phones matching the criteria."""
    results = [
        p for p in phones
        if p["price_gbp"] >= min_price
        and p["unlocked"]
        and p["condition"] == "Brand New"
    ]
    if brand:
        results = [p for p in results if p["brand"].lower() == brand.lower()]
    return results


def saving(phone):
    return phone["original_price_gbp"] - phone["price_gbp"]


def value_score(phone):
    """Higher rating / lower price = better value.  Normalised to 0–100."""
    return round((phone["rating_out_of_10"] / phone["price_gbp"]) * 1000, 3)


def pick_best_buys(phones):
    """Select standout phones per category."""
    picks = {}

    # Best overall value: highest value_score
    picks["best_value"] = max(phones, key=value_score)

    # Best camera: highest main_camera_mp but also factor rating
    picks["best_camera"] = max(
        phones,
        key=lambda p: (p["main_camera_mp"] * 0.4 + p["rating_out_of_10"] * 60),
    )

    # Best battery: highest battery mAh
    picks["best_battery"] = max(phones, key=lambda p: p["battery_mah"])

    # Best AI / software: Google Pixel > Apple > Samsung > OnePlus priority
    ai_priority = {"Google": 4, "Apple": 3, "Samsung": 2, "OnePlus": 1}
    picks["best_ai"] = max(
        phones,
        key=lambda p: (ai_priority.get(p["brand"], 0), p["rating_out_of_10"]),
    )

    # Best compact: smallest display with rating >= 8
    compact_candidates = [p for p in phones if p["rating_out_of_10"] >= 8.0]
    if compact_candidates:
        picks["best_compact"] = min(
            compact_candidates,
            key=lambda p: float(p["display"].split('"')[0]),
        )

    # Best under £500
    budget = [p for p in phones if p["price_gbp"] <= 500]
    if budget:
        picks["best_budget"] = max(budget, key=lambda p: p["rating_out_of_10"])

    # Highest rated
    picks["highest_rated"] = max(phones, key=lambda p: p["rating_out_of_10"])

    return picks


# ─────────────────────────── Rich (coloured) output ──────────────────────────

def print_rich(phones, sort_by="price"):
    if sort_by == "price":
        phones = sorted(phones, key=lambda p: p["price_gbp"])
    elif sort_by == "rating":
        phones = sorted(phones, key=lambda p: p["rating_out_of_10"], reverse=True)
    elif sort_by == "saving":
        phones = sorted(phones, key=saving, reverse=True)

    console.print(
        Panel.fit(
            "[bold cyan]📱 UK Smartphone Deals – Brand New, Unlocked, Above £300[/bold cyan]\n"
            "[dim]Samsung · Apple · OnePlus · Google Pixel  |  March 2026[/dim]",
            border_style="cyan",
        )
    )

    # ── Full Comparison Table ────────────────────────────────────────────────
    tbl = Table(
        title="[bold]Full Price & Spec Comparison[/bold]",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold magenta",
    )
    tbl.add_column("Brand",        style="bold",        no_wrap=True)
    tbl.add_column("Model",        style="cyan",        no_wrap=True)
    tbl.add_column("Price (£)",    justify="right",     style="green")
    tbl.add_column("Was (£)",      justify="right",     style="dim")
    tbl.add_column("Saving",       justify="right",     style="yellow")
    tbl.add_column("Display",      no_wrap=False,       max_width=28)
    tbl.add_column("Chip",         no_wrap=False,       max_width=26)
    tbl.add_column("RAM",          justify="right")
    tbl.add_column("Storage",      justify="right")
    tbl.add_column("Camera (MP)",  justify="right")
    tbl.add_column("Battery",      justify="right")
    tbl.add_column("5G",           justify="center")
    tbl.add_column("Rating /10",   justify="center",    style="bold")
    tbl.add_column("Best For",     no_wrap=False,       max_width=30)

    for p in phones:
        save = saving(p)
        saving_str = f"£{save}" if save > 0 else "–"
        tbl.add_row(
            p["brand"],
            p["model"],
            f"£{p['price_gbp']:,}",
            f"£{p['original_price_gbp']:,}",
            f"[yellow]{saving_str}[/yellow]",
            p["display"],
            p["processor"],
            f"{p['ram_gb']} GB",
            f"{p['storage_gb']} GB",
            str(p["main_camera_mp"]),
            f"{p['battery_mah']:,} mAh",
            "✅" if p["five_g"] else "❌",
            _rating_str(p["rating_out_of_10"]),
            p["best_for"],
        )

    console.print(tbl)
    console.print()

    # ── Per-tier breakdowns ──────────────────────────────────────────────────
    for lo, hi, tier_name in PRICE_TIERS:
        tier_phones = [p for p in phones if lo <= p["price_gbp"] < hi]
        if not tier_phones:
            continue
        t2 = Table(
            title=f"[bold]{tier_name}[/bold]",
            box=box.SIMPLE_HEAVY,
            show_lines=False,
            header_style="bold blue",
        )
        t2.add_column("Brand")
        t2.add_column("Model",       style="cyan")
        t2.add_column("Price",       justify="right", style="green")
        t2.add_column("Saving",      justify="right", style="yellow")
        t2.add_column("Rating",      justify="center")
        t2.add_column("Value Score", justify="right")
        t2.add_column("Deal Note",   no_wrap=False, max_width=42)

        for p in tier_phones:
            save = saving(p)
            t2.add_row(
                p["brand"],
                p["model"],
                f"£{p['price_gbp']:,}",
                f"£{save}" if save else "–",
                _rating_str(p["rating_out_of_10"]),
                str(value_score(p)),
                p["deal_note"],
            )
        console.print(t2)
        console.print()

    # ── Best Buys ────────────────────────────────────────────────────────────
    best_buys = pick_best_buys(phones)
    console.print(
        Panel.fit("[bold yellow]🌟 Best Buy Recommendations[/bold yellow]", border_style="yellow")
    )

    for cat_key, cat_label in BEST_BUY_CATEGORIES:
        phone = best_buys.get(cat_key)
        if not phone:
            continue
        save = saving(phone)
        save_str = f"  [yellow](Save £{save})[/yellow]" if save > 0 else ""
        highlights = "  •  ".join(phone["highlights"][:3])
        console.print(
            f"  [bold]{cat_label}[/bold]\n"
            f"    [cyan]{phone['brand']} {phone['model']}[/cyan] — "
            f"[green]£{phone['price_gbp']:,}[/green]{save_str}\n"
            f"    {phone['display']}  |  {phone['processor']}  |  "
            f"{phone['ram_gb']} GB RAM  |  {phone['battery_mah']:,} mAh\n"
            f"    {highlights}\n"
            f"    Available at: {', '.join(phone['retailers'])}\n"
        )


# ──────────────────────────── Plain text fallback ────────────────────────────

def print_plain(phones, sort_by="price"):
    if sort_by == "price":
        phones = sorted(phones, key=lambda p: p["price_gbp"])
    elif sort_by == "rating":
        phones = sorted(phones, key=lambda p: p["rating_out_of_10"], reverse=True)
    elif sort_by == "saving":
        phones = sorted(phones, key=saving, reverse=True)

    print("=" * 90)
    print("  UK Smartphone Deals – Brand New, Unlocked, Above £300  |  March 2026")
    print("  Samsung · Apple · OnePlus · Google Pixel")
    print("=" * 90)

    print(f"\n{'Brand':<12}{'Model':<28}{'Price':>8}{'Was':>8}{'Saving':>8}{'Rating':>8}  Best For")
    print("-" * 90)
    for p in phones:
        save = saving(p)
        save_str = f"£{save}" if save else "–"
        print(
            f"{p['brand']:<12}{p['model']:<28}£{p['price_gbp']:>6,}"
            f"  £{p['original_price_gbp']:>5,}  {save_str:>6}  {p['rating_out_of_10']:>4}/10"
            f"  {p['best_for']}"
        )

    print("\n" + "=" * 90)
    print("  BEST BUY RECOMMENDATIONS")
    print("=" * 90)
    best_buys = pick_best_buys(phones)
    for cat_key, cat_label in BEST_BUY_CATEGORIES:
        phone = best_buys.get(cat_key)
        if not phone:
            continue
        save = saving(phone)
        save_str = f" (Save £{save})" if save else ""
        print(f"\n  {cat_label}")
        print(f"    {phone['brand']} {phone['model']} — £{phone['price_gbp']:,}{save_str}")
        print(f"    {phone['display']} | {phone['processor']}")
        print(f"    RAM: {phone['ram_gb']} GB | Battery: {phone['battery_mah']:,} mAh | Camera: {phone['main_camera_mp']} MP")
        print(f"    Highlights: {' | '.join(phone['highlights'][:3])}")
        print(f"    Retailers: {', '.join(phone['retailers'])}")


# ─────────────────────────────── Helpers ─────────────────────────────────────

def _rating_str(r):
    if r >= 9.0:
        return f"[bold green]{r}[/bold green]"
    if r >= 8.0:
        return f"[green]{r}[/green]"
    return f"[yellow]{r}[/yellow]"


# ─────────────────────────────── Entry point ─────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Compare UK smartphone deals (brand new, unlocked, above £300)."
    )
    parser.add_argument(
        "--min-price", type=int, default=300, metavar="GBP",
        help="Minimum price in GBP (default: 300)",
    )
    parser.add_argument(
        "--brand", type=str, default=None,
        choices=["Samsung", "Apple", "OnePlus", "Google"],
        help="Filter by brand",
    )
    parser.add_argument(
        "--sort", type=str, default="price",
        choices=["price", "rating", "saving"],
        help="Sort order: price | rating | saving (default: price)",
    )
    parser.add_argument(
        "--no-color", action="store_true",
        help="Disable Rich colour output",
    )
    args = parser.parse_args()

    phones = filter_phones(PHONES, min_price=args.min_price, brand=args.brand)
    if not phones:
        print("No phones matched the given filters.")
        sys.exit(1)

    if HAS_RICH and not args.no_color:
        print_rich(phones, sort_by=args.sort)
    else:
        print_plain(phones, sort_by=args.sort)


if __name__ == "__main__":
    main()
