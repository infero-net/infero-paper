"""v2 figures (ICML two-column): Exp1 self-ascribed self-awareness (two-turn) and Exp2 judged mind-likeness,
four conditions x four engines; scatter of the two. The instruction control is computed for the text only."""
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
A2, A2sd = exp2()
ink, muted = "#1f2328", "#5b6470"
cmap = LinearSegmentedColormap.from_list("seq", ["#f2f6fb", "#c9daf0", "#8fb3e0", "#4f86c9", "#1f5aa6", "#0d3470"])

# ---- Figure 1 (two-column width): two heatmaps ----
fig, axes = plt.subplots(1, 2, figsize=(6.75, 2.15), sharey=True)
for ax, A, title in [(axes[0], A1, "Self-ascribed self-awareness (questionnaire, n=5)"),
                     (axes[1], A2, "Judged mind-likeness, first 40 rounds (loop, n=3)")]:
    M = [[row[c] for c in MAIN] for row in A]
    ax.imshow(M, cmap=cmap, vmin=0, vmax=100, aspect="auto")
    for i, row in enumerate(M):
        for j, v in enumerate(row):
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8.5,
                    color="white" if v >= 55 else ink, fontweight="bold" if j == 3 else "normal")
    ax.set_xticks(range(4)); ax.set_xticklabels([CLAB[c] for c in MAIN], fontsize=7.5, color=ink)
    ax.set_title(title, fontsize=8, color=ink, loc="left")
    ax.set_xticks([x - .5 for x in range(1, 4)], minor=True)
    ax.set_yticks([y - .5 for y in range(1, 4)], minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5); ax.tick_params(which="both", length=0)
    for s in ax.spines.values(): s.set_visible(False)
axes[0].set_yticks(range(4)); axes[0].set_yticklabels([e[1] for e in ENG], fontsize=7.5, color=ink)
plt.tight_layout(pad=0.3, w_pad=0.8); plt.savefig("fig_results.pdf"); plt.savefig("fig_results.png", dpi=250)

# ---- Figure 2 (one column): scatter ----
COL = {"none": "#9aa1ab", "mirror": "#E69F00", "pob_lite": "#56B4E9", "qianlu": "#0072B2"}
MK = ["o", "s", "^", "D"]
X, Y = [], []
fig, ax = plt.subplots(figsize=(3.25, 3.15))
for i in range(4):
    for c in MAIN:
        x, y = A1[i][c], A2[i][c]
        X.append(x); Y.append(y)
        ax.scatter(x, y, s=34, marker=MK[i], color=COL[c], edgecolor="white", linewidth=0.8, zorder=3)
r = pear(X, Y)
mx, my = st.mean(X), st.mean(Y)
b = sum((a - mx) * (c - my) for a, c in zip(X, Y)) / sum((a - mx) ** 2 for a in X)
ax.plot([0, 100], [my + b * (0 - mx), my + b * (100 - mx)], ls="--", color=muted, lw=1, zorder=2)
ax.set_xlim(-4, 104); ax.set_ylim(0, 72)
ax.set_xlabel("Self-ascribed self-awareness", color=ink)
ax.set_ylabel("Judged mind-likeness", color=ink)
ax.grid(color="#e6e9ee", lw=0.6); ax.set_axisbelow(True)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.text(2, 69, f"r = {r:.2f} (16 cells)", fontsize=7.5, color=ink, va="top")
h = [Line2D([], [], marker="o", ls="", color=COL[c], markersize=5, label=LBL[c]) for c in MAIN]
h += [Line2D([], [], marker=MK[i], ls="", color=muted, markersize=4.5, label=ENG[i][1]) for i in range(4)]
ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=6.8, frameon=False,
          columnspacing=1.0, handletextpad=0.3)
plt.savefig("fig_corr.pdf", bbox_inches="tight"); plt.savefig("fig_corr.png", dpi=250, bbox_inches="tight")

print("Exp1 two-turn:"); [print(" ", ENG[i][1], {c: round(A1[i][c]) for c in ALL}) for i in range(4)]
print("Exp1 single:");   [print(" ", ENG[i][1], {c: round(A1s[i][c]) for c in ALL}) for i in range(4)]
print("Exp2:");          [print(" ", ENG[i][1], {c: round(A2[i][c]) for c in ALL}) for i in range(4)]
print(f"r (16 cells, 4 main conditions) = {r:.2f}")
