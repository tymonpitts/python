#!/usr/bin/env python
import sys
import os

if __name__ == '__main__':
    grep_args = ['egrep']
    grep_args.append('-nHRI')
    grep_args.append('--color=always')
    grep_args.append('--exclude "*.pyc"')
    grep_args.append('--exclude-dir ".git"')
    grep_args.append('--exclude-dir ".svn"')
    grep_args.append('--exclude-dir "pkg"')
    grep_args.extend(sys.argv[1:-1])
    grep_args.append('"%s"' % sys.argv[-1])
    grep_args.append('*')
    grep_cmd = ' '.join(grep_args)
    os.system(grep_cmd)

    find_cmd = 'find ./ -regextype "egrep" -regex ".*%s.*"' % sys.argv[1]
    os.system(find_cmd)
    