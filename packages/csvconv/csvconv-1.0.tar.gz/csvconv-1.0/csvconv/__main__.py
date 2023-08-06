import sys
import csv
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--dialect', default='excel', choices=csv.list_dialects())
    parser.add_argument('-tD', '--to-dialect', default='excel-tab', choices=csv.list_dialects())
    parser.add_argument('INPUT', type=argparse.FileType())

    args = parser.parse_args()

    with args.INPUT as f:
        reader = csv.reader(f, dialect=args.dialect)
        writer = csv.writer(sys.stdout, dialect=args.to_dialect)

        writer.writerows(reader)

if __name__ == '__main__':
    main()
    """
    csvconv -d comma -dd tab file
    """
