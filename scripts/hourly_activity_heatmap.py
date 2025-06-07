import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import defaultdict

# Load chat file
file_path = "WhatsApp Chat with BCC.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Regex with support for U+202F (narrow space) before AM/PM
timestamp_msg_pattern = re.compile(
    r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}):(\d{2})[\u202f ]?([APap][Mm]) - (.*?):'
)

# Initialize hourly activity tracker
hourly_activity = defaultdict(lambda: [0]*24)

# Parse lines
for line in lines:
    match = timestamp_msg_pattern.match(line)
    if match:
        date_str, hour, minute, am_pm, sender = match.groups()
        hour = int(hour)
        if am_pm.lower() == 'pm' and hour != 12:
            hour += 12
        elif am_pm.lower() == 'am' and hour == 12:
            hour = 0
        hourly_activity[sender][hour] += 1

# Keep only users with messages
hourly_filtered = {sender: counts for sender, counts in hourly_activity.items() if sum(counts) > 0}

if hourly_filtered:
    df_hours = pd.DataFrame.from_dict(hourly_filtered, orient='index')

    if df_hours.shape[1] == 24:
        df_hours.columns = [f"{h:02d}:00" for h in range(24)]

        # Sort by total messages
        df_hours["Total"] = df_hours.sum(axis=1)
        df_hours = df_hours.sort_values("Total", ascending=False).drop(columns="Total")

        # ✅ Show table
        display(df_hours)

        # ✅ Plot heatmap
        plt.figure(figsize=(16, 8))
        sns.heatmap(df_hours, cmap="YlGnBu", linewidths=0.3, linecolor='gray')
        plt.title("Hourly WhatsApp Activity BCC MEMBERS", fontsize=16)
        plt.xlabel("Hour of Day", fontsize=12)
        plt.ylabel("Sender", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ The data does not contain 24 hourly slots.")
else:
    print("⚠️ No valid hourly activity data was found.")