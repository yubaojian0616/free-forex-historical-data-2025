# Free Forex Historical Data 2025 (M1 Benchmark) & Zero-Dependency HistData Formatter

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset](https://img.shields.io/badge/Benchmark-2025%20EURUSD%20%7C%20XAUUSD-green)](https://barionquant.com/en/download)
[![Web Tool](https://img.shields.io/badge/Web%20Converter-Zero--Install-blueviolet)](https://barionquant.com/en/tools/histdata-csv-formatter)

A lightweight, zero-dependency Python utility to parse, clean, and standardize raw **HistData** and generic broker CSV exports into clean, gap-verified OHLCV data. 

Also provides direct benchmark links to full-year 2025 1-minute (M1) cleaned datasets for algorithmic backtesting and manual chart replay.

---

## ⚡ The Pain with Free Forex Historical Data

Anyone who has downloaded free historical candlestick data from sites like HistData knows the headaches:
1. **Weird Delimiters & Dialects**: Semicolons (`;`), variable commas, or missing column headers.
2. **Confusing Timestamps**: Non-standard `YYYYMMDD HHMMSS` or split Date/Time columns.
3. **Timezone Pitfalls**: HistData is encoded in **EST without Daylight Saving Time (UTC-5 year-round)**, breaking session overlays (London/NY overlap) if not shifted to UTC.
4. **Platform Incompatibilities**: Python (Pandas/Backtrader), MetaTrader, and local backtesting engines all expect different header conventions.

This repository provides:
- **`converter.py`**: A 1-file, zero-dependency script to clean your raw CSVs.
- **Direct 2025 Datasets**: Full-year continuous benchmark M1 datasets.
- **Web Alternative**: A browser-based GUI converter if you don't want to run Python.

---

## 📥 Direct Download: Full-Year 2025 Cleaned Datasets

If you just need continuous, clean 2025 1-minute benchmark data without running scripts, download the pre-cleaned ZIP packages (no signup, no email required):

| Symbol | Timeframe | Period | Candles | Direct Link |
| :----- | :-------- | :----- | :------ | :---------- |
| **EUR/USD** | 1-Minute (M1) | Full-Year 2025 | 374,281 | [Download BQ_EURUSD_M1_Starter.zip](https://releases.barionquant.com/barionquant/data/BQ_EURUSD_M1_Starter.zip) |
| **XAU/USD (Gold)** | 1-Minute (M1) | Full-Year 2025 | 374,281 | [Download BQ_XAUUSD_M1_Starter.zip](https://releases.barionquant.com/barionquant/data/BQ_XAUUSD_M1_Starter.zip) |

*Both datasets feature UTC timestamps, session-modeled volume, and standard columns: `timestamp,open,high,low,close,volume`.*

---

## 🚀 Quick Start: Using `converter.py`

### 1. Requirements
- Python 3.8+
- Zero external pip dependencies (uses Python standard library `csv`, `datetime`, `argparse`).

### 2. Run the Converter

```bash
# Basic usage (auto-detects delimiter, converts EST -> UTC, writes to [input]_clean.csv)
python converter.py raw_histdata_eurusd.csv

# Specify custom output path
python converter.py raw_histdata_eurusd.csv -o clean_eurusd_m1.csv

# Keep raw EST timezone (skip UTC +5h shift)
python converter.py raw_histdata_eurusd.csv --no-utc
```

### 3. Output Format
Standard continuous ISO-8601 CSV:
```csv
timestamp,open,high,low,close,volume
2025-01-02 22:00:00,1.03450,1.03462,1.03418,1.03430,42
2025-01-02 22:01:00,1.03430,1.03445,1.03420,1.03440,35
```

---

## 🌐 No Python? Free Web & Desktop Tools

If you prefer a graphical interface or trade on Windows:

- 🛠️ **[Web HistData CSV Formatter](https://barionquant.com/en/tools/histdata-csv-formatter)**: Instant in-browser converter with drag-and-drop, candlestick preview, and custom dialect detection (zero upload to server, runs 100% locally in WebAssembly/JS).
- 🖥️ **[BarionQuant Desktop](https://barionquant.com/en/download)**: Free local forex chart replay training desk for Windows. Replay historical price action bar-by-bar offline, enforce 3-line discipline rules, and avoid monthly cloud feed fees.
- 🧮 **[Prop Firm Drawdown Calculator](https://barionquant.com/en/tools/prop-firm-risk-calculator)**: Interactive trailing drawdown & lot-size risk calculator for FTMO, Topstep, and funded challenges.
- 🛡️ **[Discipline Card Generator](https://barionquant.com/en/tools/discipline-card-generator)**: Generate cryptographic process-compliance cards for your daily trading sessions.

---

## 📜 License & Acknowledgments

- Script released under the **MIT License**.
- Market benchmark datasets: Open Benchmark · Educational & Simulation Use Only. See [Download](https://barionquant.com/en/download). Not an exchange feed.
