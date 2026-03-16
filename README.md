# 📱 UK Mobile Deals Comparison

Compares **brand-new, unlocked** smartphones from **Samsung, Apple, OnePlus and Google Pixel**
priced **above £300** in the UK, with specs comparison and best-buy recommendations.

## Quick Start

```bash
python3 compare_phones.py              # full colour table + best buys
python3 compare_phones.py --sort rating
python3 compare_phones.py --brand Samsung
python3 compare_phones.py --min-price 700
python3 compare_phones.py --no-color   # plain text output
```

## Files

| File | Description |
|------|-------------|
| `compare_phones.py` | Main script – run this to see the comparison |
| `phones_data.py` | Curated dataset: specs & UK prices (March 2026) |
| `MOBILE_DEALS_REPORT.md` | Full markdown report with tables & best-buy write-ups |

## Criteria

- ✅ Brand new
- ✅ SIM-free / unlocked
- ✅ Price above £300 GBP
- ✅ Brands: Samsung, Apple, OnePlus, Google Pixel only

## Requirements

- Python 3.8+
- `rich` library (for coloured output): `pip install rich`

See **[MOBILE_DEALS_REPORT.md](MOBILE_DEALS_REPORT.md)** for the full comparison and recommendations.
