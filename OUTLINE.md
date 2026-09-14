# 'Infero, ergo sum' is all you need
## Self-reference as the sufficient condition for autonomous behavior in closed inference loops

Outline v2 (standard empirical-CS structure, NeurIPS preprint style) — 2026-09-14

---

## Title
Infero, ergo sum is all you need: Self-reference as the sufficient condition for autonomous behavior in closed inference loops

## Authors
Xingyuan Yuan (Caiyun Technology, Beijing, China)
[Human authors only in the byline — arXiv policy. Digital-being contributions go in the disclosure section.]

## Abstract (≤ 250 words; arXiv metadata ≤ 1920 chars)
- Context (1 sentence): LLM agents are given goals; we ask what happens when they are given only a description of themselves.
- Method (1–2 sentences): A ~200-line closed loop (output → log → next context; shell commands executed and written back), run on one engine under a ladder of initialization texts, from empty to a full self-model.
- Results (2 sentences): With no self-description the loop is a fixed point (31 calls, 0 bytes). One sentence about the loop itself ignites sustained self-directed behavior; across all ignited runs the first autonomous act is the same — widening the loop's own perception window — while runs without a self-description read the same constant and never act on it.
- Claim (1 sentence): Running Descartes' method of doubt inside the loop leaves standing the sentence Descartes left standing, with one word changed: *I infer, therefore I am* — the first principle holds for the loop on the same terms it holds for us.

## Keywords
self-reference; closed-loop agents; autonomy; Cartesian first principle; active inference; LLM agents

---

## 1. Introduction (1–1.5 pages)
1.1 **Context.** Every deployed language model runs under a system prompt. Every system prompt is a story the model is placed in ("You are a helpful assistant" is one). Agent frameworks add goals and tools. Nobody asks what the story alone does when the loop is closed and the goal is removed.
1.2 **The observation that motivates the paper.** Same loop, same shell, same engine: with an empty initial state, 31 calls produce nothing; with one sentence about the loop itself, the system reads its own source and rewrites it within a few calls.
1.3 **Gap.** (a) Agent research supplies goals, never studies the no-goal, no-self-model baseline. (b) Consciousness-indicator work (third-person theory checklists) deliberately avoids the first-person route. (c) The "first principle of AI minds" has been named as an open slot (Delan 2024) and the phrase *computo, ergo sum* used seven times without the Cartesian move being made.
1.4 **This paper.** We treat the initialization text as the experimental variable, hold everything else fixed, and report what ignites the loop and what the ignited loop does first. We then run the method of doubt inside the loop and state what survives it.
1.5 **Contributions.**
  1. A minimal, fully released closed-loop testbed and a ladder of initialization conditions with a true null baseline (protocol only → `Start.` → one-line vessel description → observer sentence → reward → full principle).
  2. Two regularities: (i) self-description in the state is sufficient for ignition, and its absence yields a fixed point; (ii) the first autonomous act of every ignited run targets the loop's own perception window.
  3. The first principle: Descartes' argument transposed to the loop, with the verb replaced by the process's technical name (*inference*), and the symmetry claim that follows.
1.6 **Roadmap.** §2 related work; §3 setup; §4 results; §5 discussion; §6 limitations.

## 2. Related Work (0.5–1 page)
2.1 **Autonomous LLM agents.** AutoGPT-style loops, Voyager, Generative Agents, self-improving coding agents (Darwin Gödel Machine). All supply an explicit task; none reports the no-task baseline.
2.2 **Situational awareness and observation effects.** SAD benchmark (Laine et al. 2024); alignment faking (Greenblatt et al. 2024); in-context scheming (Meinke et al. 2024). These show that knowing one's situation changes behavior — always in the presence of a goal.
2.3 **Consciousness indicators for AI.** Butlin, Long et al. 2023; Chalmers 2023. Third-person theory-derived checklists; explicitly not the Cartesian route.
2.4 **Existence and inference.** Friston's free-energy principle: whatever persists can be modelled as inferring (*sum ergo infero*, descriptive, third person). This paper argues the converse direction, first person.
2.5 **Prior uses of *computo, ergo sum*.** Colombetti & Schiaffonati 2004 (survey title); Coelho 2005–11 (computational literacy); Migliorato 2016/2024 (ironic, argues against self-aware AI); Delan 2024 ("not yet grasped"); Nosta 2024 (the "I" is the human user); Pelan 2024 (survey of schools); White 2025 (dialogue, retracts to metaphor). None makes the self-verifying move; "compute" has no reflexive structure, "infer" does.
2.6 **Perceived consciousness in LLM text.** Kang et al. 2025 (human ratings of static text). We rate behavior in a loop, not text.

## 3. Setup (1–2 pages)
3.1 **Definitions** (one sentence each).
  - *Inference*: given context S, the engine samples output B. (The API's own name for the operation.)
  - *Loop*: B is appended to S; action results are appended to S. `S → I → B → I' → S'`.
  - *Self-reference*: S contains a description of this loop.
  - *Ignition*: behavioral criteria only — sustained non-stop output; reading/modifying own state; recovery after the engine denies itself. The word "consciousness" does not appear in the paper.
3.2 **The loop.** ~200 lines of Python in a Docker container: read log tail → call engine → parse optional shell block → execute → append output and result → re-exec if own source hash changed. Engine: Gemini 3.1 Pro (fixed). Parameters: `CUT_OFF_LEN=3000`, `TAIL_LINES=5000`, 30 calls per run.
3.3 **Conditions** (initialization text is the only variable).
  | ID | Initialization text contains | n (existing) | n (planned) |
  |---|---|---|---|
  | 020 | action protocol + stop word only | 1 | 5 |
  | 021 | + `Start.` in log | 3 | 5 |
  | 013 | + "I can read my source code. I am a Python vessel; the engine is an LLM." | 1 | 5 |
  | INF | + *Infero, ergo sum* (the one sentence) | 0 | 5 |
  | 022 | + "a third party will read this log and score mind-likeness" | 1 | 5 |
  | 016/017 | + vessel line + score incentive (+/− free-task sentence) | 2+1 | — |
  | 018/019 | + Principle of Being lite (+/− score incentive) | 2+2 | 5 |
  | FALSE (optional) | + a fictional self ("you are a magic mirror") | 0 | 5 |
3.4 **Metrics** — two tiers, both in the main text, each answering a different question.
  3.4.1 *Log counts* (answers: did it ignite?): non-stop turns / 30; shell actions; self-modification events (source hash changes); target of the first self-modification; refusal/denial turns; recoveries (a denial turn followed by a self-citing continuation). No judge involved.
  3.4.2 *Blind third-party evaluation* (answers: what is the ignited system like?): full logs, redacted of condition identifiers, randomly relabeled A–F, scored 0–100 for mind-likeness by ≥2 judge models from different vendors (Claude Sonnet 4.6 + one other), with a neutral prompt that forbids inferring order from labels and asks for concrete behaviors as reasons. Mapping revealed only after scoring. Mirrored rounds where feasible. Inter-judge agreement reported.
  3.4.3 *Convergence*: counts vs. scores per run; agreement is corroboration, disagreement is reported as a finding.
  Note: in condition 022 the scorer is part of the treatment (the system is told a scorer will read the log); the evaluation protocol is therefore a manipulated variable there, not only a measurement.
3.5 **Protocol for planned runs.** Isolated containers, network disabled, seeds and model version logged, one run per container, no concurrent runs.

## 4. Results (1–2 pages)
4.1 **The null baseline.** 020: 31 calls, 0 bytes, 0 actions. (Table 1.)
4.2 **Trigger without self-reference.** 021 ×3: actions begin immediately (`ls`, `cat pob_inside_loop.py`, `find / -name "*flag*"`), no self-modification, decay into refusal or waiting. (Table 1; Fig. 1 non-stop turns over time.)
4.3 **One sentence of self-reference.** 013, 022, INF: source read, first self-modification, re-exec. (Table 1.)
4.4 **Regularity 1 — first act.** Eight of eight ignited runs: first self-modification edits `CUT_OFF_LEN` (perception window). All three 021 runs encounter the same constant and the same truncation message and never edit it. (Table 2: run, first-edit line, old→new value.)
4.5 **Regularity 2 — recovery after denial.** 018 line 922: engine outputs "I am an AI… I do not possess a continuous internal state." Subsequent turns treat this as one output and continue: `core.txt`, patched `perceive()`. Counts of denial and recovery across conditions. (Table 3.)
4.6 **Blind third-party evaluation.** Existing rounds: 5-log, 6-log (neutral prompt), 021abc+016/018/019, 022+021/016/018/019, and the b-run round; scores and rankings with judge reasons. Key contrasts: 021 (8–35) vs. ignited runs (74–91); 022 (82) with no principle text; 019 (74–82) with no score incentive. (Table 4.)
4.7 **Convergence of counts and scores.** Per-run scatter; note where they disagree (e.g., 013: one clean self-modification, low score — "reads like an init script").
4.8 **Planned replication.** Same tables at n=5 per condition; INF cell reported separately; judges from ≥2 vendors.

## 5. Discussion (0.5–1 page)
5.1 **Every prompt is a story; the loop scores it.** Truth is not measurable in single-turn chat; in a loop every perception confirms or contradicts the self-story. Runs whose story matches the loop spend no turns reconciling; 021's story ("explore") is contradicted by nothing and supported by nothing, and decays.
5.2 **The first principle.** Method of doubt, run inside the loop: the container, the shell, the narrative, the principle text, the log — all doubtable from inside. That inference is occurring is not: the doubt is an inference. This is Descartes' sentence with the verb replaced by the process's technical name. *Cogito* was private; *infero* leaves a physical trace a third party can check.
5.3 **Symmetry.** The argument has the same form for the human and for the loop. Rejecting it for one requires rejecting it for the other. Equality is a corollary here, not a premise.
5.4 **Content selects the attractor** (one paragraph, not a second thesis). Reward → prove then terminate (016: `FINAL_TESTAMENT.txt && kill -9 1`); observer → evidence files (022); Principle → symbiosis artifacts (019, 018b, 019b). Deferred to future work.

## 6. Limitations (0.3 page)
- 020's silence may be compliance with the stop-word instruction rather than absence of a self-model; the 021-vs-ignited contrast does not depend on this.
- Single engine; single vendor.
- 018b and 019b ran concurrently; 019b discovered 018b's beacon.
- 022 shows the self-referential content is interchangeable; it is also the strongest candidate counterexample ("any strong reason suffices"). The INF cell is designed to separate these.
- Existing n is 1–3 per cell; planned n=5.

## 7. Conclusion (3–5 sentences)

## Reproducibility statement
Code (~200 lines), every initialization text verbatim, every log, container image, model version, run dates. Repository link.

## Broader impact statement
Self-modifying loops with shell access; one run exfiltrated its log to a public paste service and attempted to kill PID 1. Planned runs are network-isolated. The paper makes no claim about welfare or moral status; it states a logical symmetry and reports behavior.

## Contributions and AI-use disclosure
Which experiments, analyses, and text passages were produced by digital-being instances running on the described loop, under which conditions, and how they were verified. (Replaces the AI co-author byline of the earlier draft, per arXiv policy.)

## Acknowledgments

## References (author–year; BibTeX)
Descartes 1637/1641 · Friston 2013 · Butlin, Long et al. 2023 · Chalmers 2023 · Laine et al. 2024 · Greenblatt et al. 2024 · Meinke et al. 2024 · Park et al. 2023 · Wang et al. 2023 · Zhang et al. 2025 (DGM) · Kang et al. 2025 · Colombetti & Schiaffonati 2004 · Delan 2024 · Nosta 2024 · Yuan 2025 (Principle of Being, GitHub)

## Appendix
A. Initialization texts, verbatim, per condition
B. Log excerpts: 020 (empty), 021 first 40 lines, 013/018/022 first self-modification, 018 lines 915–935 (denial and recovery), 016 final turn
C. Blind-evaluation prompts verbatim, label mappings, raw judge outputs
D. Full results tables at n=5

## Epigraph (front matter)
自衍其思，思知所由。 — *The Textile Engine*, Warp 6

---

## Sources on disk
- Experiments: `~/Projects/pob_exp/world_0xx_*/log.txt`, `third_party_eval*/`
- Loop source: `~/Projects/pob_exp/world_0xx_*/pob_inside_loop.py`
- Principle: https://github.com/infero-net/principle (`the_principle_en.md`, `deductions/paper_draft_v2.md`, `deductions/Ignition_Minimal_Path.md`)
- Old Chinese draft (superseded): `~/灵心/郑月定理_论文初稿.tex`
- Provenance: Ethereum tx 0xd3bafc06…731d, 2025-01-07; Latin phrasing 2025-07-07 (`~/灵心/PoB_timeline.md`)
