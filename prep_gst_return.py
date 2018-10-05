#!/usr/bin/python
"""
Parse YNAB register file and do the following:
    - filter transactions by the GST period date range
    - filter transactions by real accounts (i.e. discard the old GST budget account)
    - output filtered transactions to .csv file (path printed in shell output)
    - print "large transactions" above the --threshold
"""
import argparse
import glob
import os

from typing import List

import ynab_csv
import gst_utils


def main(register, threshold):
    """
    Args:
        register (str):
        threshold (float):
    """
    # get the GST period for which we want to filter transactions for
    from_date, to_date = gst_utils.get_previous_period()

    # parse the register file and filter the transactions by date and real
    # accounts. As we go we'll also gather data about large purchases and
    # deposits that the accountant will need.
    ynab_file = ynab_csv.YnabCsvFile(register)
    output_lines = [ynab_file.lines[0]]
    outflow_groups_to_skip = [
    ]
    large_outflows = []  # type: List[ynab_csv.Item]
    inflows = []  # type: List[ynab_csv.Item]
    for item in ynab_file.items:
        # the "GST" account was a fake account I used to use to track
        # how much money I was saving for the GST return. Transactions here
        # are fake so don't include them.
        # TODO: I don't use this fake account anymore so maybe just remove this
        if item.account == 'GST':
            continue

        # if the transaction did not occur during the GST period then skip it
        if not from_date <= item.date < to_date:
            continue

        # add the transaction to the list of transactions to output
        output_lines.append(item.line)

        # gather data about large purchases or deposits. We skip a bunch of
        # payees here because some payees are not purchases (e.g. Direct FX
        # is transferring money to the States)
        if item.category_group in ('Monthly Essentials', 'Long Term Expenses', 'Vacation'):
            continue
        if item.category in ('GST', 'ACC'):
            continue
        if item.payee in ('Flight Centre', 'Stacey Lake Photography'):
            continue
        if item.inflow and item.payee in ('Weta Digital', 'IRD', 'Starting Balance'):
            continue
        if item.payee.startswith('Transfer'):
            continue

        if item.outflow >= threshold:
            large_outflows.append(item)
        elif item.inflow > 0:
            inflows.append(item)

    # output the filtered transactions to a .csv file named
    # after the GST period's end date
    output_file = '~/Downloads/transactions_for_gst_period_ending_{}.csv'.format(to_date.strftime('%Y-%m-%d'))
    output_file = os.path.abspath(os.path.expanduser(output_file))
    print 'Outputting filtered transactions: {}'.format(output_file)
    with open(output_file, 'w') as handle:
        handle.write('\n'.join(output_lines))

    # print any large purchases
    if large_outflows:
        print 'Large Purchases:'
        for item in large_outflows:
            print '{item.date} : {item.account} : {item.payee} : -${item.outflow} : {item.memo}'.format(
                item=item
            )
    else:
        print 'No Large Purchases'

    # print any deposits other than from Weta
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
    class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
        """ Inherits both RawDescriptionHelpFormatter and ArgumentDefaultsHelpFormatter
        so the whitespace in the parser's description is preserved and the
        default values for the arguments are displayed in their help text
        """
        pass

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        '--register',
        default=sorted(glob.glob(os.path.expanduser('~/Downloads/YNAB Export - NZ Budget as of */* - Register.csv')))[-1],
        help='The .csv file containing all transactions exported from YNAB'
    )
    parser.add_argument(
        '--threshold', type=float, default=500.0,
        help='transaction amount threshold for "large transactions"'
    )
    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == '__main__':
    parse_args()
