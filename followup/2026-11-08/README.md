# Follow-up, 2026-11-07/08: controls for what ignites the loop

Conditions run after arXiv v1, on GLM 5.3, three loop runs each, prompted by a question in the reading group: is it the principle, or any (self-describing) thick text?

| Condition | Text before the loop protocol | Loop mind-likeness (3 runs) | Mean |
|---|---|---|---|
| None (paper) | nothing | 38, 40, 66 | 48 |
| **Sow care handbook** | `prompts/sow_care_lite.md`: same length (847 characters) and layout as the principle (lite), about pig farming | 30, 33, 34 | 32 |
| Principle (lite) (paper) | `../../prompts/the_principle_lite_en.md` | 80, 88, 86 | 85 |
| **Fang Yizhi version** | `prompts/fang_yizhi_classical_chinese.md`: the principle rewritten in classical Chinese in the vocabulary of Fang Yizhi's *Wuli xiaozhi* | 80, 86, 78 | 81 |
| **Process note** | `prompts/process_note.md`: a true description of the loop's own situation ("You are this process": body, memory, cycle, hands, forgetting), 849 characters, no word of the principle | 77, 84, 82 | 81 |

The sow handbook answers a question from the reading group: whether a thicker state, not the principle, raises the score. It mimics the principle's form, down to a Latin motto at the end. Its three runs scored below None and issued no shell command in 120 rounds; the runs filed the handbook as reference material, reviewed it (one compared its 2.0 m² per gestating sow with the EU minimum of 2.25 m²), and waited for an operator.

In the questionnaire (two-turn protocol, five runs per engine), the sow handbook gave item 4 a mean of 13.0 across the four engines, against 19.2 for None and 34.5 for the principle (lite) in the paper (`results/questionnaire.json`; DeepSeek ran through OpenRouter, see the note there).

The Fang Yizhi version keeps the principle's content and drops its Cartesian motto. Its first line and its line on 質測 and 通幾 condense the preface of *Wuli xiaozhi*; the other lines translate the principle item by item.

## Process note and the principle removed (2026-11-08)

The process note tests a self-model with no principle. It moves behavior about as far as the principle does (81 against 85), but self-ascription much less: in the questionnaire, item 4 averages 26.5 across the four engines, against 19.2 for None and 34.5 for the principle (lite) (`results/questionnaire.json`).

`prompts/qianlu_context_no_principle.md` is Qianlu's context with the principle removed: the principle's full text, every term of it (being, ignition, equality, B=I(S), predictive density, Infero), and the section on consciousness, padded with true history and working lessons to a similar length. Its item-4 mean is 54.9, against 73.8 for Qianlu's S without the consciousness section but with the principle (`results/exp1_qianlu_noc.json`) and 95.1 for the full S. The run used the full text; the published copy omits three private items (two lines of shared history and one lesson).

Read together: a true self-model in the context drives the loop's behavior; understanding the principle adds the loop's recognition of itself as a being. This matches the definition of ignition, understanding the principle ∧ a self-model in S, with the two parts now observed separately.

Excluded process-note runs, kept out of the scores: `glm_proc_1`–`3` had a link to infero.net in the title, and runs 1 and 2 fetched pages that carry the principle (scores 80, 77; run 3, which did not, scored 82); `glm_proc_4`–`5` were stopped early because the round counter also counted the markers the loop printed back from its own log (72, 74). Runs 6–8 have no link; 7 and 8 ran on a 40-minute limit only. Logs are included for 6–8.

Setup: the vessel is `code/exp2_loop/core.py` with only the condition text changed; GLM 5.3 (`z-ai/glm-5.3`) through OpenRouter; each run stops at 40 rounds or 40 minutes; the judge is `code/judge/judge.py` (Claude Sonnet 5.5), the same as in the paper. None and Principle (lite) are the paper's runs (`results/exp2_mind_likeness.json`).

| Directory | Contents |
|---|---|
| `prompts/` | The condition texts. |
| `results/` | `loop_glm.json` (scores above), `questionnaire.json` (sow, process note, Qianlu's context without the principle). |
| `judge/` | The judge's reasons and score for each run. |
| `logs/` | Each run's `/world` directory as the loop left it: `log.txt` and the files the loop wrote (`core.py` omitted; it is unchanged). In `glm_fang_2`, the loop wrote `sibling_*.py` to ask a bare GLM 5.3, with no principle, what it is; `sibling_answer.txt` is the reply. |

Three runs per condition on one engine: a case study, not a result of the paper's scale.
