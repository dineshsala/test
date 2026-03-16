"""Tests for the mobile phone price comparison tool."""

import pytest
from phones import (
    PHONES,
    Phone,
    filter_phones,
    sort_phones,
    run_report,
)


# ---------------------------------------------------------------------------
# Data integrity tests
# ---------------------------------------------------------------------------

def test_all_phones_have_required_fields():
    for p in PHONES:
        assert p.brand, f"Missing brand: {p}"
        assert p.model, f"Missing model: {p}"
        assert p.price_gbp > 0, f"Invalid price for {p.model}"
        assert p.chip, f"Missing chip for {p.model}"


def test_all_phones_are_unlocked_and_brand_new():
    for p in PHONES:
        assert p.unlocked is True, f"{p.model} is not unlocked"
        assert p.condition == "Brand New", f"{p.model} is not brand new"


def test_brands_covered():
    brands = {p.brand for p in PHONES}
    assert "Samsung" in brands
    assert "Apple" in brands
    assert "OnePlus" in brands
    assert "Google" in brands


def test_all_phones_have_5g():
    for p in PHONES:
        assert p.five_g is True, f"{p.model} does not have 5G"


# ---------------------------------------------------------------------------
# Filter tests
# ---------------------------------------------------------------------------

def test_filter_above_300():
    filtered = filter_phones(PHONES, min_price=300.0)
    assert all(p.price_gbp >= 300 for p in filtered)


def test_filter_excludes_below_threshold():
    low_phone = Phone(
        brand="Test", model="Cheap", price_gbp=199.0,
        storage_gb=64, ram_gb=4, display_inches=6.0,
        battery_mah=3000, camera_mp=12, chip="Generic",
        os="Android 13", five_g=False,
    )
    phones_with_cheap = PHONES + [low_phone]
    filtered = filter_phones(phones_with_cheap, min_price=300.0)
    assert low_phone not in filtered


def test_filter_unlocked_only():
    locked_phone = Phone(
        brand="Test", model="Locked", price_gbp=500.0,
        storage_gb=128, ram_gb=8, display_inches=6.5,
        battery_mah=4000, camera_mp=50, chip="Generic",
        os="Android 14", five_g=True, unlocked=False,
    )
    phones_with_locked = PHONES + [locked_phone]
    filtered = filter_phones(phones_with_locked, unlocked_only=True)
    assert locked_phone not in filtered


def test_filter_new_only():
    refurb_phone = Phone(
        brand="Test", model="Refurb", price_gbp=500.0,
        storage_gb=128, ram_gb=8, display_inches=6.5,
        battery_mah=4000, camera_mp=50, chip="Generic",
        os="Android 14", five_g=True, condition="Refurbished",
    )
    phones_with_refurb = PHONES + [refurb_phone]
    filtered = filter_phones(phones_with_refurb, new_only=True)
    assert refurb_phone not in filtered


# ---------------------------------------------------------------------------
# Sort tests
# ---------------------------------------------------------------------------

def test_sort_by_price_ascending():
    filtered = filter_phones(PHONES)
    sorted_phones = sort_phones(filtered, key="price_gbp", reverse=False)
    prices = [p.price_gbp for p in sorted_phones]
    assert prices == sorted(prices)


def test_sort_by_price_descending():
    filtered = filter_phones(PHONES)
    sorted_phones = sort_phones(filtered, key="price_gbp", reverse=True)
    prices = [p.price_gbp for p in sorted_phones]
    assert prices == sorted(prices, reverse=True)


# ---------------------------------------------------------------------------
# Best-buy tests
# ---------------------------------------------------------------------------

def test_best_buys_exist():
    best_buys = [p for p in PHONES if p.best_buy]
    assert len(best_buys) > 0


def test_best_buys_span_multiple_brands():
    brands = {p.brand for p in PHONES if p.best_buy}
    assert len(brands) >= 2


def test_best_buys_all_above_300():
    best_buys = [p for p in PHONES if p.best_buy]
    assert all(p.price_gbp >= 300 for p in best_buys)


# ---------------------------------------------------------------------------
# Smoke test – run_report should not raise
# ---------------------------------------------------------------------------

def test_run_report_runs_without_error(capsys):
    run_report(min_price=300.0)
    captured = capsys.readouterr()
    assert "Samsung" in captured.out
    assert "Apple" in captured.out
    assert "OnePlus" in captured.out
    assert "Google" in captured.out
    assert "£" in captured.out
    assert "BEST BUY" in captured.out
