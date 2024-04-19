from app.ollie_grade.ollie import Ollie
from app.ollie_grade.grade import Grade
import app.ollie_grade.tests.config as test_cfg
import pandas as pd
import json
import argparse
import sys, os


def compare(commit_csv_filepath: str, reference_csv_filepath: str):
    try:
        df = pd.read_csv(commit_csv_filepath)
        ollie_almost = Ollie(df, "almost-good", is_goofy=True)
        df = pd.read_csv(reference_csv_filepath)
        ollie_good = Ollie(df, "good", is_goofy=True)
    except FileNotFoundError as e:
        print("One of the filepaths were invalid, try again.")
        sys.exit(1)
    comparator = Grade(ollie_almost, ollie_good)
    json_results = comparator.compare()
    output_filepath = "comparison.json"
    with open(output_filepath, "w") as f:
        json.dump(json_results, f)
        print(f"Output saved to: {os.getcwd()}\\{output_filepath}")


def parse_args(arguments: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser("ollies_comparison")
    parser.add_argument(
        "commit_csv_filepath",
        help="A filepath for your captured Ollie (Kinect skeleton frames saved to .csv file).",
    )
    parser.add_argument(
        "reference_csv_filepath",
        help="A filepath for someone's Ollie that will be compared with yours (Kinect skeleton frames saved to .csv file).",
    )
    parser.add_argument(
        "--test",
        "-t",
        action="store_true",
        help="If provided, ignore filepaths and compare hardcoded test .csv files.",
    )
    return parser.parse_args(arguments)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args.test:
        compare(test_cfg.TEST_COMMIT, test_cfg.TEST_REFERENCE)
    else:
        compare(args.commit_csv_filepath, args.reference_csv_filepath)
    sys.exit(0)
