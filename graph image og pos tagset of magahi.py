import matplotlib.pyplot as plt
from collections import Counter

# Your tag frequencies from the NER tagger
tag_freq = {
    "N_NN": 5045, "PSP": 979,  "V_VM": 441,
    "V_VAUX": 270, "CC_CCS": 251, "QT_QTF": 172,
    "RD_ECH": 138, "NNP-PER": 99, "PR_PRP": 84,
}

# Sort by frequency (descending)
tags   = list(tag_freq.keys())
counts = list(tag_freq.values())

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(tags, counts, color="#378ADD", edgecolor="white", linewidth=0.5)

# Add count labels on top of each bar
for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 20,
            str(int(bar.get_height())),
            ha="center", va="bottom", fontsize=9)

ax.set_title("Magahi BIS POS Tag Frequencies", fontsize=14)
ax.set_xlabel("POS Tag")
ax.set_ylabel("Frequency")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.show()