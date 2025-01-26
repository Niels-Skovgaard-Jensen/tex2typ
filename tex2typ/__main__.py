import argparse
import time
from pathlib import Path

from tex2typ.equation_converter import EquationConverter
from tex2typ.image_generator import ImageGenerator
from tex2typ.validator import TypstValidator


def setup_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Convert equations and generate images",
        prefix_chars="-",
        allow_abbrev=True,
    )
    parser.add_argument("equation", help="Equation to process")
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
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Convert from Typst to LaTeX (default is LaTeX to Typst)",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy converted equation to clipboard",
        default=False,
    )
    return parser


def convert_equation(args: argparse.Namespace) -> str:
    """Convert equation between LaTeX and Typst formats.

    Args:
        args: Parsed command line arguments

    Returns:
        The converted equation or error message
    """
    converter = EquationConverter()
    return converter.convert(
        args.equation, to_latex=args.reverse, copy_to_clipboard=args.copy
    )


def process_image_generation(typst_eq: str, args: argparse.Namespace) -> str:
    """Process image generation request.

    Args:
        typst_eq: The Typst equation to convert to image
        args: Parsed command line arguments

    Returns:
        Status message
    """
    save_path = Path(args.save_image) if args.save_image else None
    image_generator = ImageGenerator()
    success, message = image_generator.typst_to_image(typst_eq, save_path, dpi=args.dpi)
    if not success:
        return message
    return message


def main() -> str:
    """Process equations: convert between LaTeX and Typst, generate images.

    Returns:
        The status message or converted equation.
    """
    parser = setup_argument_parser()
    args = parser.parse_args()

    start_time = time.perf_counter() if args.time else None

    # Convert between formats if no image generation is requested
    if not (args.image or args.save_image):
        result = convert_equation(args)
        if args.time:
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000  # type: ignore[operator]
            print(f"Processing time: {elapsed_ms:.2f} ms")
        return result

    # For image generation, ensure equation is in Typst format
    if not args.reverse:
        converter = EquationConverter()
        typst_eq = converter.latex_to_typst(args.equation)
        if typst_eq.startswith("Error"):
            return typst_eq
    else:
        typst_eq = args.equation

    # Ensure equation is wrapped in math mode
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
        result_message = process_image_generation(typst_eq, args)

    if args.time:
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000  # type: ignore[operator]
        print(f"Processing time: {elapsed_ms:.2f} ms")

    return result_message


if __name__ == "__main__":
    print(main())
