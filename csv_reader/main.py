import csv_reader
import argparse


def main():
    parser = argparse.ArgumentParser(description="CSV Reader")
    parser.add_argument("-f", "--file", type=str, help="The CSV file to read")
    parser.add_argument("--where", type=str, help="The filter to apply")
    parser.add_argument("--aggregate", type=str, help="The aggregator to use")
    args = parser.parse_args()

    print(csv_reader.csv_parser(args.file, args.where, args.aggregate))


if __name__ == "__main__":
    main()
