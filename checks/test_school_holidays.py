"""Check C14: the school holiday calendar (data/school_holidays_sh.csv) is consistent.

- structure: dates parse, start <= end, periods do not overlap, the calendar covers 2013-2019
- plausibility: summer holidays last 5-7 weeks in every year 2013-2019
- consistency with the public-holiday calendar (holidays package, SH):
  Easter holidays contain Good Friday and Easter Monday, Christmas holidays contain 25/26 Dec,
  the single Pfingsten day is the Friday after Ascension Day.
"""

from pathlib import Path

import holidays
import pandas as pd
import pytest

CSV = Path(__file__).resolve().parents[1] / "data" / "school_holidays_sh.csv"


@pytest.fixture(scope="module")
def sh():
    return pd.read_csv(CSV, parse_dates=["start", "end"])


@pytest.fixture(scope="module")
def public():
    return holidays.Germany(subdiv="SH", years=range(2012, 2021))


def test_structure(sh):
    assert list(sh.columns) == ["name", "start", "end", "school_year", "source"]
    assert sh.notna().all().all()
    assert (sh.start <= sh.end).all()
    s = sh.sort_values("start")
    assert (s.start.iloc[1:].values > s.end.iloc[:-1].values).all(), "periods overlap"


def test_covers_2013_to_2019(sh):
    # every period overlaps 2013-2019; only the edge periods may reach into Dec 2012 / Jan 2020
    assert (sh.end >= "2013-01-01").all() and (sh.start <= "2019-12-31").all()
    assert sh.start.min() >= pd.Timestamp("2012-12-01")
    assert sh.end.max() <= pd.Timestamp("2020-01-31")
    for year in range(2013, 2020):
        names = set(sh[sh.start.dt.year == year].name)
        assert {"Osterferien", "Sommerferien", "Herbstferien"} <= names, year


def test_summer_holidays_5_to_7_weeks(sh):
    summer = sh[sh.name == "Sommerferien"]
    assert sorted(summer.start.dt.year) == list(range(2013, 2020))
    days = (summer.end - summer.start).dt.days + 1
    assert days.between(35, 49).all(), days.tolist()


def test_consistent_with_public_holidays(sh, public):
    def day_off(d):
        return d.dayofweek >= 5 or d in public

    def in_period(name, date):
        # inside the period, or directly attached to it with only weekends / public holidays
        # in between (e.g. 2019: Easter holidays end Thu 18 Apr, Good Friday is 19 Apr)
        for p in sh[sh.name == name].itertuples():
            if p.start <= date <= p.end:
                return True
            gap_after = pd.date_range(p.end + pd.Timedelta(days=1), date - pd.Timedelta(days=1))
            gap_before = pd.date_range(date + pd.Timedelta(days=1), p.start - pd.Timedelta(days=1))
            if date > p.end and all(day_off(d) for d in gap_after) and len(gap_after) <= 4:
                return True
            if date < p.start and all(day_off(d) for d in gap_before) and len(gap_before) <= 4:
                return True
        return False

    for date, hname in public.items():
        date = pd.Timestamp(date)
        if not pd.Timestamp("2013-01-01") <= date <= pd.Timestamp("2019-12-31"):
            continue
        if hname in ("Karfreitag", "Ostermontag"):
            assert in_period("Osterferien", date), (date, hname)
        if hname in ("Erster Weihnachtstag", "Zweiter Weihnachtstag"):
            assert in_period("Weihnachtsferien", date), (date, hname)
        if hname == "Christi Himmelfahrt":
            assert in_period("Pfingstferien", date + pd.Timedelta(days=1)), (date, hname)
