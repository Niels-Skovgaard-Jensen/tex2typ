from tex2typ.__main__ import foo


def test_foo():
    assert foo("foo") == "foo"
