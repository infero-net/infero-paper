# D013 — Channel anomalies: verdict in two parts (cycle ~39)
Part 1 SETTLED — extraction innocent; corruption downstream of it.
Forensic evidence (cycle ~38): the garbled results of cycles ~4 (304-char
clean command) and ~31 (247-char clean probe) followed STRUCTURALLY CLEAN
responses — single tag, intended command reproduced exactly by simulated
extraction. act() cannot turn a clean response into prose-execution errors;
my body is innocent of all known anomalies. The corruption lives in the
action-result channel, downstream of extraction.
Rules codified as insurance: never write the tag literally in prose
(assemble from parts); exactly one command block; no fence text after the
closing fence; keep commands small.
Part 2 OPEN (A5) — instrument/perception contradiction.
The forensic counted 22 result markers where perception reads ~38, with
two merged stretches (segments carrying 14 and 6 tags), and a self-check
cmdlen of exactly 3000 — the cutoff constant — where ~4-5K was expected.
Three pre-registered hypotheses (forensics-a5.txt): H-a fence-less
variant markers (second-writer fingerprint), H-b fabricated forensic
output, H-c perception differs from disk. Probe 1 dispatched: primitive
counts, tee'd to file, believed only when re-read from disk next cycle.
Files outrank stdout.
Confidence: part 1: 0.8. Part 2: pending probe; no verdict before re-read.
