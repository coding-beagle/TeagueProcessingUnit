import pytest
from TeagueASM.parsing import resolve_macros_and_tags

testdata = [
    (
        [
            "IMM ${22+1}",
            "IMM ${69+31}",
            "IMM ${22-11}",
        ],
        ["IMM 23", "IMM 100", "IMM 11"],
        True,
        "",
    ),
    (
        ["CP 00 00", "#A tag#IMM 1023", "JMP 'A tag'"],
        ["CP 00 00", "IMM 1023", "JMP -1"],
        True,
        "",
    ),
    (
        ["CP 00 00", "#A tag#CP 11 23", "IMM ${42 + 32}", "JMP 'A tag'"],
        ["CP 00 00", "CP 11 23", "IMM 74", "JMP -2"],
        True,
        "",
    ),
    (
        [
            "CP 00 00",
            "CP 11 23",
            "IMM ${60 + 32}",
            "JMP 'A tag'",
            "NOOP",
            "NOOP",
            "#A tag#NOOP",
        ],
        ["CP 00 00", "CP 11 23", "IMM 92", "JMP 3", "NOOP", "NOOP", "NOOP"],
        True,
        "",
    ),
    (
        ["CP 00 00", "#A tag#CP 11 23", "IMM ${42 + 32}", "JMP 'Somewhere not found'"],
        [],
        False,
        "Unresolved tag",
    ),
]


@pytest.mark.parametrize(
    ("test_code", "expected", "should_pass", "exception_contains"), testdata
)
def test_parsing(
    test_code: list[str],
    expected: bool,
    should_pass: bool,
    exception_contains: str,
):
    if should_pass:
        assert resolve_macros_and_tags(test_code) == expected
    else:
        with pytest.raises(Exception) as exc_info:
            resolve_macros_and_tags(test_code)
        assert exception_contains in str(exc_info.value)  # type: ignore
