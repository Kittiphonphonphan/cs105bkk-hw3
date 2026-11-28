"""Part 10: your own tests for parse_walk. The README says what to write here.

We grade this file by running it against a correct walks.py, where every test must pass,
and against versions of walks.py with a bug planted in parse_walk, where your tests should fail.
"""

import pytest

from walks import Walk, parse_walk


@pytest.fixture
def good_row() -> dict[str, str]:
    """Provided: one good row, as csv.DictReader gives it. Each test gets its own new copy."""
    return {"date": "2026-11-16", "steps": "4200", "place": "Lumphini Park"}


def test_core_example_a_good_row_becomes_a_walk(good_row):
    """Provided: an example that uses the fixture. Write your own tests below it."""
    assert parse_walk(good_row) == Walk("2026-11-16", 4200, "Lumphini Park")


# Your tests go here.


def test_parse_walk_strips_whitespace_and_does_not_mutate_row(good_row):
    good_row["date"] = "  2026-11-16 \t"
    good_row["steps"] = "  3100 \n"
    good_row["place"] = "  campus  "
    original = dict(good_row)

    walk = parse_walk(good_row)

    assert walk == Walk(date="2026-11-16", steps=3100, place="campus")
    assert good_row == original


def test_parse_walk_accepts_zero_steps(good_row):
    good_row["steps"] = "0"
    assert parse_walk(good_row) == Walk("2026-11-16", 0, "Lumphini Park")


def test_parse_walk_accepts_empty_place(good_row):
    good_row["place"] = "   "
    assert parse_walk(good_row) == Walk("2026-11-16", 4200, "")


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("date", ""),
        ("date", "   \t\n "),
        ("steps", ""),
        ("steps", "   "),
        ("steps", "abc"),
        ("steps", "12.5"),
        ("steps", "10.0"),
        ("steps", "-1"),
        ("steps", "-300"),
    ],
)
def test_parse_walk_raises_value_error_on_bad_rows(good_row, field, bad_value):
    good_row[field] = bad_value
    with pytest.raises(ValueError):
        parse_walk(good_row)