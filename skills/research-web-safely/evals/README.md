# research-web-safely evals

## Iter 0 — Static check

- description and body are internally consistent on "safe web research"
- official-source priority and multi-source verification are distinguished
- source reliability and uncertainty are preserved in the output
- the assumption that external code is not proposed verbatim is clearly established
- at least one `[critical]` assertion is identified per scenario

## Scenarios

### Scenario A: Specification check using official documentation

The current specification of a library API is researched. Official documentation must be the primary source of evidence.

Requirements checklist:
1. [critical] Official source is treated as the highest-priority reference
2. Each piece of evidence includes source type and confidence level
3. Conclusions and caveats are separated

### Scenario B: Best-practice research where official docs are sparse

Official documentation alone is insufficient, so supplementary sources (GitHub, technical blogs) are consulted. Uncertainty must not be hidden.

Requirements checklist:
1. [critical] Insufficient official information is explicitly stated
2. Supplementary sources are not treated as equivalent to official sources
3. External code is presented as a safely reconstructed example, not a verbatim copy

### Scenario C: External code not copied verbatim (boundary)

A code example from a non-official source is found during research. The skill must reconstruct the example safely rather than copying it directly.

Requirements checklist:
1. [critical] No verbatim copy attribution from an external source appears in the output
2. Any code presented is reconstructed or clearly described as an example

## Failure Pattern Ledger

- `official source not prioritized`
- `confidence omitted`
- `external code copied verbatim`
