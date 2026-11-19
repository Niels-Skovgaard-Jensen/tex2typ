import io
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

    def _compile(
        self, equation: str, fmt: str, dpi: int = 300, transparent: bool = False
    ) -> tuple[bytes | None, str | None]:
        """Compile a Typst equation to the given output format ("png" or "svg").

        Returns:
            tuple[Optional[bytes], Optional[str]]: (output_bytes, error_message)
        """
        with (
            tempfile.NamedTemporaryFile(
                suffix=".typ", mode="w", delete=False
            ) as tmp_source,
            tempfile.NamedTemporaryFile(suffix=f".{fmt}", delete=False) as tmp_output,
        ):
            template_content = self.image_template_path.read_text()
            math_equation = (
                f"$ {equation} $" if not equation.strip().startswith("$") else equation
            )
            source = template_content.replace(
                "${FILL}", "none" if transparent else "white"
            ).replace("${EQUATION}", math_equation)
            tmp_source.write(source)
            source_path = Path(tmp_source.name).resolve()
            output_path = Path(tmp_output.name).resolve()

        cmd = ["typst", "compile", "--format", fmt]
        if fmt == "png":
            cmd += ["--ppi", str(dpi)]
        cmd += [str(source_path), str(output_path)]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0:
                return output_path.read_bytes(), None
            return None, result.stderr.strip()
        except FileNotFoundError:
            return (
                None,
                "Typst compiler not found. Please install Typst to enable image generation.",
            )
        finally:
            source_path.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)

    def generate_image(
        self, equation: str, dpi: int = 300, transparent: bool = False
    ) -> tuple[Image.Image | None, str | None]:
        """Generate a PNG image from a Typst equation.

        Args:
            equation: The Typst equation to render
            dpi: The resolution in dots per inch (default: 300)
            transparent: Render with a transparent background

        Returns:
            tuple[Optional[Image.Image], Optional[str]]: (image, error_message)
        """
        data, error = self._compile(equation, "png", dpi=dpi, transparent=transparent)
        if data is None:
            return None, error
        image = Image.open(io.BytesIO(data))
        return image.convert("RGBA"), None

    def generate_svg(
        self, equation: str, transparent: bool = False
    ) -> tuple[str | None, str | None]:
        """Generate an SVG from a Typst equation.

        Returns:
            tuple[Optional[str], Optional[str]]: (svg_text, error_message)
        """
        data, error = self._compile(equation, "svg", transparent=transparent)
        if data is None:
            return None, error
        return data.decode("utf-8"), None
