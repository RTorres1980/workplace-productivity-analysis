import pandas as pd
import pytest

import analyze_work_friends as awf


@pytest.fixture
def df():
    return pd.DataFrame({
        "Date": ["d1", "d2", "d3", "d4"],
        "Helpful Friends Made": [1, 2, 3, 4],
        "People to Avoid": [4, 3, 2, 1],
        "Projects Completed": [1, 2, 3, 4],
        "Lunch Gossip Sessions": [0, 1, 2, 3],
    })


def test_shipped_data_loads():
    data = awf.load_data()
    assert len(data) == 14
    assert set(awf.REQUIRED_COLUMNS) <= set(data.columns)


def test_missing_column_is_reported(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"Date": ["d1"], "Projects Completed": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Helpful Friends Made"):
        awf.load_data(path)


def test_correlation_signs(df):
    assert awf.correlation(df, "Helpful Friends Made") == pytest.approx(1.0)
    assert awf.correlation(df, "People to Avoid") == pytest.approx(-1.0)


@pytest.mark.parametrize("corr, emoji", [(0.9, "✅"), (0.3, "🙂"), (0.0, "😬"), (-0.4, "😬")])
def test_friends_verdict_thresholds(corr, emoji):
    assert awf.friends_verdict(corr).startswith(emoji)


@pytest.mark.parametrize("corr, emoji", [(-0.2, "🚀"), (0.0, "🤔"), (0.6, "🤔")])
def test_avoid_verdict_thresholds(corr, emoji):
    assert awf.avoid_verdict(corr).startswith(emoji)


def test_peak_day_takes_first_on_ties(df):
    df.loc[1, "People to Avoid"] = 4
    assert awf.peak_day(df, "People to Avoid") == "d1"
    assert awf.peak_day(df, "Helpful Friends Made") == "d4"


def test_main_writes_both_charts(tmp_path, capsys):
    awf.main(out_dir=tmp_path)
    assert (tmp_path / "friends_vs_projects.png").stat().st_size > 0
    assert (tmp_path / "avoid_vs_projects.png").stat().st_size > 0
    assert "Analyzing 14 days" in capsys.readouterr().out
