"""Friends & Foes Productivity Analyzer.

Reads a daily log of office social activity and reports how helpful friends
and people to avoid relate to projects completed. Correlation, not causation.
"""
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DATA_FILE = Path(__file__).with_name("work_friends_productivity.csv")

REQUIRED_COLUMNS = [
    "Date",
    "Helpful Friends Made",
    "People to Avoid",
    "Projects Completed",
    "Lunch Gossip Sessions",
]


def load_data(path=DATA_FILE):
    """Load the daily log and check that every required column is present."""
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    return df


def correlation(df, column, target="Projects Completed"):
    """Pearson correlation between one column and the target."""
    return df[column].corr(df[target])


def friends_verdict(corr):
    if corr > 0.5:
        return f"✅ Strong finding: More friends = more projects done! Correlation: {corr:.2f}"
    if corr > 0:
        return f"🙂 Slight boost: Friends help a little. Correlation: {corr:.2f}"
    return f"😬 Your friends might be professional time-wasters. Correlation: {corr:.2f}"


def avoid_verdict(corr):
    if corr < 0:
        return f"🚀 Avoiding certain people is a productivity booster! Correlation: {corr:.2f}"
    return (
        "🤔 Avoiding people doesn't seem to help... or maybe you avoided the wrong ones. "
        f"Correlation: {corr:.2f}"
    )


def peak_day(df, column):
    """Date of the day with the highest value in a column (first one on ties)."""
    return df.loc[df[column].idxmax(), "Date"]


def scatter(df, x, path, color):
    plt.figure(figsize=(8, 5))
    plt.scatter(df[x], df["Projects Completed"], color=color)
    plt.title(f"{x} vs Projects Completed")
    plt.xlabel(x)
    plt.ylabel("Projects Completed")
    plt.grid(True)
    plt.savefig(path, dpi=120)
    plt.close()
    return path


def main(data_path=DATA_FILE, out_dir=Path(".")):
    df = load_data(data_path)
    out_dir = Path(out_dir)

    print("=== Welcome to the 'Friends & Foes Productivity Analyzer' ===\n")
    print(f"Analyzing {len(df)} days of office social strategy.\n")

    print(friends_verdict(correlation(df, "Helpful Friends Made")))
    print(avoid_verdict(correlation(df, "People to Avoid")))

    print(f"📅 Best Friend-Making Day: {peak_day(df, 'Helpful Friends Made')}")
    print(f"🚫 Peak Avoidance Day: {peak_day(df, 'People to Avoid')} — minimal meetings recommended.")

    for x, name, color in [
        ("Helpful Friends Made", "friends_vs_projects.png", "green"),
        ("People to Avoid", "avoid_vs_projects.png", "red"),
    ]:
        scatter(df, x, out_dir / name, color)
        print(f"📊 Chart saved: {name}")

    avg_gossip = df["Lunch Gossip Sessions"].mean()
    print(
        f"🍔 On average, there were {avg_gossip:.1f} lunch gossip sessions per day. "
        "Correlation with productivity unverified."
    )


if __name__ == "__main__":
    main()
