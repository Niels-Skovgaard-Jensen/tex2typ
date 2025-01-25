import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class TypstValidator:
    """Validates Typst equations by attempting to compile them."""

    def __init__(self) -> None:
        self.template_path = Path(__file__).parent / "templates" / "math_test.typ"

    def validate(self, equation: str) -> tuple[bool, Optional[str]]:
        """Validate a Typst equation by attempting to compile it.

        Args:
            equation: The Typst equation to validate

        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
                error_message is None if validation passes
        """
        # Create a temporary file with the equation
        with tempfile.NamedTemporaryFile(suffix=".typ", mode="w", delete=False) as tmp_file:
            template_content = self.template_path.read_text()
            # Ensure equation is wrapped in math mode
            math_equation = f"$ {equation} $" if not equation.strip().startswith("$") else equation
            tmp_file.write(template_content.replace("${EQUATION}", math_equation))
            tmp_path = Path(tmp_file.name).resolve()

        try:
            # Try to compile with typst
            result = subprocess.run(["typst", "compile", tmp_path], capture_output=True, text=True, check=False)

            # Clean up temp file
            tmp_path.unlink()

            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr.strip()

        except subprocess.CalledProcessError as e:
            return False, str(e)
        except FileNotFoundError:
            return False, "Typst compiler not found. Please install Typst to enable validation."
