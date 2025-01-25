import argparse
import re
import subprocess
import tempfile
import time
from pathlib import Path

import pypandoc  # type: ignore[import-untyped]
from PIL import Image

from tex2typ.validator import TypstValidator


def fix_bar_notation(typst_eq: str) -> str:
    """Replace x^(‾) with #bar(x) in Typst equations."""
    # Pattern matches any character followed by ^(‾)
    pattern = r"(\w+)\^\(‾\)"
    return re.sub(pattern, r"overline(\1)", typst_eq)


def latex_to_typst(latex_equation: str) -> str:
    """Convert LaTeX equation to Typst equation using pandoc.

    Args:
        latex_equation: The LaTeX equation to convert

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
        typst_output = pypandoc.convert_text(latex_content, "typst", format="latex", extra_args=["--wrap=none"])

        # Clean up the output and fix bar notation
        typst_equation: str = fix_bar_notation(typst_output.strip())
        typst_equation = typst_equation.replace("$", "").strip(" ")
    except Exception as e:
        return f"Error: {e!s}"
    else:
        return typst_equation


def typst_to_latex(typst_equation: str) -> str:
    """Convert Typst equation to LaTeX equation using pandoc.

    Args:
        typst_equation: The Typst equation to convert

    Returns:
        The converted LaTeX equation or an error message
    """
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


def copy_image_to_clipboard(image: Image.Image) -> bool:
    """Copy image to clipboard using osascript on macOS.

    Args:
        image: The PIL Image to copy

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create a temporary file to store the image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            image.save(tmp_file, format="PNG")
            tmp_path = Path(tmp_file.name)

        # AppleScript to copy image to clipboard
        script = f'''
        set theFile to POSIX file "{tmp_path}"
        set theImage to read theFile as JPEG picture
        set the clipboard to theImage
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

        # Clean up temporary file
        tmp_path.unlink()
    except Exception:
        return False
    else:
        return result.returncode == 0


def save_image_to_file(image: Image.Image, output_path: Path) -> bool:
    """Save image to file.

    Args:
        image: The PIL Image to save
        output_path: Path to save the image to

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")
    except Exception:
        return False
    else:
        return True


def typst_to_image(typst_equation: str, save_path: Path | None = None, dpi: int = 300) -> tuple[bool, str]:
    """Convert Typst equation to image and copy to clipboard.

    Args:
        typst_equation: The Typst equation to convert
        save_path: Optional path to save the image to
        dpi: The resolution in dots per inch (default: 300)

    Returns:
        tuple[bool, str]: (success, message)
    """
    try:
        validator = TypstValidator()
        image, error = validator.generate_image(typst_equation, dpi=dpi)
        if error:
            return False, f"Error: {error}"

        if image:
            messages = []

            # Copy to clipboard using pbcopy
            if copy_image_to_clipboard(image):
                messages.append("Image copied to clipboard!")
            else:
                messages.append("Failed to copy image to clipboard")

            # Save to file if requested
            if save_path:
                if save_image_to_file(image, save_path):
                    messages.append(f"Image saved to {save_path}")
                else:
                    messages.append(f"Failed to save image to {save_path}")

            return any("Failed" not in msg for msg in messages), " ".join(messages)
        else:
            return False, "Failed to generate image"
    except Exception as e:
        return False, f"Error: {e!s}"


def main() -> str:
    """Process Typst equations and generate images.

    Returns:
        The status message.
    """
    parser = argparse.ArgumentParser(
        description="Generate images from Typst equations",
        prefix_chars="-",
        allow_abbrev=True,
    )
    parser.add_argument("equation", help="Typst equation to process")
    parser.add_argument(
        "-t",
        "--time",
        action="store_true",
        help="Display processing time in milliseconds",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--validate",
        action="store_true",
        help="Validate the Typst equation compiles",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--image",
        action="store_true",
        help="Generate and copy image to clipboard",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--save-image",
        type=str,
        help="Save the generated image to the specified path",
        default=None,
    )
    parser.add_argument(
        "--dpi",
        type=int,
        help="Image resolution in dots per inch (default: 300)",
        default=300,
    )
    args = parser.parse_args()

    start_time = time.perf_counter() if args.time else None

    # Ensure equation is wrapped in math mode
    typst_eq = args.equation
    if not typst_eq.strip().startswith("$"):
        typst_eq = f"$ {typst_eq} $"

    if args.validate:
        validator = TypstValidator()
        is_valid, error = validator.validate(typst_eq)
        if not is_valid:
            return f"Error: {error}"
        return "Equation is valid"

    result_message = "Equation processed successfully"
    if args.image or args.save_image:
        save_path = Path(args.save_image) if args.save_image else None
        success, message = typst_to_image(typst_eq, save_path, dpi=args.dpi)
        result_message = message
        if not success:
            return message

    if args.time:
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000  # type: ignore[operator]
        print(f"Processing time: {elapsed_ms:.2f} ms")

    return result_message


if __name__ == "__main__":
    print(main())
