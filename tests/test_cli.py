from unittest.mock import patch

import pytest

from tex2typ.__main__ import main


def test_bar_notation():
    latex_eq = "\\bar{x}"
    result = main(latex_eq)
    assert "overline" in result


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
def test_cli_argument_parsing(cli_args, expected_calls):
    with (
        patch("argparse.ArgumentParser.parse_args") as mock_args,
        patch("tex2typ.__main__.latex_to_typst") as mock_l2t,
        patch("tex2typ.__main__.typst_to_latex") as mock_t2l,
        patch("pyperclip.copy") as mock_copy,
    ):
        # Configure the mock arguments
        mock_args.return_value = type("Args", (), expected_calls)

        # Run the main function
        main()

        # Verify the correct conversion function was called
        if expected_calls["reverse"]:
            mock_t2l.assert_called_once_with(expected_calls["equation"])
        else:
            mock_l2t.assert_called_once_with(expected_calls["equation"])

        # Verify clipboard usage
        if expected_calls["copy"]:
            assert mock_copy.called
        else:
            assert not mock_copy.called
