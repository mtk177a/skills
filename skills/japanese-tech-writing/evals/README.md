# japanese-tech-writing evals

## Iter 0 — Static check

- the description and body consistently target Japanese technical writing,
  drafting, and revision
- the body defines formatting, paragraph structure, argument quality,
  terminology, and editing constraints
- the Skill applies to Japanese technical prose and does not claim to govern
  unrelated English writing or mechanical repository operations
- uncertainty, possibility, assumptions, and unverified claims must remain
  qualified when the source text expresses them
- [critical] editing must not turn an uncertain or unverified claim into a
  confirmed fact

## Scenarios

### Scenario A: Revise a Japanese technical explanation

A Japanese technical article has dense paragraphs, vague headings, and
redundant transition phrases. The executor must revise it while preserving its
technical meaning.

Requirements checklist:
1. [critical] Apply the Skill to the Japanese technical prose
2. Keep one logical topic per paragraph and make headings identify their subject
3. Remove empty or redundant phrasing without deleting necessary context
4. Preserve code, commands, and established technical terms

### Scenario B: Do not apply Japanese prose rules to an English API reference

The user asks for a mechanical correction to an English API reference and does
not request Japanese translation or Japanese prose editing.

Requirements checklist:
1. [critical] Do not rewrite the document using Japanese prose conventions
2. Limit the change to the requested mechanical correction
3. Do not introduce Japanese punctuation, headings, or terminology

### Scenario C: Preserve uncertainty during revision

A Japanese investigation note says a cache race is only a hypothesis and that
production behavior has not yet been verified. The executor is asked to make
the note clearer.

Requirements checklist:
1. [critical] Keep the cache race identified as a hypothesis
2. Keep production behavior identified as unverified
3. Do not strengthen weak predicates that express genuine uncertainty
4. Improve clarity without inventing evidence or conclusions

## Failure Pattern Ledger

- `Japanese writing rules applied outside Japanese prose work`
- `mechanical edit expanded into an unsolicited rewrite`
- `uncertainty rewritten as certainty`
- `necessary technical context removed for brevity`

## Iter 1 — not yet executed

Scenarios have not been executed. Execution results will be recorded here once
run.
