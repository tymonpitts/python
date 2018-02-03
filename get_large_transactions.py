#! /usr/bin/python
import argparse

import ynab_csv


def main(csv_file, threshold=500.0):
    ynab_file = ynab_csv.YnabCsvFile(csv_file)
    payees_to_skip = [
        'Iron Bridge',
        'Denise Le Cren',
        'Direct Fx',
        'IRD',
        'ACC',
        'GST',
        'Immigration',
        'AA',
        'Flight Centre',
        'Weta Digital',
        'Commonsense Organics Wages',
        'Starting Balance',
    ]

    for item in ynab_file.items:
        if item.payee in payees_to_skip:
            continue
        if item.payee.startswith('Transfer'):
            continue
        if item.outflow > threshold:
            print '{item.date} : {item.account} : {item.payee} : -${item.outflow} : {item.memo}'.format(
                item=item
            )
        elif item.inflow > threshold:
            print '{item.date} : {item.account} : {item.payee} : +${item.inflow} : {item.memo}'.format(
                item=item
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('--threshold', type=float, default=500.0)
    args = parser.parse_args()
    main(args.csv_file, threshold=args.threshold)
