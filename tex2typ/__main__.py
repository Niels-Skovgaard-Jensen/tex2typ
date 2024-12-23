import argparse
import re

import pypandoc


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
        typst_equation = typst_output.strip()
        typst_equation = fix_bar_notation(typst_equation)
    except Exception as e:
        return f"Error: {e!s}"
    else:
        return typst_equation


def main():
    parser = argparse.ArgumentParser(description="Convert LaTeX equations to Typst format")
    parser.add_argument("equation", help="LaTeX equation to convert")
    args = parser.parse_args()

    result = latex_to_typst(args.equation)
    print(result)


if __name__ == "__main__":
    main()
