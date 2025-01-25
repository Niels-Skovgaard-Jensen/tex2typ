import argparse

import pyperclip  # type: ignore[import-untyped]

from tex2typ.mappings import LatexToTypstConverter, TypstToLatexConverter


def latex_to_typst(latex_equation: str) -> str:
    """Convert LaTeX equation to Typst equation."""
    try:
        converter = LatexToTypstConverter()
        return converter.convert(latex_equation)
    except Exception as e:
        return f"Error: {e!s}"


def typst_to_latex(typst_equation: str) -> str:
    """Convert Typst equation to LaTeX equation."""
    try:
        converter = TypstToLatexConverter()
        return converter.convert(typst_equation)
    except Exception as e:
        return f"Error: {e!s}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert equations between LaTeX and Typst formats",
        prefix_chars="-",
        allow_abbrev=True,
    )
    parser.add_argument("equation", help="Equation to convert")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy result to clipboard (requires pyperclip)")
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Convert from Typst to LaTeX (default is LaTeX to Typst)"
    )
    args = parser.parse_args()

    result = typst_to_latex(args.equation) if args.reverse else latex_to_typst(args.equation)
    print(result)

    if args.copy:
        pyperclip.copy(result)
        print("Result copied to clipboard!")


if __name__ == "__main__":
    main()
