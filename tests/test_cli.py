from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tex2typ.__main__ import main
from tex2typ.equation_converter import EquationConverter


def test_bar_notation():
    """Test that bar notation is correctly converted."""
    converter = EquationConverter()
    latex_eq = r"\bar{x}"
    result = converter.latex_to_typst(latex_eq)
    # Different Pandoc versions may produce different output
    assert "overline" in result or "macron" in result


@pytest.mark.parametrize(
    "cli_args,expected_calls",
    [
        (
            ["tex2typ", "x^2"],
            {"equation": "x^2", "copy": False, "reverse": False, "time": False},
        ),
        (
            ["tex2typ", "x^2", "-c"],
            {"equation": "x^2", "copy": True, "reverse": False, "time": False},
        ),
        (
            ["tex2typ", "x^2", "-r"],
            {"equation": "x^2", "copy": False, "reverse": True, "time": False},
        ),
    ],
)
def test_cli_argument_parsing(cli_args, expected_calls, monkeypatch):
    """Test CLI argument parsing and corresponding function calls."""
    with patch("sys.argv", cli_args):
        # Create a mock converter
        mock_converter = MagicMock()
        mock_converter.convert.return_value = "converted_equation"

        # Create a mock converter class
        mock_converter_class = MagicMock(return_value=mock_converter)

        # Patch the EquationConverter class where it's imported
        with patch("tex2typ.__main__.EquationConverter", mock_converter_class):
            # Run the main function
            result = main()

            # Verify the converter was called with correct arguments
            mock_converter.convert.assert_called_once_with(
                expected_calls["equation"],
                to_latex=expected_calls["reverse"],
                copy_to_clipboard=expected_calls["copy"],
            )

            assert result == "converted_equation"


def test_image_generation():
    """Test image generation functionality."""
    cli_args = ["tex2typ", "x^2", "-i", "-s", "test.png"]
    with patch("sys.argv", cli_args):
        # Create mock converter
        mock_converter = MagicMock()
        mock_converter.latex_to_typst.return_value = "converted_equation"
        mock_converter_class = MagicMock(return_value=mock_converter)

        # Create mock image generator
        mock_img_gen = MagicMock()
        mock_img_gen.typst_to_image.return_value = (
            True,
            "Image generated successfully",
        )
        mock_img_gen_class = MagicMock(return_value=mock_img_gen)

        # Patch both classes where they're imported
        with (
            patch("tex2typ.__main__.EquationConverter", mock_converter_class),
            patch("tex2typ.__main__.ImageGenerator", mock_img_gen_class),
        ):
            # Run the main function
            result = main()

            # Verify the conversion and image generation were called
            mock_converter.latex_to_typst.assert_called_once_with("x^2")
            mock_img_gen.typst_to_image.assert_called_once_with(
                "$ converted_equation $", Path("test.png"), dpi=300
            )
            assert result == "Image generated successfully"
