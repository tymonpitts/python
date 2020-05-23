#!/usr/bin/python
"""
Parse the latest YNAB export in the Downloads folder from this year and print
information about highest balance, interest earned, and tax withheld for each
account for the previous tax year.
"""
import argparse
import datetime
import glob
import locale
import os

import ynab_csv


# TODO: highest balance may not be correct if the transactions within a single
#       day are out of order. Not sure how to solve this one...
def main():
    locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
    current_year = datetime.datetime.now().year
    tax_year = current_year - 1
    csv_file = glob.glob(os.path.expanduser('~/Downloads/YNAB Export - NZ Budget as of {}*/* - Register.csv'.format(current_year)))[-1]
    ynab_file = ynab_csv.YnabCsvFile(csv_file)
    balances = {}
    starting_balances = {}
    highest_balance_dates = {}
    highest_balances = {}
    interest_earned = {}
    tax_withheld = {}
    for item in reversed(ynab_file.items):
        if item.date.year < tax_year:
            starting_balances.setdefault(item.account, 0.0)
            starting_balances[item.account] -= item.outflow
            starting_balances[item.account] += item.inflow
            balances.setdefault(item.account, 0.0)
            balances[item.account] -= item.outflow
            balances[item.account] += item.inflow
        elif item.date.year == tax_year:
            highest_balances.setdefault(item.account, 0.0)
            interest_earned.setdefault(item.account, 0.0)
            tax_withheld.setdefault(item.account, 0.0)
            balances[item.account] -= item.outflow
            balances[item.account] += item.inflow
            if highest_balances[item.account] < balances[item.account]:
                highest_balances[item.account] = balances[item.account]
                highest_balance_dates[item.account] = item.date
            if item.payee == 'Credit Interest Paid':
                interest_earned[item.account] += item.inflow
            if item.payee == 'Withholding Tax':
                tax_withheld[item.account] += item.outflow
        else:
            break
    for account in sorted(starting_balances):
        if not highest_balances.get(account, 0.0) or 'credit' in account.lower():
            continue
        print(account)
        print('  Account Number: ')
        print('  Highest Balance: {}'.format(locale.currency(highest_balances[account], grouping=True)))
        print('  Highest Balance Date: {}'.format(highest_balance_dates[account]))
        if interest_earned[account]:
            print('  Total Interest Earned: {}'.format(locale.currency(interest_earned[account], grouping=True)))
        if tax_withheld[account]:
            print('  Total Tax Withheld: {}'.format(locale.currency(tax_withheld[account], grouping=True)))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == '__main__':
    parse_args()
