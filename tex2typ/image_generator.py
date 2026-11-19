import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from tex2typ.validator import TypstValidator


class ImageGenerator:
    """Class to handle image generation and manipulation for Typst equations."""

    def __init__(self) -> None:
        """Initialize the ImageGenerator with a validator."""
        self.validator = TypstValidator()

    def copy_to_clipboard(self, image: Image.Image) -> bool:
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
            set theImage to read theFile as «class PNGf»
            set the clipboard to theImage
            '''

            result = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True
            )

            # Clean up temporary file
            tmp_path.unlink()
        except Exception:
            return False
        else:
            return result.returncode == 0

    def save_to_file(self, image: Image.Image, output_path: Path) -> bool:
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

    def _save_svg(
        self, typst_equation: str, save_path: Path, transparent: bool
    ) -> tuple[bool, str]:
        """Render the equation as SVG and write it to ``save_path``."""
        svg, error = self.validator.generate_svg(
            typst_equation, transparent=transparent
        )
        if svg is None:
            return False, f"Error: {error}"
        try:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(svg)
        except OSError:
            return False, f"Failed to save SVG to {save_path}"
        return True, f"SVG saved to {save_path}"

    def typst_to_image(
        self,
        typst_equation: str,
        save_path: Path | None = None,
        dpi: int = 300,
        transparent: bool = False,
        copy: bool = True,
    ) -> tuple[bool, str]:
        """Render a Typst equation, copy it to the clipboard and/or save it.

        The output format of ``save_path`` is chosen by its extension
        (``.svg`` for SVG, anything else for PNG).

        Args:
            typst_equation: The Typst equation to convert
            save_path: Optional path to save the image to
            dpi: The resolution in dots per inch for PNG output (default: 300)
            transparent: Render with a transparent background
            copy: Copy a PNG rendering to the clipboard

        Returns:
            tuple[bool, str]: (success, message)
        """
        try:
            messages: list[str] = []
            ok = True
            save_svg = save_path is not None and save_path.suffix.lower() == ".svg"

            if copy or (save_path and not save_svg):
                image, error = self.validator.generate_image(
                    typst_equation, dpi=dpi, transparent=transparent
                )
                if image is None:
                    return False, f"Error: {error}"
                if copy:
                    if self.copy_to_clipboard(image):
                        messages.append("Image copied to clipboard!")
                    else:
                        ok = False
                        messages.append("Failed to copy image to clipboard")
                if save_path and not save_svg:
                    if self.save_to_file(image, save_path):
                        messages.append(f"Image saved to {save_path}")
                    else:
                        ok = False
                        messages.append(f"Failed to save image to {save_path}")

            if save_path and save_svg:
                svg_ok, msg = self._save_svg(typst_equation, save_path, transparent)
                ok = ok and svg_ok
                messages.append(msg)

            return ok, " ".join(messages)
        except Exception as e:
            return False, f"Error: {e!s}"
