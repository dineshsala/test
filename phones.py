"""
Mobile Phone Price & Spec Comparison Tool
Covers: Samsung, Apple, OnePlus, Google Pixel
Filter: Brand new, unlocked, above £300 (UK market)
Data reflects market prices as of March 2026.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Phone:
    brand: str
    model: str
    price_gbp: float
    storage_gb: int
    ram_gb: int
    display_inches: float
    battery_mah: int
    camera_mp: int        # main / primary lens
    chip: str
    os: str
    five_g: bool
    unlocked: bool = True
    condition: str = "Brand New"
    best_buy: bool = False
    notes: str = ""


# ---------------------------------------------------------------------------
# Phone catalogue (UK unlocked prices, brand new, March 2026)
# ---------------------------------------------------------------------------

PHONES: List[Phone] = [
    # ── Samsung ──────────────────────────────────────────────────────────────
    Phone(
        brand="Samsung", model="Galaxy S25 Ultra",
        price_gbp=1299.00, storage_gb=256, ram_gb=12,
        display_inches=6.9, battery_mah=5000,
        camera_mp=200, chip="Snapdragon 8 Elite", os="Android 15",
        five_g=True,
        notes="Best Samsung flagship; 200 MP quad-camera, titanium frame, built-in S Pen",
    ),
    Phone(
        brand="Samsung", model="Galaxy S25+",
        price_gbp=999.00, storage_gb=256, ram_gb=12,
        display_inches=6.7, battery_mah=4900,
        camera_mp=50, chip="Snapdragon 8 Elite", os="Android 15",
        five_g=True,
        notes="Large-screen S25 without Ultra price; excellent everyday flagship",
    ),
    Phone(
        brand="Samsung", model="Galaxy S25",
        price_gbp=799.00, storage_gb=128, ram_gb=12,
        display_inches=6.2, battery_mah=4000,
        camera_mp=50, chip="Snapdragon 8 Elite", os="Android 15",
        five_g=True,
        notes="Compact flagship; solid all-rounder with latest Snapdragon",
    ),
    Phone(
        brand="Samsung", model="Galaxy S24 FE",
        price_gbp=599.00, storage_gb=128, ram_gb=8,
        display_inches=6.7, battery_mah=4700,
        camera_mp=50, chip="Exynos 2500", os="Android 15",
        five_g=True,
        notes="Fan Edition – great value flagship features at mid-range price",
    ),
    Phone(
        brand="Samsung", model="Galaxy A55 5G",
        price_gbp=449.00, storage_gb=128, ram_gb=8,
        display_inches=6.6, battery_mah=5000,
        camera_mp=50, chip="Exynos 1480", os="Android 14",
        five_g=True,
        notes="Mid-range workhorse; IP67, AMOLED, 6-year OS support promise",
    ),

    # ── Apple ─────────────────────────────────────────────────────────────────
    Phone(
        brand="Apple", model="iPhone 16 Pro Max",
        price_gbp=1199.00, storage_gb=256, ram_gb=8,
        display_inches=6.9, battery_mah=4685,
        camera_mp=48, chip="A18 Pro", os="iOS 18",
        five_g=True,
        notes="Apple's best; ProMotion 120 Hz, 4K 120fps video, Action Button & Camera Control",
    ),
    Phone(
        brand="Apple", model="iPhone 16 Pro",
        price_gbp=999.00, storage_gb=128, ram_gb=8,
        display_inches=6.3, battery_mah=3582,
        camera_mp=48, chip="A18 Pro", os="iOS 18",
        five_g=True,
        notes="Pro-grade in a compact form; A18 Pro chip, ProRes video",
    ),
    Phone(
        brand="Apple", model="iPhone 16 Plus",
        price_gbp=899.00, storage_gb=128, ram_gb=8,
        display_inches=6.7, battery_mah=4674,
        camera_mp=48, chip="A18", os="iOS 18",
        five_g=True,
        notes="Big screen, big battery, no Pro features; excellent for media consumption",
    ),
    Phone(
        brand="Apple", model="iPhone 16",
        price_gbp=799.00, storage_gb=128, ram_gb=8,
        display_inches=6.1, battery_mah=3561,
        camera_mp=48, chip="A18", os="iOS 18",
        five_g=True,
        notes="Base iPhone 16 – compact, capable, Apple Intelligence ready",
    ),
    Phone(
        brand="Apple", model="iPhone 15",
        price_gbp=699.00, storage_gb=128, ram_gb=6,
        display_inches=6.1, battery_mah=3349,
        camera_mp=48, chip="A16 Bionic", os="iOS 18",
        five_g=True,
        notes="Previous-gen base model; Dynamic Island, USB-C; still sold new",
    ),

    # ── OnePlus ──────────────────────────────────────────────────────────────
    Phone(
        brand="OnePlus", model="OnePlus 13",
        price_gbp=899.00, storage_gb=256, ram_gb=12,
        display_inches=6.82, battery_mah=6000,
        camera_mp=50, chip="Snapdragon 8 Elite", os="Android 15",
        five_g=True,
        notes="Huge 6000 mAh + 100 W wired charging; Hasselblad tuned cameras",
    ),
    Phone(
        brand="OnePlus", model="OnePlus 12",
        price_gbp=749.00, storage_gb=256, ram_gb=12,
        display_inches=6.82, battery_mah=5400,
        camera_mp=50, chip="Snapdragon 8 Gen 3", os="Android 14",
        five_g=True,
        notes="Still excellent value; 100 W charging, Hasselblad camera system",
    ),
    Phone(
        brand="OnePlus", model="OnePlus Nord 4",
        price_gbp=449.00, storage_gb=128, ram_gb=8,
        display_inches=6.74, battery_mah=5500,
        camera_mp=50, chip="Snapdragon 7+ Gen 3", os="Android 14",
        five_g=True,
        notes="Metal unibody mid-ranger; fast 100 W charging, clean OxygenOS",
    ),

    # ── Google Pixel ─────────────────────────────────────────────────────────
    Phone(
        brand="Google", model="Pixel 9 Pro XL",
        price_gbp=1099.00, storage_gb=128, ram_gb=16,
        display_inches=6.8, battery_mah=5060,
        camera_mp=50, chip="Google Tensor G4", os="Android 15",
        five_g=True,
        notes="Best Pixel; 7-year OS updates, top-tier computational photography, Gemini AI",
    ),
    Phone(
        brand="Google", model="Pixel 9 Pro",
        price_gbp=999.00, storage_gb=128, ram_gb=16,
        display_inches=6.3, battery_mah=4700,
        camera_mp=50, chip="Google Tensor G4", os="Android 15",
        five_g=True,
        notes="Compact Pro Pixel; same camera system, titanium frame",
    ),
    Phone(
        brand="Google", model="Pixel 9",
        price_gbp=799.00, storage_gb=128, ram_gb=12,
        display_inches=6.3, battery_mah=4700,
        camera_mp=50, chip="Google Tensor G4", os="Android 15",
        five_g=True,
        notes="Clean Android, great camera, 7-year updates – best mid-premium Pixel",
    ),
    Phone(
        brand="Google", model="Pixel 8a",
        price_gbp=499.00, storage_gb=128, ram_gb=8,
        display_inches=6.1, battery_mah=4492,
        camera_mp=64, chip="Google Tensor G3", os="Android 15",
        five_g=True,
        notes="Budget flagship camera; 7-year updates, compact build, excellent AI features",
    ),
]

# Mark best buys
_BEST_BUY_MODELS = {
    "Galaxy S25",           # best balanced Samsung
    "Galaxy S24 FE",        # best-value Samsung
    "iPhone 16 Pro",        # sweet-spot Apple Pro
    "OnePlus 13",           # best OnePlus value
    "Pixel 9",              # best Pixel value
    "Pixel 8a",             # budget pick
}
for p in PHONES:
    if p.model in _BEST_BUY_MODELS:
        p.best_buy = True


# ---------------------------------------------------------------------------
# Filtering & sorting helpers
# ---------------------------------------------------------------------------

def filter_phones(
    phones: List[Phone],
    min_price: float = 300.0,
    unlocked_only: bool = True,
    new_only: bool = True,
) -> List[Phone]:
    return [
        p for p in phones
        if p.price_gbp >= min_price
        and (not unlocked_only or p.unlocked)
        and (not new_only or p.condition == "Brand New")
    ]


def sort_phones(phones: List[Phone], key: str = "price_gbp", reverse: bool = False) -> List[Phone]:
    return sorted(phones, key=lambda p: getattr(p, key), reverse=reverse)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

COLS = {
    "#":        4,
    "Brand":    10,
    "Model":    24,
    "Price":    10,
    "Storage":  9,
    "RAM":      6,
    "Screen":   8,
    "Battery":  9,
    "Camera":   9,
    "Chip":     22,
    "5G":       4,
    "★":        3,
}

SEP = "  "


def _header() -> str:
    return SEP.join(col.ljust(width) for col, width in COLS.items())


def _divider() -> str:
    return SEP.join("─" * width for col, width in COLS.items())


def _row(idx: int, p: Phone) -> str:
    values = [
        str(idx).ljust(COLS["#"]),
        p.brand.ljust(COLS["Brand"]),
        p.model.ljust(COLS["Model"]),
        f"£{p.price_gbp:,.0f}".ljust(COLS["Price"]),
        f"{p.storage_gb} GB".ljust(COLS["Storage"]),
        f"{p.ram_gb} GB".ljust(COLS["RAM"]),
        f"{p.display_inches}\"".ljust(COLS["Screen"]),
        f"{p.battery_mah:,}".ljust(COLS["Battery"]),
        f"{p.camera_mp} MP".ljust(COLS["Camera"]),
        p.chip.ljust(COLS["Chip"]),
        ("Yes" if p.five_g else "No").ljust(COLS["5G"]),
        ("★" if p.best_buy else "").ljust(COLS["★"]),
    ]
    return SEP.join(values)


def print_table(phones: List[Phone]) -> None:
    print(_header())
    print(_divider())
    for i, p in enumerate(phones, start=1):
        print(_row(i, p))


def print_best_buys(phones: List[Phone]) -> None:
    picks = [p for p in phones if p.best_buy]
    if not picks:
        print("  No best-buy picks in current selection.")
        return
    for p in picks:
        print(f"  ★  {p.brand} {p.model}  –  £{p.price_gbp:,.0f}")
        print(f"     {p.notes}")
        print()


def print_brand_section(brand: str, phones: List[Phone]) -> None:
    brand_phones = [p for p in phones if p.brand == brand]
    if not brand_phones:
        return
    print(f"\n{'═' * 90}")
    print(f"  {brand.upper()} ({len(brand_phones)} phones)")
    print(f"{'═' * 90}")
    print_table(brand_phones)
    bbs = [p for p in brand_phones if p.best_buy]
    if bbs:
        print(f"\n  Best Buy Picks for {brand}:")
        for p in bbs:
            print(f"    ★  {p.model}  £{p.price_gbp:,.0f}  –  {p.notes}")


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------

def run_report(min_price: float = 300.0) -> None:
    print("=" * 90)
    print("  MOBILE PHONE DEALS – UK MARKET  |  Brand New · Unlocked  |  Above £300")
    print(f"  Data: Samsung · Apple · OnePlus · Google Pixel  |  As of March 2026")
    print("=" * 90)

    phones = filter_phones(PHONES, min_price=min_price)
    phones_by_price = sort_phones(phones, key="price_gbp")

    # ── Full sorted list ──────────────────────────────────────────────────────
    print(f"\n{'─' * 90}")
    print("  ALL PHONES SORTED BY PRICE (lowest first)")
    print(f"{'─' * 90}")
    print_table(phones_by_price)

    # ── Per-brand breakdown ───────────────────────────────────────────────────
    for brand in ("Samsung", "Apple", "OnePlus", "Google"):
        print_brand_section(brand, phones_by_price)

    # ── Best buys summary ─────────────────────────────────────────────────────
    print(f"\n{'=' * 90}")
    print("  ★  BEST BUY RECOMMENDATIONS")
    print(f"{'=' * 90}")
    print_best_buys(phones_by_price)

    # ── Category winners ──────────────────────────────────────────────────────
    print(f"{'─' * 90}")
    print("  CATEGORY PICKS")
    print(f"{'─' * 90}")

    categories = {
        "Best Overall":       max(phones, key=lambda p: (p.camera_mp + p.ram_gb * 10 + p.storage_gb // 10 - p.price_gbp // 100)),
        "Best Camera":        max(phones, key=lambda p: p.camera_mp),
        "Biggest Battery":    max(phones, key=lambda p: p.battery_mah),
        "Best Value (>£300)": min(phones_by_price, key=lambda p: p.price_gbp),
        "Premium Pick":       max(phones, key=lambda p: p.ram_gb),
    }

    for cat, phone in categories.items():
        flag = " ★" if phone.best_buy else ""
        print(f"  {cat:<22}  {phone.brand} {phone.model:<24}  £{phone.price_gbp:,.0f}{flag}")
        print(f"  {'':22}  {phone.notes}")
        print()

    # ── Price tier summary ────────────────────────────────────────────────────
    tiers = [
        ("Budget Premium  (£300–£599)",  300,  599),
        ("Mid Premium     (£600–£899)",  600,  899),
        ("High Premium    (£900–£1199)", 900, 1199),
        ("Ultra Premium   (£1200+)",    1200, 9999),
    ]
    print(f"{'─' * 90}")
    print("  PRICE TIERS")
    print(f"{'─' * 90}")
    for label, lo, hi in tiers:
        tier_phones = [p for p in phones_by_price if lo <= p.price_gbp <= hi]
        names = ", ".join(f"{p.brand} {p.model} (£{p.price_gbp:,.0f})" for p in tier_phones)
        print(f"  {label}: {names or 'none'}")

    print(f"\n{'=' * 90}")
    print("  Notes:  ★ = Best Buy recommendation  |  All phones: 5G · Brand New · Unlocked")
    print("          Prices sourced from major UK retailers (Amazon, John Lewis, retailer sites).")
    print(f"{'=' * 90}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    min_price = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
    run_report(min_price=min_price)
