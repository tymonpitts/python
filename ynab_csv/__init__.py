import datetime
import functools
import os
import re


QUOTE_REPLACEMENT = '&quote&'

def item_property_decorator(expected_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(self):
            try:
                return self._cache[func.__name__]
            except KeyError:
                try:
                    self._cache[func.__name__] = func(self)
                    assert isinstance(self._cache[func.__name__], expected_type)
                    return self._cache[func.__name__]
                except:
                    print 'error on line %s: %s' % (self.line_number, self.line)
                    raise
        return wrapped
    return decorator


class YnabCsvFile(object):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(os.path.expanduser(file_path))
        with open(self.file_path, 'r') as handle:
            contents = handle.read().strip()
        contents = contents.replace('\\"', QUOTE_REPLACEMENT)
        self.lines = contents.splitlines()

        expected_colums = [
            'Account',
            'Flag',
            'Date',
            'Payee',
            'Category Group/Category',
            'Category Group',
            'Category',
            'Memo',
            'Outflow',
            'Inflow',
            'Cleared',
        ]
        self.columns = [eval(c) for c in self.lines[0].split(',')]
        if self.columns != expected_colums:
            raise Exception('Unexpected columns: %s != %s' % (self.columns, expected_colums))

        self.line_pattern = re.compile(
            r'"(?P<account>.+)",'
            r'"(?P<flag>.*)",'
            r'"(?P<date>.+)",'
            r'"(?P<payee>.*)",'
            r'"(?P<full_category>.*)",'
            r'"(?P<category_group>.*)",'
            r'"(?P<category>.*)",'
            r'"(?P<memo>.*)",'
            r'\$(?P<outflow>[0-9.]+),'
            r'\$(?P<inflow>[0-9.]+),'
            r'"(?P<cleared>(Cleared|Uncleared))"'
        )

        self.items = [Item(self, l, i+1) for i, l in enumerate(self.lines[1:])]


class Item(object):
    def __init__(self, file, line, line_number):
        """
        Args:
            file (YnabCsvFile):
            line (str):
            line_number (int):
        """
        self.file = file
        self.line = line
        self.line_number = line_number

        match = self.file.line_pattern.match(line)
        if not match:
            raise Exception('could not parse line %s: %s' % (self.line_number, self.line))

        self.account = match.group('account')  # type: str
        self.flag = match.group('flag')  # type: str
        self.date = datetime.datetime.strptime(match.group('date'), '%d/%m/%Y').date()
        self.payee = match.group('payee')  # type: str
        self.full_category = match.group('full_category')  # type: str
        self.category_group = match.group('category_group')  # type: str
        self.category = match.group('category')  # type: str
        self.memo = match.group('memo').replace(QUOTE_REPLACEMENT, '"')  # type: str
        self.outflow = float(match.group('outflow'))
        self.inflow = float(match.group('inflow'))
        self.cleared = match.group('cleared') == 'Cleared'


    #     self._split = line.split(',')
    #     self._cache = {}
    #
    # @property
    # @item_property_decorator(str)
    # def account(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.account_column])
    #
    # @property
    # @item_property_decorator(str)
    # def flag(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.flag_column])
    #
    # @property
    # @item_property_decorator(datetime.date)
    # def date(self):
    #     """
    #     Returns:
    #         datetime.date
    #     """
    #     return datetime.datetime.strptime(self._split[self.file.date_column], '"%d/%m/%Y"').date()
    #
    # @property
    # @item_property_decorator(str)
    # def payee(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.payee_column])
    #
    # @property
    # @item_property_decorator(str)
    # def full_category(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.full_category_column])
    #
    # @property
    # @item_property_decorator(str)
    # def category_group(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.category_group_column])
    #
    # @property
    # @item_property_decorator(str)
    # def category(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.category_column])
    #
    # @property
    # @item_property_decorator(str)
    # def memo(self):
    #     """
    #     Returns:
    #         str
    #     """
    #     return eval(self._split[self.file.memo_column])
    #
    # @property
    # @item_property_decorator(float)
    # def outflow(self):
    #     """
    #     Returns:
    #         float
    #     """
    #     return eval(self._split[self.file.outflow_column].replace('$', '', 1))
    #
    # @property
    # @item_property_decorator(float)
    # def inflow(self):
    #     """
    #     Returns:
    #         float
    #     """
    #     return eval(self._split[self.file.inflow_column].replace('$', '', 1))
    #
    # @property
    # @item_property_decorator(bool)
    # def cleared(self):
    #     """
    #     Returns:
    #         bool
    #     """
    #     assert self._split[self.file.cleared_column] in ('"Cleared"', '"Uncleared"')
    #     return self._split[self.file.cleared_column] == '"Cleared"'
