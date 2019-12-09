import inspect
import linecache


class ContextManagerContent(object):
    def __init__(self, max_retries):
        self.max_retries = max_retries
        self._start_line = None
        self._end_line = None

    def __enter__(self):
        calling_frame = inspect.currentframe().f_back
        self._start_line = calling_frame.f_lineno + 1

    def __exit__(self, _type, value, _traceback):
        if not value:
            return True

        calling_frame = inspect.currentframe().f_back
        self._end_line = calling_frame.f_lineno
        source_file = calling_frame.f_code.co_filename
        source_globals = calling_frame.f_globals
        source_locals = calling_frame.f_locals
        source_locals['retried'] = True

        lines = [linecache.getline(source_file, lineno) for lineno in range(self._start_line, self._end_line + 1)]
        code = inspect.cleandoc(''.join(lines))
        print('code to retry:')
        for line in code.splitlines():
            print('  {}'.format(line))
        retries = 0
        while retries < self.max_retries:
            retries += 1
            print('retry {}'.format(retries))
            try:
                exec(code, source_globals, source_locals)
            except Exception:
                pass
            else:
                return True
        raise _type, value, _traceback


def doit():
    a = 0
    with ContextManagerContent(5):
        print('hello {}'.format(a))
        a += 1
        if a < 3:
            raise NotImplementedError
        print('success!')
    print('retried: {}'.format(locals().get('retried', False)))
