#! /usr/bin/python
import argparse
import re


def main(csv_file, threshold=None):
    with open(csv_file, 'r') as handle:
        lines = handle.read().splitlines()

    columns = lines[0].split(',')
    amount_column = columns.index('"Inflow"')
    payee_column = columns.index('"Payee"')
    payees_to_skip = ['Transfer : GST', 'Transfer : ANZ Credit', 'Transfer : ANZ Checking', 'Weta Digital']

    for i, line in enumerate(lines[1:]):
        try:
            split = eval(line.replace('$', ''))
            amount = float(split[amount_column])
            if not amount or (threshold and amount < threshold):
                continue

            payee = split[payee_column]
            if payee in payees_to_skip:
                continue

            print '%04d  %s' % (i, line)
        except:
            print 'error on line %s: %s' % (i+1, line)
            raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('--threshold', type=float, default=None)
    args = parser.parse_args()
    main(args.csv_file, threshold=args.threshold)
