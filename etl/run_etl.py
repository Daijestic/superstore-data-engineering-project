from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .extract import extract_raw_data
    from .transform import build_dimensions_and_fact
    from .load import save_csv
except ImportError:
    from extract import extract_raw_data
    from transform import build_dimensions_and_fact
    from load import save_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Superstore ETL based on the notebook logic."
    )
    parser.add_argument(
        "--input",
        default="../data/superstore_raw.csv",
        help="Path to the raw Superstore CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory to store output CSV files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    raw_df = extract_raw_data(input_path)
    dim_customer, dim_product, dim_location, fact_sales = build_dimensions_and_fact(raw_df)

    save_csv(dim_customer, output_dir / "dim_customer.csv")
    save_csv(dim_product, output_dir / "dim_product.csv")
    save_csv(dim_location, output_dir / "dim_location.csv")
    save_csv(fact_sales, output_dir / "fact_sales.csv")

    print("ETL hoàn tất.")
    print(f"- Input: {input_path}")
    print(f"- Output directory: {output_dir}")
    print(f"- dim_customer rows: {len(dim_customer)}")
    print(f"- dim_product rows: {len(dim_product)}")
    print(f"- dim_location rows: {len(dim_location)}")
    print(f"- fact_sales rows: {len(fact_sales)}")


if __name__ == "__main__":
    main()
