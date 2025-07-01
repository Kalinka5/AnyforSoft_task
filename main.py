"""
CLI entry point for the MLM Commission Engine.
"""
import argparse
import json
import sys
import os
from datetime import datetime

from src.data_loader import load_partners
from src.tree_validator import validate_hierarchy
from src.commission_engine import CommissionCalculator
from src.utils import get_days_in_month, get_current_year_month

def main():
    """
    Main function to run the commission calculation engine.
    """
    parser = argparse.ArgumentParser(description="MLM Commission Engine")
    parser.add_argument(
        "--input", required=True, help="Path to the input partners JSON file."
    )
    parser.add_argument(
        "--output", required=True, help="Path to the output commissions JSON file."
    )
    parser.add_argument(
        "--month",
        help="The month for which to calculate commissions (YYYY-MM). Defaults to the current month.",
    )
    args = parser.parse_args()

    try:
        if args.month:
            try:
                year, month = map(int, args.month.split("-"))
            except ValueError:
                raise ValueError("Invalid month format. Please use YYYY-MM.")
        else:
            year, month = get_current_year_month()

        days_in_month = get_days_in_month(year, month)

        partners = load_partners(args.input)
        validate_hierarchy(partners)

        calculator = CommissionCalculator(partners, days_in_month)
        commissions = calculator.calculate_commissions()

        # Ensure the output directory exists
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(commissions, f, indent=2)

        print(f"Successfully calculated commissions for {year}-{month:02d} and saved to '{args.output}'")

    except (FileNotFoundError, ValueError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
