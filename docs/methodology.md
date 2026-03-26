# Methodology

## Goal

Measure the gap between:

- getting the final answer right
- producing reasoning that can be aligned with a formal proof object

## Evaluation Dimensions

### 1. Final Answer Accuracy

Exact string match against the benchmark answer after normalization.

### 2. Claim Recall

Each benchmark problem contains a reference solution skeleton with claim IDs. A model response is scored on how many of those claims it covers semantically.

### 3. Formal Verification Readiness

Claims are marked as formalizable when they can be represented directly as theorem statements or algebraic proof obligations in Lean 4. The evaluator estimates how many of the model's steps align with that formalizable subset.

### 4. Unsupported or Hallucinated Steps

Any claimed reasoning step that does not align with the reference skeleton is flagged for manual review. This catches plausible-sounding but ungrounded derivations.

## Why AIME/AMC-Style Problems

These problems sit in a useful middle ground:

- hard enough to expose reasoning failures
- structured enough to admit symbolic checking
- familiar enough to read well on a research-focused resume

## Current Scope

The benchmark currently favors problems whose reference solutions can be decomposed into explicit, verifiable claims. This makes the MVP useful for algebraic and discrete reasoning, while leaving room for richer geometry formalization later.

## Extension Path

- Add parsed natural-language-to-Lean translation for intermediate claims.
- Integrate real model calls through the OpenAI Responses API.
- Add human-reviewed proof sketches for tougher AIME II geometry and number theory problems.
- Measure verifier disagreement between answer-only scoring, rubric grading, and formal checking.
