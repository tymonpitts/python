#!/usr/bin/python
"""
Parse YNAB csv file and do the following:
- filter by date range
- filter by real accounts (i.e. discard GST budget account)
- output large transactions
"""
import argparse
import datetime
import os

import ynab_csv


def get_date(s, format='%d/%m/%Y'):
    return datetime.datetime.strptime(s, format).date()


def main(csv_file, output_file, from_date, to_date, threshold):
    """
    Args:
        csv_file (str):
        output_file (str):
        from_date (datetime.date):
        to_date (datetime.date):
        threshold (float):
    """
    ynab_file = ynab_csv.YnabCsvFile(csv_file)
    output_lines = [ynab_file.lines[0]]
    payees_to_skip = [
        'Transfer : GST',
        'Transfer : ANZ Credit',
        'Transfer : ANZ Checking',
        'Iron Bridge',
        'Denise Le Cren',
        'Weta Digital',
    ]
    large_outflows = []  # type: list[ynab_csv.Item]
    large_inflows = []  # type: list[ynab_csv.Item]
    for item in ynab_file.items:
        if item.account == 'GST':
            continue

        if not from_date <= item.date <= to_date:
            continue

        output_lines.append(item.line)

        if item.payee in payees_to_skip:
            continue

        if item.outflow > threshold:
            large_outflows.append(item)
        elif item.inflow > threshold:
            large_inflows.append(item)

    with open(os.path.abspath(os.path.expanduser(output_file)), 'w') as handle:
        handle.write('\n'.join(output_lines))

    if large_outflows:
        print 'Large Purchases:'
        for item in large_outflows:
            print '  %04d  %s' % (item.line_number, item.line)
    else:
        print 'No Large Purchases'

    if large_inflows:
        print
        print 'Large Sales:'
        for item in large_inflows:
            print '  %04d  %s' % (item.line_number, item.line)
    else:
        print 'No Large Sales'


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    parser.add_argument('output_file')
    parser.add_argument('from_date', type=get_date)
    parser.add_argument('to_date', type=get_date)
    parser.add_argument('--threshold', type=float, default=500.0)
    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == '__main__':
    parse_args()
