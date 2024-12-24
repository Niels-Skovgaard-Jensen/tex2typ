import argparse
import re

import pypandoc  # type: ignore[import-untyped]
import pyperclip  # type: ignore[import-untyped]


def fix_bar_notation(typst_eq: str) -> str:
    """Replace x^(‾) with #bar(x) in Typst equations."""
    # Pattern matches any character followed by ^(‾)
    pattern = r"(\w+)\^\(‾\)"
    return re.sub(pattern, r"overline(\1)", typst_eq)


def latex_to_typst(latex_equation: str) -> str:
    """Convert LaTeX equation to Typst equation using pandoc."""
    try:
        # Create the LaTeX content with proper document structure
        latex_content = f"""
        \\documentclass{{article}}
        \\begin{{document}}
        $${latex_equation}$$
        \\end{{document}}
        """

        # Convert using pypandoc
        typst_output = pypandoc.convert_text(latex_content, "typst", format="latex", extra_args=["--wrap=none"])

        # Clean up the output and fix bar notation
        typst_equation: str = fix_bar_notation(typst_output.strip())
    except Exception as e:
        return f"Error: {e!s}"
    else:
        return typst_equation


def typst_to_latex(typst_equation: str) -> str:
    """Convert Typst equation to LaTeX equation using pandoc."""
    try:
        # Create the Typst content
        typst_content = f"{typst_equation}"

        # Convert using pypandoc
        latex_output = pypandoc.convert_text(typst_content, "latex", format="typst", extra_args=["--wrap=none"])

        # Clean up the output
        latex_equation: str = latex_output
    except Exception as e:
        return f"Error: {e!s}"
    else:
        return latex_equation


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert equations between LaTeX and Typst formats")
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
