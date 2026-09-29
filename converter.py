#!/usr/bin/env python3
"""
HistData & Forex CSV Cleaner & Standardizer.

A zero-dependency Python script to convert raw HistData (and generic FX broker CSVs)
into clean, standard OHLCV format suitable for Python (Pandas/Backtrader), Excel,
and local chart replay engines (like BarionQuant Desktop).

Full 2025 year-round cleaned benchmark datasets (EURUSD, XAUUSD) available at:
https://barionquant.com/en/download
Browser-based zero-install tool:
https://barionquant.com/en/tools/histdata-csv-formatter
"""

from __future__ import annotations

import argparse
import csv
import datetime
import sys
from pathlib import Path
from typing import Generator, List, Optional, Tuple


def detect_delimiter(first_line: str) -> str:
    """Detect whether the CSV uses commas, semicolons, or tabs."""
    if ";" in first_line:
        return ";"
    if "\t" in first_line:
        return "\t"
    return ","


def parse_datetime(raw_date: str, raw_time: Optional[str] = None) -> Optional[datetime.datetime]:
    """Parse various HistData timestamp variants into a datetime object."""
    combined = f"{raw_date.strip()} {raw_time.strip()}" if raw_time else raw_date.strip()
    
    # Common formats:
    # 1. 20250102 170000 (standard HistData 1-minute ASCII)
    # 2. 2025.01.02 17:00 (MetaTrader export)
    # 3. 2025-01-02 17:00:00 (ISO format)
    formats = [
        "%Y%m%d %H%M%S",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(combined, fmt)
        except ValueError:
            continue
    return None


def clean_forex_csv(
    input_path: Path,
    output_path: Path,
    est_to_utc: bool = True,
) -> Tuple[int, int]:
    """
    Clean and reformat forex CSV to standard: timestamp,open,high,low,close,volume.
    HistData raw data is in EST without Daylight Saving Time (UTC-5 year-round).
    Optionally converts to standard UTC.
    """
    valid_rows = 0
    skipped_rows = 0

    with open(input_path, "r", encoding="utf-8", errors="replace") as infile:
        first_line = infile.readline()
        if not first_line:
            print(f"[-] Empty input file: {input_path}")
            return 0, 0
        
        delimiter = detect_delimiter(first_line)
        infile.seek(0)
        reader = csv.reader(infile, delimiter=delimiter)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])

            for row in reader:
                if not row or len(row) < 5:
                    skipped_rows += 1
                    continue

                # Ignore header if present
                if any(h in row[0].lower() for h in ["date", "time", "timestamp"]):
                    continue

                dt: Optional[datetime.datetime] = None
                o, h, l, c = None, None, None, None
                v = "0"

                # Check format: Date and Time in one column vs separate
                if len(row) == 5 or (len(row) == 6 and not row[1].replace(":", "").isdigit()):
                    # Format: datetime, open, high, low, close [, volume]
                    dt = parse_datetime(row[0])
                    o, h, l, c = row[1], row[2], row[3], row[4]
                    if len(row) >= 6:
                        v = row[5]
                elif len(row) >= 6:
                    # Format: date, time, open, high, low, close [, volume]
                    dt = parse_datetime(row[0], row[1])
                    o, h, l, c = row[2], row[3], row[4], row[5]
                    if len(row) >= 7:
                        v = row[6]

                if not dt:
                    skipped_rows += 1
                    continue

                # HistData is EST without DST (UTC-5). Adding 5 hours aligns to UTC.
                if est_to_utc:
                    dt = dt + datetime.timedelta(hours=5)

                try:
                    # Verify numeric validity
                    float(o); float(h); float(l); float(c)
                    writer.writerow([
                        dt.strftime("%Y-%m-%d %H:%M:%S"),
                        f"{float(o):.5f}",
                        f"{float(h):.5f}",
                        f"{float(l):.5f}",
                        f"{float(c):.5f}",
                        int(float(v)) if v else 0,
                    ])
                    valid_rows += 1
                except (ValueError, TypeError):
                    skipped_rows += 1
                    continue

    return valid_rows, skipped_rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean & standardize raw HistData / Forex CSVs into continuous standard OHLCV format."
    )
    parser.add_argument("input", type=Path, help="Path to input raw CSV file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Path to output cleaned CSV (defaults to [name]_clean.csv)"
    )
    parser.add_argument(
        "--no-utc",
        action="store_true",
        help="Do not shift HistData EST timestamps to UTC (+5h)",
    )

    args = parser.parse_args()
    input_file = args.input
    if not input_file.exists():
        print(f"[-] Error: input file not found: {input_file}")
        return 1

    output_file = args.output or input_file.with_name(f"{input_file.stem}_clean.csv")
    print(f"[*] Processing {input_file} -> {output_file} ...")

    valid, skipped = clean_forex_csv(input_file, output_file, est_to_utc=not args.no_utc)
    print(f"[+] Done! Wrote {valid:,} clean candles (skipped {skipped:,} malformed rows).")
    print(f"[*] Standard format: timestamp,open,high,low,close,volume")
    print(f"[*] Tip: You can test this dataset offline on BarionQuant Desktop: https://barionquant.com/en/download")
    return 0


if __name__ == "__main__":
    sys.exit(main())
