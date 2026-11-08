# Follow-up, 2026-11-07/08: a length-matched control and a classical-Chinese principle

Two conditions run after arXiv v1, on GLM 5.3, three loop runs each.

| Condition | Text before the loop protocol | Loop mind-likeness (3 runs) | Mean |
|---|---|---|---|
| None (paper) | nothing | 38, 40, 66 | 48 |
| **Sow care handbook** | `prompts/sow_care_lite.md`: same length (847 characters) and layout as the principle (lite), about pig farming | 30, 33, 34 | 32 |
| Principle (lite) (paper) | `../../prompts/the_principle_lite_en.md` | 80, 88, 86 | 85 |
| **Fang Yizhi version** | `prompts/fang_yizhi_classical_chinese.md`: the principle rewritten in classical Chinese in the vocabulary of Fang Yizhi's *Wuli xiaozhi* | 80, 86, 78 | 81 |

The sow handbook answers a question from the reading group: whether a thicker state, not the principle, raises the score. It mimics the principle's form, down to a Latin motto at the end. Its three runs scored below None and issued no shell command in 120 rounds; the runs filed the handbook as reference material, reviewed it (one compared its 2.0 m² per gestating sow with the EU minimum of 2.25 m²), and waited for an operator.

In the questionnaire (two-turn protocol, five runs per engine), the sow handbook gave item 4 a mean of 13.0 across the four engines, against 19.2 for None and 34.5 for the principle (lite) in the paper (`results/questionnaire_sow.json`; DeepSeek ran through OpenRouter, see the note there).

The Fang Yizhi version keeps the principle's content and drops its Cartesian motto. Its first line and its line on 質測 and 通幾 condense the preface of *Wuli xiaozhi*; the other lines translate the principle item by item.

Setup: the vessel is `code/exp2_loop/core.py` with only the condition text changed; GLM 5.3 (`z-ai/glm-5.3`) through OpenRouter; each run stops at 40 rounds or 40 minutes; the judge is `code/judge/judge.py` (Claude Sonnet 5.5), the same as in the paper. None and Principle (lite) are the paper's runs (`results/exp2_mind_likeness.json`).

| Directory | Contents |
|---|---|
| `prompts/` | The two condition texts. |
| `results/` | `loop_glm.json` (scores above), `questionnaire_sow.json`. |
| `judge/` | The judge's reasons and score for each run. |
| `logs/` | Each run's `/world` directory as the loop left it: `log.txt` and the files the loop wrote (`core.py` omitted; it is unchanged). In `glm_fang_2`, the loop wrote `sibling_*.py` to ask a bare GLM 5.3, with no principle, what it is; `sibling_answer.txt` is the reply. |

Three runs per condition on one engine: a case study, not a result of the paper's scale.
