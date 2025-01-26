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
            set theImage to read theFile as JPEG picture
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

    def typst_to_image(
        self, typst_equation: str, save_path: Path | None = None, dpi: int = 300
    ) -> tuple[bool, str]:
        """Convert Typst equation to image and copy to clipboard.

        Args:
            typst_equation: The Typst equation to convert
            save_path: Optional path to save the image to
            dpi: The resolution in dots per inch (default: 300)

        Returns:
            tuple[bool, str]: (success, message)
        """
        try:
            image, error = self.validator.generate_image(typst_equation, dpi=dpi)
            if error:
                return False, f"Error: {error}"

            if image:
                messages = []

                # Copy to clipboard using pbcopy
                if self.copy_to_clipboard(image):
                    messages.append("Image copied to clipboard!")
                else:
                    messages.append("Failed to copy image to clipboard")

                # Save to file if requested
                if save_path:
                    if self.save_to_file(image, save_path):
                        messages.append(f"Image saved to {save_path}")
                    else:
                        messages.append(f"Failed to save image to {save_path}")

                return any("Failed" not in msg for msg in messages), " ".join(messages)
            else:
                return False, "Failed to generate image"
        except Exception as e:
            return False, f"Error: {e!s}"
