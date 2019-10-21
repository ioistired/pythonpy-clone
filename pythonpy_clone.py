#!/usr/bin/env python3

__version__ = '0.0.3'
__license__ = 'BlueOak-1.0.0'

"""
A clone of https://github.com/Russell91/pythonpy with less ugly code and supporting import expressions (e.g. sys!.version)
"""

import argparse
import functools
import re
import sys

import import_expression

version_info = 'Pythonpy Clone {}\nPython {}'.format(__version__, sys.version)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)

parser.add_argument('expression', nargs='?', default='None', help="e.g. py '2 ** 32'")
parser.add_argument(
	'-x', dest='lines_of_stdin', action='store_const', const=True, default=False, help='treat each row of stdin as x')
parser.add_argument(
	'-l', dest='list_of_stdin', action='store_const', const=True, default=False, help='treat list of stdin as l')
parser.add_argument('--si', '--split_input', dest='input_delimiter', help='split each line of input on this regex')
parser.add_argument('--so', '--split_output', dest='output_delimiter', help='print each line of output joined by this string')
parser.add_argument('-c', dest='pre_cmd', help='run code before expression')
parser.add_argument('-C', dest='post_cmd', help='run code after expression')
parser.add_argument('-V', '--version', action='version', version=version_info, help='version info')
parser.add_argument('-h', '--help', action='help', help='show this help message and exit')

def err(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main():
	args = parser.parse_args()
	if sum((args.list_of_stdin, args.lines_of_stdin)) > 1:
		err('Pythonpy accepts at most one of [-x, -l] flags')
		sys.exit(1)

	if args.pre_cmd:
		import_expression.exec(args.pre_cmd)

	if not args.expression and args.post_cmd:
		import_expression.exec(args.post_cmd)
		sys.exit(0)

	stdin = map(str.rstrip, sys.stdin)  # ignore trailing newline

	if args.input_delimiter:
		split = re.compile(args.input_delimiter).split
		stdin = (split(l.rstrip()) for l in stdin)

	if args.output_delimiter:
		def fprint(x, join=args.output_delimiter.join):
			if x is not None:
				print(join(x))
	else:
		def fprint(x):
			if x is not None:
				print(x)

	code = import_expression.compile(args.expression, '<pythonpy expression>', 'eval')

	if args.list_of_stdin:
		l = list(stdin)
		it = [import_expression.eval(code, dict(l=l))]
	elif args.lines_of_stdin:
		it = (import_expression.eval(code, dict(x=line)) for line in stdin)
	else:
		it = [import_expression.eval(code)]

	for x in it:
		try:
			it = [x] if isinstance(x, str) else iter(x)
		except TypeError:  # not iterable
			fprint(x)
		else:
			for x in it:
				fprint(x)

	if args.post_cmd:
		import_expression.exec(args.post_cmd)

if __name__ == '__main__':
	main()
