import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import defaultdict

# Load the chat file
file_path = "WhatsApp Chat with BCC.txt"  # Update path if needed
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Initialize message counters
msg_data = defaultdict(lambda: {
    "Text": 0,
    "Media": 0,
    "Sticker_Emoji": 0,
    "Audio": 0,
    "Video": 0,
    "Reaction": 0
})

# Regex for emojis
emoji_pattern = re.compile(
    r'[\U0001F600-\U0001F64F'  # emoticons
    r'\U0001F300-\U0001F5FF'  # symbols & pictographs
    r'\U0001F680-\U0001F6FF'  # transport & map symbols
    r'\U0001F1E0-\U0001F1FF]+',  # flags
    flags=re.UNICODE
)

reaction_phrases = ["this message was deleted", "you reacted", "reacted to"]
media_tag = "<media omitted>"

# Parse lines
for line in lines:
    if " - " in line:
        try:
            _, content = line.split(" - ", 1)
            if ": " in content:
                sender, msg = content.split(": ", 1)
                sender = sender.strip()
                msg = msg.strip().lower()

                if any(r in msg for r in reaction_phrases):
                    msg_data[sender]["Reaction"] += 1
                elif media_tag in msg:
                    msg_data[sender]["Media"] += 1
                elif "audio" in msg:
                    msg_data[sender]["Audio"] += 1
                elif "video" in msg:
                    msg_data[sender]["Video"] += 1
                elif emoji_pattern.search(msg):
                    msg_data[sender]["Sticker_Emoji"] += 1
                else:
                    msg_data[sender]["Text"] += 1
        except ValueError:
            continue

# Convert to DataFrame
df = pd.DataFrame(msg_data).T.fillna(0).astype(int).reset_index().rename(columns={"index": "Sender"})

# ✅ Filter only real group members
valid_members = [
    'Rammoorthy', 'Guru Manoj', 'Mukeshthenraj 🏎️', 'Bala', 'Motta Abishiek', 'Tamilselvan',
    'Vella Abisheik', 'Jothikailash', 'Santhanam', 'Godwin', 'Sudharson', 'Shaju', 'Sanjeevi',
    'Prem Wapp', 'Sridhar', 'Hanifa', 'Nirmal', 'Najibullah', 'David Prakash',
    '+91 88383 51415', 'Prem', 'Manoj Army', 'Meta AI'
]
df = df[df["Sender"].isin(valid_members)]

# Melt for barplot
df_melt = df.melt(id_vars=["Sender"], var_name="Message Type", value_name="Count")

# ✅ Plotting with enhanced visibility
plt.figure(figsize=(18, 8))
sns.set_style("whitegrid")
sns.barplot(data=df_melt, x="Sender", y="Count", hue="Message Type")

plt.title("WhatsApp Message Types by Sender", fontsize=18, weight='bold')
plt.xlabel("Sender", fontsize=14)
plt.ylabel("Message Count", fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title="Message Type", title_fontsize=13, fontsize=11, loc="upper right")
plt.tight_layout()
plt.show()