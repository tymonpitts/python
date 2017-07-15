#!/usr/bin/python
"""
YNAB exports ALL my data for ALL of my accounts but I only need a certain
date range when GST time comes around and only real accounts (i.e. not the GST
budget account).  The specified date range is inclusive.
"""
import argparse
import datetime
import os

import ynab_csv


def get_date(s, format='%d/%m/%Y'):
    return datetime.datetime.strptime(s, format).date()


def main(csv_file, output_file, from_date, to_date):
    """
    Args:
        csv_file (str):
        output_file (str):
        from_date (datetime.date):
        to_date (datetime.date):
    """
    ynab_file = ynab_csv.YnabCsvFile(csv_file)
    output_lines = [ynab_file.lines[0]]
    for item in ynab_file.items:
        if item.account == 'GST':
            continue

        if from_date <= item.date <= to_date:
            output_lines.append(item.line)

    with open(os.path.abspath(os.path.expanduser(output_file)), 'w') as handle:
        handle.write('\n'.join(output_lines))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    parser.add_argument('output_file')
    parser.add_argument('from_date', type=get_date)
    parser.add_argument('to_date', type=get_date)
    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == '__main__':
    parse_args()
