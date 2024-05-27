#!/usr/bin/env python3

import re
import setuptools
import sys
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE / 'pythonpy_clone.py') as f:
	VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not VERSION:
	raise RuntimeError('version is not set')

with open(HERE / 'README.md') as f:
	README = f.read()

setuptools.setup(
	name='pythonpy-clone',
	author='io mintz',
	url='https://github.com/ioistired/pythonpy-clone',
	version=VERSION,
	py_modules=['pythonpy_clone'],
	license='BlueOak-1.0.0',
	description='rewrite of pythonpy using AST manipulations instead of regex',
	long_description=README,
	long_description_content_type='text/markdown; variant=GFM',
	install_requires=['import-expression>=1.0.0,<2.0.0'],
	python_requires='>=3.6.0',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: System Administrators',
		'Topic :: Utilities',
		'Natural Language :: English',
		'Operating System :: OS Independent',
	],
	entry_points={
		'console_scripts': list(map(
			'py{} = pythonpy_clone:main'.format,
			('', sys.version_info.major, '.'.join(map(str, sys.version_info[:2])))
		)),
	},
)
