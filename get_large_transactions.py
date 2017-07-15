#! /usr/bin/python
import argparse
import re


def main(csv_file, threshold=500.0):
    with open(csv_file, 'r') as handle:
        lines = handle.read().splitlines()

    columns = lines[0].split(',')
    amount_column = columns.index('"Outflow"')
    payee_column = columns.index('"Payee"')
    payees_to_skip = ['Transfer : GST', 'Transfer : ANZ Credit', 'Iron Bridge', 'Denise Le Cren']

    for i, line in enumerate(lines[1:]):
        try:
            split = eval(line.replace('$', ''))
            # split = line.split(',')
            # amount = float(split[amount_column].replace('$', ''))
            amount = float(split[amount_column])
            if amount < threshold:
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
    parser.add_argument('--threshold', type=float, default=500.0)
    args = parser.parse_args()
    main(args.csv_file, threshold=args.threshold)
