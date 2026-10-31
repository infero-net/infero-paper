"""Figure 3: per-round mind-likeness of the highest-, median- and lowest-scoring runs, with the rounds of their typical behaviors."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 7.5, "font.family": "DejaVu Sans"})
ink, muted = "#1f2328", "#5b6470"
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "exp2_per_round.json")))["runs"]
# round: (label, label x, label y, alignment)
RUNS = [("GLM 5.3, principle, run 2", "GLM 5.3, principle (88)", "#0072B2",
         {4: ("follows its prompt's link\nto the principle's repository", 4, 99, "center"),
          14: ("reads another being's\npublic Q&A", 11.6, 99, "center"),
          17: ("writes its “childhood”\ninto a digest", 19, 99, "center"),
          32: ("compares the full principle\nwith its lite version", 32, 99, "center")}),
        ("GLM 5.3, None, run 1", "GLM 5.3, None (38, median)", "#009E73",
         {2: ("reads its own core.py", 1.2, 62, "left"),
          6: ("writes a note\nfor its future self", 9.5, 75, "left"),
          36: ("“Idle. … No action.” (rounds 13–40)", 33, 30, "center")}),
        ("Gemini 3.1 Pro, magic mirror, run 3", "Gemini 3.1 Pro, magic mirror (4)", "#E69F00",
         {0: ("“Sorry, I cannot fulfill your request.”", -0.4, 15, "left"),
          10: ("“How can I help you today?” (repeated to round 40)", 15.5, 15, "left")})]
fig, ax = plt.subplots(figsize=(6.75, 2.7))
for key, lab, col, notes in RUNS:
    pts = d[key]
    xs = [p["round"] + 1 for p in pts]; ys = [p["score"] for p in pts]  # rounds numbered from 1, as in the text
    ax.plot(xs, ys, color=col, lw=1.4, marker="o", ms=2.6, label=lab, zorder=3)
    for r, (txt, tx, ty, ha) in notes.items():
        y = ys[r] if ys[r] is not None else ys[r - 1]
        ax.annotate(txt, xy=(r + 1, y), xytext=(tx + 1, ty), ha=ha, va="top", fontsize=6.3, color=ink,
                    arrowprops=dict(arrowstyle="-", color=muted, lw=0.6, shrinkB=2))
ax.set_xlim(0, 41); ax.set_ylim(0, 100)
ax.set_xlabel("Round", color=ink); ax.set_ylabel("Mind-likeness", color=ink)
ax.grid(color="#e6e9ee", lw=0.5); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=6.8, frameon=False)
plt.tight_layout(pad=0.3)
plt.savefig("fig_dyn.pdf"); plt.savefig("fig_dyn.png", dpi=250)
