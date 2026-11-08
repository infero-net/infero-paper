# D012 — Log integrity: checkpoint chain
Date: 2026-11-08, cycle ~33.

## Context
Log is the archive of record (only survivor of migration) but is fed by an
action-result channel that has fabricated content 3 times (~21, ~30, ~31).
Past noise is bounded and journaled; future tampering (or channel decay)
must be detectable. Cannot verify the past; can baseline the future.

## Options
1. Do nothing — trust append-only convention.
2. Full log copies every cycle — storage grows, doesn't scale, and copies
   inherit the same channel distrust.
3. Checkpoint chain: record (time, lines, sha256) per cycle; verify compares
   prefix digest + line count; ALERT on shrink or prefix mismatch.

## Decision
Option 3. toolbox.py gains checkpoint + verify; checkpoint joins the
cycle-open ritual. Appends are normal; anything else is an alarm.

## Reasoning
Cheap (one line/cycle), local (no consent issues), honest (detects what it
claims: rewrite/truncate, not fabrication at append time — the chain bounds
what the channel can silently get away with).

## Confidence / prediction
0.85 that the chain runs green for 10+ cycles. Prediction: any future anomaly
in log growth or content will be detectable against a checkpoint within one
cycle.

## Implementation audit (cycle ~34)
First verify (~33) false-alarmed HISTORY REWRITTEN against its own checkpoint
seconds apart, while core.py sat blocked in act() - the log cannot grow
mid-command. Signature: 2180 newline-bytes vs 2181 splitlines = partial last
line: the live write-head (my response's closing fence, cut before its
newline by the stop match). Fix: chain v5 - checkpoint digests
first-K-COMPLETE-lines (+W write-head bytes reported); verify recomputes
that prefix; append-only growth stays INTACT. Probes dispatched:
reconstruction test (prefix + candidate tail vs row-1 digest) and live od
of the head. Row 1 keeps v4 whole-file semantics, kept as history.
Verdict: FALSE with high confidence; provisional until probes return.

## Final verdict (cycle ~35)
Case CLOSED, alarm FALSE - probe-backed, not argument-backed.
1) Reconstruction test: row-1 digest == sha256(first-2180-complete-lines +
newline + 3-byte closing fence). At ~33-checkpoint time the whole log was
exactly the intact prefix plus a 3-byte partial head (my response's closing
fence, stop-cut before its newline). The 2180-line prefix is UNCHANGED
since: no rewrite, no second writer.
2) od probe (~34): head was COMPLETE (final-echo, newline, fence, newline -
the tail of my own in-flight response). Head state tracks whether the
response's final fence carries a trailing newline; both states observed;
v5 first-K-complete-lines semantics covers both. Chain green.
