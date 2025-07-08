# tex2typ

[![Release](https://img.shields.io/github/v/release/Niels-Skovgaard-Jensen/tex2typ)](https://img.shields.io/github/v/release/Niels-Skovgaard-Jensen/tex2typ)
[![Build status](https://img.shields.io/github/actions/workflow/status/Niels-Skovgaard-Jensen/tex2typ/main.yml?branch=main)](https://github.com/Niels-Skovgaard-Jensen/tex2typ/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/Niels-Skovgaard-Jensen/tex2typ/branch/main/graph/badge.svg)](https://codecov.io/gh/Niels-Skovgaard-Jensen/tex2typ)
[![Commit activity](https://img.shields.io/github/commit-activity/m/Niels-Skovgaard-Jensen/tex2typ)](https://img.shields.io/github/commit-activity/m/Niels-Skovgaard-Jensen/tex2typ)
[![License](https://img.shields.io/github/license/Niels-Skovgaard-Jensen/tex2typ)](https://img.shields.io/github/license/Niels-Skovgaard-Jensen/tex2typ)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python CLI tool for converting LaTeX equations into Typst equations and back

## Quick start as a `uv tool` (recommended)

```bash
uvx tex2typ <YourLaTeXEquation> <options>
```

Example:

```bash
uvx tex2typ "\boldsymbol{H^i} = -\frac{1}{j\omega\mu_0}\nabla\times\boldsymbol{E^i}" -c
```

Will return and copy to clipboard:

```
$ bold(H^i) = - frac(1, j omega mu_0) nabla times bold(E^i) $
```

## Installation

tex2typ requires Pandoc and Typst to be installed

- Pandoc installation:
https://pandoc.org/installing.html
- Typst installation:
https://github.com/typst/typst

tex2typ is hosted on PyPI and can be installed through uv or pip. We recommend using it as a uvx tool:
uv:
```bash
uvx tex2typ
```

# Running CLI

If using a virtual env or conda, run

```bash
uvx tex2typ <YourEquation> <options>
```

Where `-c` automatically copies the resulting Typst equation to your clipboard, and `-r` allows you to convert back from Typst to LaTeX.

Example:
```bash
uvx tex2typ "\boldsymbol{H^i} = -\frac{1}{j\omega\mu_0}\nabla\times\boldsymbol{E^i}" -c
```
Which will return and copy to the clipboard:
```
$ bold(H^i) = - frac(1, j omega mu_0) nabla times bold(E^i) $
```

## Typst to LaTeX

By providing the `-r` option, one can convert from typst to LaTeX.
Example:
```bash
uvx run tex2typ "bold(H^i) = - frac(1, j omega mu_0) nabla times bold(E^i)" -r
```

Will return:

```
\mathbf{H^i} = -\frac{1}{j\omega\mu_0}\nabla\times\mathbf{E^i}
```

Options:

- `-c` or `--copy`: Copy the result to your clipboard
- `-r` or `--reverse`: Convert from Typst to LaTeX (default is LaTeX to Typst)



