import subprocess
import tempfile
from pathlib import Path

from PIL import Image


class TypstValidator:
    """Validates Typst equations by attempting to compile them."""

    def __init__(self) -> None:
        self.template_path = Path(__file__).parent / "templates" / "math_test.typ"
        self.image_template_path = (
            Path(__file__).parent / "templates" / "math_to_image.typ"
        )

    def validate(self, equation: str) -> tuple[bool, str | None]:
        """Validate a Typst equation by attempting to compile it.

        Args:
            equation: The Typst equation to validate

        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
                error_message is None if validation passes
        """
        # Create a temporary file with the equation
        with tempfile.NamedTemporaryFile(
            suffix=".typ", mode="w", delete=False
        ) as tmp_file:
            template_content = self.template_path.read_text()
            # Ensure equation is wrapped in math mode
            math_equation = (
                f"$ {equation} $" if not equation.strip().startswith("$") else equation
            )
            tmp_file.write(template_content.replace("${EQUATION}", math_equation))
            tmp_path = Path(tmp_file.name).resolve()

        try:
            # Try to compile with typst
            result = subprocess.run(
                ["typst", "compile", tmp_path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Clean up temp file
            tmp_path.unlink()

            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr.strip()

        except subprocess.CalledProcessError as e:
            return False, str(e)
        except FileNotFoundError:
            return (
                False,
                "Typst compiler not found. Please install Typst to enable validation.",
            )

    def generate_image(
        self, equation: str, dpi: int = 300
    ) -> tuple[Image.Image | None, str | None]:
        """Generate an image from a Typst equation.

        Args:
            equation: The Typst equation to render
            dpi: The resolution in dots per inch (default: 300)

        Returns:
            tuple[Optional[Image.Image], Optional[str]]: (image, error_message)
                image is None if generation fails
                error_message is None if generation succeeds
        """
        # Create temporary files for the source and output
        with (
            tempfile.NamedTemporaryFile(
                suffix=".typ", mode="w", delete=False
            ) as tmp_source,
            tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_output,
        ):
            template_content = self.image_template_path.read_text()
            # Ensure equation is wrapped in math mode
            math_equation = (
                f"$ {equation} $" if not equation.strip().startswith("$") else equation
            )
            tmp_source.write(template_content.replace("${EQUATION}", math_equation))
            source_path = Path(tmp_source.name).resolve()
            output_path = Path(tmp_output.name).resolve()

        try:
            # Try to compile with typst
            result = subprocess.run(
                ["typst", "compile", "--ppi", str(dpi), source_path, output_path],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                # Load the image
                image = Image.open(output_path)
                # Convert to RGBA to ensure compatibility with clipboard
                image_converted = image.convert("RGBA")
                return image_converted, None
            else:
                return None, result.stderr.strip()

        except subprocess.CalledProcessError as e:
            return None, str(e)
        except FileNotFoundError:
            return (
                None,
                "Typst compiler not found. Please install Typst to enable image generation.",
            )
        finally:
            # Clean up temporary files
            source_path.unlink()
            output_path.unlink()
