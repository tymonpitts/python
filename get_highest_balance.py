#! /usr/bin/python
import argparse
def main(opening_balance, csv_file, gst=False):
    with open(csv_file, 'r') as handle:
        lines = handle.read().splitlines()
    balance = opening_balance
    balances = [balance]
    interest_earned = 0.0
    tax_withheld = 0.0
    for i, line in enumerate(lines):
        try:
            split = line.split(',')
            date = split[6]
            amount = float(split[5])
            balance += amount
            balances.append((balance, date))
            print('{} : {} : {}'.format(date, amount, balance))
            if gst:
                name = split[0]
                if name == 'Credit Interest Paid':
                    interest_earned += amount
                if name == 'Withholding Tax':
                    tax_withheld += -amount
        except:
            print 'error on line %s' % i
            raise
    print 'highest balance: %s' % (max(balances),)
    if gst:
        print 'interest earned: %s' % interest_earned
        print 'tax withheld: %s' % tax_withheld

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('opening_balance', type=float)
    parser.add_argument('csv_file')
    parser.add_argument('--gst', action='store_true')
    args = parser.parse_args()
    main(args.opening_balance, args.csv_file, gst=args.gst)
