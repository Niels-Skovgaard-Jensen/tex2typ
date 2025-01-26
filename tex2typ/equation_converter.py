import re

import pypandoc  # type: ignore[import-untyped]
import pyperclip  # type: ignore[import-untyped]


class EquationConverter:
    """Class to handle equation conversions between LaTeX and Typst formats."""

    @staticmethod
    def fix_bar_notation(typst_eq: str) -> str:
        """Replace x^(‾) with #bar(x) in Typst equations.

        Args:
            typst_eq: The Typst equation to fix

        Returns:
            The fixed Typst equation
        """
        # Pattern matches any character followed by ^(‾)
        pattern = r"(\w+)\^\(‾\)"
        return re.sub(pattern, r"overline(\1)", typst_eq)

    def latex_to_typst(
        self, latex_equation: str, copy_to_clipboard: bool = False
    ) -> str:
        """Convert LaTeX equation to Typst equation using pandoc.

        Args:
            latex_equation: The LaTeX equation to convert
            copy_to_clipboard: Whether to copy the result to clipboard

        Returns:
            The converted Typst equation or an error message
        """
        try:
            # Create the LaTeX content with proper document structure
            latex_content = f"""
            \\documentclass{{article}}
            \\begin{{document}}
            $${latex_equation}$$
            \\end{{document}}
            """

            # Convert using pypandoc
            typst_output = pypandoc.convert_text(
                latex_content, "typst", format="latex", extra_args=["--wrap=none"]
            )

            # Clean up the output and fix bar notation
            typst_equation: str = self.fix_bar_notation(typst_output.strip())
            typst_equation = typst_equation.replace("$", "").strip(" ")

            if copy_to_clipboard and not typst_equation.startswith("Error"):
                pyperclip.copy(typst_equation)
                print("Result copied to clipboard!")
        except Exception as e:
            return f"Error: {e!s}"
        else:
            return typst_equation

    def typst_to_latex(
        self, typst_equation: str, copy_to_clipboard: bool = False
    ) -> str:
        """Convert Typst equation to LaTeX equation using pandoc.

        Args:
            typst_equation: The Typst equation to convert
            copy_to_clipboard: Whether to copy the result to clipboard

        Returns:
            The converted LaTeX equation or an error message
        """
        try:
            # Create the Typst content
            typst_content = f"{typst_equation}"

            # Convert using pypandoc
            latex_output: str = pypandoc.convert_text(
                typst_content, "latex", format="typst", extra_args=["--wrap=none"]
            )

            if copy_to_clipboard and not latex_output.startswith("Error"):
                pyperclip.copy(latex_output)
                print("Result copied to clipboard!")
        except Exception as e:
            return f"Error: {e!s}"
        else:
            return latex_output

    def convert(
        self, equation: str, to_latex: bool = False, copy_to_clipboard: bool = False
    ) -> str:
        """Convert equation between LaTeX and Typst formats.

        Args:
            equation: The equation to convert
            to_latex: If True, converts from Typst to LaTeX. If False, converts from LaTeX to Typst
            copy_to_clipboard: Whether to copy the result to clipboard

        Returns:
            The converted equation or error message
        """
        return (
            self.typst_to_latex(equation, copy_to_clipboard)
            if to_latex
            else self.latex_to_typst(equation, copy_to_clipboard)
        )
