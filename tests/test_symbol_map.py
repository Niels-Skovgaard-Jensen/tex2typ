from tex2typ.symbol_map import SYMBOL_MAP


def test_symbol_map():
    assert SYMBOL_MAP["\\alpha"] == "alpha"
    assert SYMBOL_MAP["\\beta"] == "beta"
