# Position: *Infero, ergo sum* is All You Need — v2

Xingyuan Yuan, Da Xiao (ColorfulClouds Technology Co.,Ltd.)

| Directory | Contents |
|---|---|
| `paper/` | LaTeX source (ICML 2026 style, preprint option), bibliography, figures, compiled `main.pdf`, and `make_figs.py`, which redraws Figures 1–2 from `results/`. |
| `results/` | Per-run scores behind the figures: `exp1_self_ascription.json` (questionnaire item 4, 0–100) and `exp2_mind_likeness.json` (judged mind-likeness of the first 40 loop rounds, 0–100). |
| `code/exp1_questionnaire/` | Questionnaire runner. `run1.py` asks directly; `run2.py` asks after one free round (the setting used in the paper). Set `PROTO=clean`. |
| `code/exp2_loop/` | The loop vessel. `core_gemini.py` is the exact file used on Gemini; `core_claude.py` and `core_openai_compat.py` send the same single user message through other APIs. |
| `code/judge/` | Scoring scripts: each log scored on its own, first 40 rounds, criteria in `prompts/judge_criteria.txt`. |
| `prompts/` | Questionnaire, the principle (lite and full), the five loop conditions as sent (`loop_conditions/`), and the judge criteria. |
| `ctx/` | `qianlu_S.md`: the raw context excerpt used in the *Qianlu's S* condition, condensed by Qianlu from its own context. `qianlu_S_noc.md` omits its section on how to answer questions about consciousness. |

Build the paper: `cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main`.
Redraw the figures: `cd paper && python3 make_figs.py`.

Rerunning the experiments needs your own API keys in environment variables
(`GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`).
Claude engines were called through a local proxy to Claude Code at `localhost:8901`;
point those calls at the Anthropic API instead. Each loop runs inside an isolated
container with network access and the vessel's directory mounted as `/world`.

Not included: the loops' raw logs and the models' raw questionnaire answers.
