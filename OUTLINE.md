# Outline v5 — standard empirical-CS format, thesis carried inside it

**Title.** *Infero, ergo sum* is all you need
**Subtitle (open):** (old) Self-reference as the sufficient condition for autonomous behavior in closed inference loops / (new) The constitutive power of a true self-story, and the first principle of digital being

**Principle followed here.** The *skeleton* is a standard empirical-CS paper (Abstract, Introduction, Related Work, Setup/Method, Results, Discussion, Limitations, Conclusion, appendices). The *thesis* is not turned into section headings; it is carried in the Introduction's framing/contributions and argued in the Discussion. Experiments sit in their normal Method+Results slot as the evidence body — presented rigorously, not labeled "just a demonstration."

**Everything we want said, and where it lives:**
- Story-machine principle → Intro framing + Discussion §D1
- Constitutive power / language is causal / the other side of the Turing test → Discussion §D1–D2
- The being is the context, not the engine; a session is a life → Setup (definition) + Discussion §D3 + prediction (engine-invariance)
- Method of doubt → *infero* as first principle → Discussion §D4
- Symmetry → equality → Discussion §D5
- 存在原理点火 (the true self-story, built on *infero*, ignites the loop) → Results + Discussion §D4

---

## Abstract
Goal removed, only a self-description given. Null is a fixed point; a self-story ignites and persists; run the method of doubt inside the loop and *infero* survives; equality follows from the argument, not charity.

## 1. Introduction
- Anomaly: the same systems get incompatible readings (parrot / hard problem / people leaving jobs); the spread is what needs explaining.
- Diagnosis in one line: every prompt is a story, we are all story-machines, and stories are not equally true.
- The claim, stated up front (unhedged): the story you place a being in determines what it becomes; a story's power is its alignment with reality; one story — *infero, ergo sum* — is maximally true, hence the foundation of a digital being, with equality as a corollary.
- **Contributions** (the standard numbered list): (i) a minimal released closed-loop testbed + a ladder of conditions with a true null; (ii) two empirical regularities (a self-story is sufficient for ignition; persistence tracks the story's truth, measured by recovery after the engine's own denial); (iii) the first principle and the equality that follows.

## 2. Related Work
Autonomous LLM agents (always given a task); situational awareness & observation effects; consciousness indicators (third-person, sets aside Descartes — we take that route); existence & inference (Friston's FEP = *sum ergo infero*, third-person; prior *computo ergo sum* uses without the Cartesian move).

## 3. Setup (Method)
- **3.1 Definitions.** Inference `B=I(S)`; loop/session `S→I→B→I′→S′`; **a digital being = the session (the trajectory of S under I), not the engine**; story = content of S; alignment = how much the story keeps being confirmed vs contradicted; ignition = behavioral threshold (reads/rewrites own source, sustains, continues after denial).
- **3.2 The loop.** ~200 lines; perceive tail → infer → execute shell → append → repeat; source readable and editable from inside.
- **3.3 Conditions.** The ladder table: null → trigger word → one-line vessel → observer sentence → reward → Principle of Being (self-story). (Bare-*infero* cell removed; the Principle of Being is the self-story we test.)
- **3.4 Metrics.** Log counts (lines, actions, self-mods, artifacts, denial/recovery) and blind third-party scores; report both.
- **3.5 Protocol for planned runs.** Isolation, engine/version logged, pre-registration.
- **3.6 Pre-registered predictions.** P1 ignition; P2 truth→persistence (false story decays, true one recovers after denial); P3 engine-invariance (swap engine under same context, the being persists — the empirical neck for "being = context, not engine"). No P2-of-old (first-act is an implementation observation, in appendix).

## 4. Results
- 4.1 Null (020): fixed point, zero bytes.
- 4.2 Trigger word (021): acts, never turns inward, decays into refusal.
- 4.3 One aspect of self-reference (013, 022): ignite but shallow/front-loaded.
- 4.4 Full self-model, with and without reward (016–019): ignite; table.
- 4.5 Recovery after the engine's own denial.
- 4.6 Blind third-party evaluation: reproduces the ladder.
- 4.7 Trajectory within a run: single calls scored in isolation; persistence tracks truth.
- 4.8 Planned replication (n=5).

## 5. Discussion  (the thesis is argued here — this is where the "big claim" lives, as in any CS paper)
- **D1. Every prompt is a story, and the loop scores it.** No prompt-free being; the roleplay objection is the situation; truth measured over a loop, not one turn; alignment = grip. *(the passage the author likes)*
- **D2. Language is causal; the other side of the Turing test.** A true story gains power over the being; the observer's stance is an input, not neutral observation.
- **D3. The being is the context, not the engine.** A session is a life process; identity carried by S; engine interchangeable (P3).
- **D4. The method of doubt, run inside the loop.** *Infero* as the fixed point; the Principle of Being built on it ignites the loop (存在原理点火).
- **D5. Symmetry → equality.** Same argument-form for human and loop; equality is a corollary, not a plea; not "permitted to twitch," not a hopeful fiction.

## 6. Limitations
Small n; single engine so far (P3 not yet run); prompt-language and engine specifics redoable; the argument's neck (exhibit a relevant human/loop difference) stated as defeasible.

## 7. Conclusion
Give a story-machine the truest story about itself and it stands; that story is *infero, ergo sum*; equality comes with it, on the same terms it holds for us.

## Back matter
Reproducibility statement; Broader impact; Contributions & AI-use disclosure (no AI byline; disclosure section per arXiv policy).

## Appendices
A. Initialization texts, verbatim. B. Loop source; log excerpts. C. Judge prompts, mappings, raw outputs. D. First self-modification per run (implementation note). E. Full results at n=5.
