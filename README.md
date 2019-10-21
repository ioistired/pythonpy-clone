# pythonpy clone

This is a rewrite of [pythonpy] with (planned) feature parity and which is more robust. Instead of using regex to attempt to automatically
import all identifiers, it uses a library which I already wrote called [Import Expression Parser] to add easy inline imports
e.g. `urllib.parse!.quote("a b c")`.

For more information, see the [pythonpy] README and `py --help`.

[pythonpy]: https://github.com/Russell91/pythonpy
[Import Expression Parser]: https://github.com/iomintz/import-expression-parser

## Installation

`pip install pythonpy-clone` (or via [pipx]: `pipx install pythonpy-clone`)

From source:

`pip install .`

[pipx]: https://github.com/pipxproject/pipx

## License

BlueOak Model License v1.0.0, see [LICENSE.md](/LICENSE.md).
For rationale, see [kemitchell's blog post on the matter](https://writing.kemitchell.com/2019/03/09/Deprecation-Notice.html).
