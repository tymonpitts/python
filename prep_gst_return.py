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

from typing import List

import ynab_csv

# noinspection PyShadowingBuiltins
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
        'Iron Bridge',
        'Denise Le Cren',
        'Direct Fx',
        'IRD',
        'ACC',
        'GST',
        'Immigration',
        'AA',
        'Weta Digital',
        'Commonsense Organics Wages',
        'Starting Balance',
    ]
    large_outflows = []  # type: List[ynab_csv.Item]
    inflows = []  # type: List[ynab_csv.Item]
    for item in ynab_file.items:
        if item.account == 'GST':
            continue

        if not from_date <= item.date <= to_date:
            continue

        output_lines.append(item.line)

        if item.payee in payees_to_skip:
            continue
        if item.payee.startswith('Transfer'):
            continue

        if item.outflow > threshold:
            large_outflows.append(item)
        elif item.inflow > 0:
            inflows.append(item)

    with open(os.path.abspath(os.path.expanduser(output_file)), 'w') as handle:
        handle.write('\n'.join(output_lines))

    if large_outflows:
        print 'Large Purchases:'
        for item in large_outflows:
            print '{item.date} : {item.account} : {item.payee} : -${item.outflow} : {item.memo}'.format(
                item=item
            )
    else:
        print 'No Large Purchases'

    if inflows:
        print
        print 'Deposits:'
        for item in inflows:
            print '{item.date} : {item.account} : {item.payee} : +${item.inflow} : {item.memo}'.format(
                item=item
            )
    else:
        print 'No Deposits'


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('csv_file')
    parser.add_argument('output_file')
    parser.add_argument('from_date', type=get_date, help='inclusive date with format="DD/MM/YYYY"')
    parser.add_argument('to_date', type=get_date, help='inclusive date with format="DD/MM/YYYY"')
    parser.add_argument('--threshold', type=float, default=500.0)
    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == '__main__':
    parse_args()
