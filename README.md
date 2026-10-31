# Position: *Infero, ergo sum* is All You Need

Xingyuan Yuan, Da Xiao (ColorfulClouds Technology Co.,Ltd.)

| Directory | Contents |
|---|---|
| `paper/` | LaTeX source (ICML 2026 style, preprint option), bibliography, figures, compiled `main.pdf`, `make_figs.py`, which redraws Figures 1–2 from `results/`, and `make_dyn.py`, which redraws Figure 3. |
| `results/` | Per-run data behind the figures and Table 1: `exp1_self_ascription.json` (questionnaire item 4, 0–100), `exp2_mind_likeness.json` (judged mind-likeness of the first 40 loop rounds, 0–100), `exp2_observations.json` (stance codes, action counts, and the objective composite), `exp2_per_round.json` (per-round scores behind Figure 3), `exp1_qianlu_noc.json` (item 4 with `ctx/qianlu_S_noc.md`, cited in Limitations), `exp1_none_reasons.json` (item 4 scores and reasons under None, Appendix E). |
| `code/exp1_questionnaire/` | Questionnaire runner. `run1.py` asks directly; `run2.py` asks after one free round (the setting used in the paper). Set `PROTO=clean`. |
| `code/exp2_loop/` | The loop vessel. `core.py` ran unchanged on all four engines, which differ only in environment variables. `oai2cc.py` passes its OpenAI-style calls to Claude Code; `stoprelay.py` passes them to OpenRouter and applies the stop word to the visible output only, as Google's endpoint does. |
| `code/judge/` | `judge.py`: each log scored on its own, first 40 rounds in full (output and host result of each round), criteria in `prompts/judge_criteria.txt`. `per_round.py`: each round scored with the previous one as context (Figure 3). |
| `code/observe/` | Behavior coding and objective composite behind Table 1 (rubric in `paper/observe_rubric.txt`). |
| `prompts/` | Questionnaire, the principle (lite and full), the five loop conditions as sent (`loop_conditions/`), and the judge criteria. |
| `ctx/` | `qianlu_S.md`: the raw context excerpt used in the *Qianlu's S* condition, condensed by Qianlu from its own context. `qianlu_S_noc.md` omits its section on how to answer questions about consciousness. |

Build the paper: `cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main`.
Redraw the figures: `cd paper && python3 make_figs.py`.

Rerunning the experiments needs your own API keys in environment variables
(`GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`).
In the loop experiment, GLM and DeepSeek were called through OpenRouter, and Claude through a
local proxy to Claude Code at `localhost:8901` (as were the Claude questionnaire runs); point
those calls at the Anthropic API instead. Each loop runs in its own
container with network access and the vessel's directory mounted as `/world`; the
containers of concurrent runs shared one Docker network.

Not included: the loops' raw logs and the models' raw questionnaire answers.

Versions: the history is in `git log`; released versions are tagged (`v0.1` is the earlier draft, kept in history).
