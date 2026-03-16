# Mobile Phone Price & Spec Comparison Tool

A Python command-line tool that compares **brand new, unlocked** smartphones from
**Samsung, Apple, OnePlus and Google Pixel** at prices **above £300** in the UK market.

## Features

- Full spec table (price, storage, RAM, display, battery, camera, chip, 5G)
- Sorted by price (lowest → highest)
- Per-brand breakdown
- Best-buy recommendations marked with ★
- Category winners (Best Overall, Best Camera, Biggest Battery, Best Value, Premium Pick)
- Price-tier summary (Budget / Mid / High / Ultra Premium)

## Usage

```bash
# Default – show all phones above £300
python phones.py

# Custom minimum price
python phones.py 500
```

## Run tests

```bash
pip install pytest
python -m pytest test_phones.py -v
```

## Data

Prices reflect UK market figures (Amazon, John Lewis, official brand stores) as of **March 2026**.
All phones are **5G, brand new and unlocked**.

| Brand   | Models included |
|---------|----------------|
| Samsung | Galaxy S25 Ultra, S25+, S25, S24 FE, A55 5G |
| Apple   | iPhone 16 Pro Max, 16 Pro, 16 Plus, 16, 15 |
| OnePlus | OnePlus 13, 12, Nord 4 |
| Google  | Pixel 9 Pro XL, 9 Pro, 9, 8a |
