import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Load data
df = pd.read_csv("work_friends_productivity.csv")

print("=== Welcome to the 'Friends & Foes Productivity Analyzer' ===\n")
print(f"Analyzing {len(df)} days of office social strategy.\n")

# Correlation between helpful friends and projects completed
correlation_friends = df["Helpful Friends Made"].corr(df["Projects Completed"])
if correlation_friends > 0.5:
    print(f"✅ Strong finding: More friends = more projects done! Correlation: {correlation_friends:.2f}")
elif correlation_friends > 0:
    print(f"🙂 Slight boost: Friends help a little. Correlation: {correlation_friends:.2f}")
else:
    print(f"😬 Your friends might be professional time-wasters. Correlation: {correlation_friends:.2f}")

# Correlation between avoiding people and productivity
correlation_avoid = df["People to Avoid"].corr(df["Projects Completed"])
if correlation_avoid < 0:
    print(f"🚀 Avoiding certain people is a productivity booster! Correlation: {correlation_avoid:.2f}")
else:
    print(f"🤔 Avoiding people doesn't seem to help... or maybe you avoided the wrong ones. Correlation: {correlation_avoid:.2f}")

# Best friend-making day
best_friend_day = df.loc[df["Helpful Friends Made"].idxmax(), "Date"]
print(f"📅 Best Friend-Making Day: {best_friend_day}")

# Worst "People to Avoid" day
worst_enemy_day = df.loc[df["People to Avoid"].idxmax(), "Date"]
print(f"🚫 Peak Avoidance Day: {worst_enemy_day} — minimal meetings recommended.")

# Plot: Friends vs Projects
plt.figure(figsize=(8,5))
plt.scatter(df["Helpful Friends Made"], df["Projects Completed"], color="green")
plt.title("Helpful Friends Made vs Projects Completed")
plt.xlabel("Helpful Friends Made")
plt.ylabel("Projects Completed")
plt.grid(True)
plt.savefig("friends_vs_projects.png", dpi=120)
plt.close()
print("📊 Chart saved: friends_vs_projects.png")

# Plot: People to Avoid vs Projects
plt.figure(figsize=(8,5))
plt.scatter(df["People to Avoid"], df["Projects Completed"], color="red")
plt.title("People to Avoid vs Projects Completed")
plt.xlabel("People to Avoid")
plt.ylabel("Projects Completed")
plt.grid(True)
plt.savefig("avoid_vs_projects.png", dpi=120)
plt.close()
print("📊 Chart saved: avoid_vs_projects.png")

# Fun fact: Lunch gossip
avg_gossip = df["Lunch Gossip Sessions"].mean()
print(f"🍔 On average, there were {avg_gossip:.1f} lunch gossip sessions per day. Correlation with productivity unverified.")
