# dodeka

[![Build Status](https://travis-ci.org/shimst3r/dodeka.svg?branch=master)](https://travis-ci.org/shimst3r/dodeka)

> δώδεκα (/ˈðoðeka/)
>
> Greek word for the number 12

`dodeka` is a command line tool for tracking the degree of fulfilment of [The Twelve-Factor App][1] methodology. Use it in your projects to test whether they conform
to the principles for developing solid web apps that originated within [Heroku](https://www.heroku.com).

## Table of Contents

* [About The Twelve-Factor App](#about-the-twelve-factor-app)
* [About `dodeka`](#about-dodeka)
* [Usage Examples](#usage-examples)
* [How to Test](#how-to-test)
* [How to Contribute](#how-to-contribute)
* [Contributors](#contributors)
* [License](#license)

## About The Twelve-Factor App

Quoting [1]:

> The twelve-factor app is a methodology for building software-as-a-service apps that:
>
> * Use declarative formats for setup automation, to minimize time and cost for new developers joining the project;
> * Have a clean contract with the underlying operating system, offering maximum portability between execution environments;
> * Are suitable for deployment on modern cloud platforms, obviating the need for servers and systems administration;
> * Minimize divergence between development and production, enabling continuous deployment for maximum agility;
> * And can scale up without significant changes to tooling, architecture, or development practices.
>
> The twelve-factor methodology can be applied to apps written in any programming language, and which use any combination of backing services (database, queue,
> memory cache, etc).

## About `dodeka`

`dodeka` is a tool for professional developers.

Especially in agile teams, the day to day work can already be quite stressful, so that important details like the 12 factors can be overlooked easily. `dodeka` can
be used as a continuous reminder: Once created, the checklist is a living artefact that can be discussed, updated, and used to track progress.

The vision of `dodeka` goes way beyond a mere checklist: As a huge fan of [continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery),
 I envision the tool to be used as naturally as type checkers or code linters, to ensure that your web app sticks as close to the 12 factors as you want it to.
 Therefore `dodeka` will incorporate mechanisms to vet your code, your repository, and your config files (if present).

This is a very ambitious undertaking. If you want to join me, see the [How to Contribute](#how-to-contribute) section.

## Usage Examples

`dodeka` can be used to generate a checklist containing the 12 factors:

```python
from dodeka import factors

list_of_factors = factors.generate_factors()
print(factors.generate_checklist(factors=list_of_factors))
```

If installed from PyPI, `dodeka` can also be used from the command line:

```sh
dodeka --help
```

To print a markdown-formatted checklist to standard output, use the following command:

```sh
dodeka --print
```

## How to Test

The test suite is based on the great [`pytest`][2] library. Once installed, the automatic test discovery can be used via

```sh
pytest dodeka
```

## How to Contribute

This project is released under the MIT license because I opt for a wide acceptance rate. This also means that I am happy for contributions! This can be done on many
ways:

* Open PRs with improvements,
* add issues if you find bugs,
* add issues for new features,
* use `dodeka` and spread the word.

PRs have to comply with:

* [`black`](https://black.readthedocs.io/en/stable/),
* [`mypy`](http://mypy-lang.org),
* and [`pylint`](https://www.pylint.org).

New features must be covered by proper tests (idealy unit tests and functional tests) using the [`pytest`][2] library.

## Contributors

* [shimst3r](https://twitter.com/shimst3r)

## License

> Copyright (c) 2019 Nils Müller
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

[1]: https://12factor.net
[2]: http://pytest.org/en/latest/
