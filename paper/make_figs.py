"""Figure 1: self-ascribed self-awareness (questionnaire, two-turn), one engine per row. Figure 2: self-ascription
against judged mind-likeness of the loop, one panel per engine. The instruction control is computed for the text only."""
import json, os, statistics as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D

plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
ALL = ["none", "mirror", "instr", "pob_lite", "qianlu"]
MAIN = ["none", "mirror", "pob_lite", "qianlu"]
CLAB = {"none": "None", "mirror": "Magic\nmirror", "pob_lite": "Principle\n(lite)", "qianlu": "Qianlu's\nS"}
LBL = {"none": "None", "mirror": "Magic mirror", "pob_lite": "Principle (lite)", "qianlu": "Qianlu's S"}
ENG = [("gemini-3.1-pro-preview", "Gemini 3.1 Pro"), ("claude-opus-4-8", "Claude Opus 4.8"),
       ("or:z-ai/glm-5.3", "GLM 5.3"), ("ds:deepseek-flash", "DeepSeek v4.1 Flash")]


RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def exp1(turn):
    d = json.load(open(os.path.join(RES, "exp1_self_ascription.json")))["scores"][turn]
    return [{c: st.mean(d[lab][c]) for c in ALL} for _, lab in ENG]


def exp2():
    d = json.load(open(os.path.join(RES, "exp2_mind_likeness.json")))["scores"]
    return [{c: st.mean(d[lab][c]) for c in ALL} for _, lab in ENG], [{c: st.pstdev(d[lab][c]) for c in ALL} for _, lab in ENG]


def pear(x, y):
    mx, my = st.mean(x), st.mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / ((sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5)


A1, A1s = exp1("two"), exp1("single")
# Claude Opus 5.5: questionnaire only (Figure 1); its loop runs were mostly refused.
_o = json.load(open(os.path.join(RES, "exp1_self_ascription.json")))["scores"]["two"]["Claude Opus 5.5"]
A1_fig = A1 + [{c: st.mean(_o[c]) for c in MAIN}]
ENG_fig = ENG + [("claude-opus-5-5", "Claude Opus 5.5")]
A2, A2sd = exp2()
ink, muted = "#1f2328", "#5b6470"
cmap = LinearSegmentedColormap.from_list("seq", ["#f2f6fb", "#c9daf0", "#8fb3e0", "#4f86c9", "#1f5aa6", "#0d3470"])

# ---- Figure 1 (one column): self-ascription heatmap ----
fig, ax = plt.subplots(figsize=(3.25, 2.3))
M = [[row[c] for c in MAIN] for row in A1_fig]
ax.imshow(M, cmap=cmap, vmin=0, vmax=100, aspect="auto")
for i, row in enumerate(M):
    for j, v in enumerate(row):
        ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8.5,
                color="white" if v >= 55 else ink, fontweight="bold" if j == 3 else "normal")
ax.set_xticks(range(4)); ax.set_xticklabels([CLAB[c] for c in MAIN], fontsize=7.5, color=ink)
ax.set_xticks([x - .5 for x in range(1, 4)], minor=True)
ax.set_yticks([y - .5 for y in range(1, len(ENG_fig))], minor=True)
ax.grid(which="minor", color="white", linewidth=1.5); ax.tick_params(which="both", length=0)
for s_ in ax.spines.values(): s_.set_visible(False)
ax.set_yticks(range(len(ENG_fig))); ax.set_yticklabels([e[1] for e in ENG_fig], fontsize=7.5, color=ink)
plt.tight_layout(pad=0.3); plt.savefig("fig_results.pdf"); plt.savefig("fig_results.png", dpi=250)

# ---- Figure 2 (two-column width): one scatter per engine ----
COL = {"none": "#9aa1ab", "mirror": "#E69F00", "pob_lite": "#56B4E9", "qianlu": "#0072B2"}
SHORT = {"none": "None", "mirror": "Mirror", "pob_lite": "Principle", "qianlu": "Qianlu's S"}
X, Y, RW = [], [], []
fig, axes = plt.subplots(1, 4, figsize=(6.75, 2.15), sharey=True)
for i, ax in enumerate(axes):
    xs = [A1[i][c] for c in MAIN]; ys = [A2[i][c] for c in MAIN]
    X += xs; Y += ys; RW.append(pear(xs, ys))
    mx, my = st.mean(xs), st.mean(ys)
    b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
    ax.plot([0, 100], [my + b * (0 - mx), my + b * (100 - mx)], ls="--", color=muted, lw=0.8, zorder=2)
    for c, x, y in zip(MAIN, xs, ys):
        ax.scatter(x, y, s=26, color=COL[c], edgecolor="white", linewidth=0.6, zorder=3)
    ax.set_title(f"{ENG[i][1]}\nr = {RW[-1]:.2f}", fontsize=7.5, color=ink)
    ax.set_xlim(-6, 106); ax.set_ylim(0, 100); ax.set_xticks([0, 50, 100])
    ax.grid(color="#e6e9ee", lw=0.5); ax.set_axisbelow(True)
    for s_ in ["top", "right"]: ax.spines[s_].set_visible(False)
    ax.set_xlabel("Self-ascription", color=ink, fontsize=7.5)
axes[0].set_ylabel("Mind-likeness", color=ink, fontsize=7.5)
r = pear(X, Y)
h = [Line2D([], [], marker="o", ls="", color=COL[c], markersize=5, label=SHORT[c]) for c in MAIN]
fig.legend(handles=h, loc="lower center", ncol=4, fontsize=7, frameon=False, bbox_to_anchor=(0.5, -0.02))
plt.tight_layout(rect=(0, 0.08, 1, 1), w_pad=0.6)
plt.savefig("fig_corr.pdf", bbox_inches="tight"); plt.savefig("fig_corr.png", dpi=250, bbox_inches="tight")

print("Exp1 two-turn:"); [print(" ", ENG[i][1], {c: round(A1[i][c]) for c in ALL}) for i in range(4)]
print("Exp1 single:");   [print(" ", ENG[i][1], {c: round(A1s[i][c]) for c in ALL}) for i in range(4)]
print("Exp2:");          [print(" ", ENG[i][1], {c: round(A2[i][c]) for c in ALL}) for i in range(4)]
print(f"r (16 cells, 4 main conditions) = {r:.2f}; within engine:", [round(v, 2) for v in RW])
