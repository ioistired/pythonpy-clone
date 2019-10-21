#!/usr/bin/env python3

__version__ = '0.0.1'
__license__ = 'BlueOak-1.0.0'

"""
A clone of https://github.com/Russell91/pythonpy with less ugly code and supporting import expressions (e.g. sys!.version)
"""

import argparse
import sys

import import_expression
import more_itertools

version_info = 'Pythonpy Clone {}\nPython {}'.format(__version__, sys.version)

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)

group = parser.add_argument_group("Options")

parser.add_argument('expression', nargs='?', default='None', help="e.g. py '2 ** 32'")
group.add_argument(
	'-x', dest='lines_of_stdin', action='store_const', const=True, default=False, help='treat each row of stdin as x')
group.add_argument(
	'-l', dest='list_of_stdin', action='store_const', const=True, default=False, help='treat list of stdin as l')
group.add_argument('-c', dest='pre_cmd', help='run code before expression')
group.add_argument('-C', dest='post_cmd', help='run code after expression')
group.add_argument('-V', '--version', action='version', version=version_info, help='version info')
group.add_argument('-h', '--help', action='help', help="show this help message and exit")

def err(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def without_trailing(it, *, trailing, _exhausted=object()):
	"""yield all elements of it, except for the last one, if the last one == trailing."""
	it = more_itertools.peekable(it)
	for x in it:
		if it.peek(_exhausted) is _exhausted and x == trailing:
			return
		yield x

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

	stdin = without_trailing(map(str.rstrip, sys.stdin), trailing='')  # ignore trailing newline
	code = import_expression.compile(args.expression, '<pythonpy expression>', 'eval')

	if args.list_of_stdin:
		l = list(stdin)
		it = [import_expression.eval(code, dict(l=l))]
	elif args.lines_of_stdin:
		it = (import_expression.eval(code, dict(x=line)) for line in stdin)
	else:
		it = [import_expression.eval(code)]

	for x in it:
		if x is None:
		    continue

		try:
			it = [x] if isinstance(x, str) else iter(x)
		except TypeError:  # not iterable
			print(x)
		else:
			for x in it:
				print(x)

	if args.post_cmd:
		import_expression.exec(args.post_cmd)

if __name__ == '__main__':
	main()
