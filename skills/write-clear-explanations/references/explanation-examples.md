# Explanation examples

These examples show how selecting premises, linking information, distinguishing a case from a rule, and ordering the answer can make an explanation usable. They are examples for judgment, not mandatory patterns or evaluation prompts. The main Skill contains the required workflow.

## A measured change is not yet a causal effect

Question: "The old process took 10 minutes and the trial took 6. Did the new process save 4 minutes?"

- **Unsupported leap:** "Yes, the new process saved 4 minutes." The two durations alone do not establish that the process caused the difference.
- **Excess detail:** A long introduction to sampling theory and statistical tests can bury the immediate decision: were the cases comparable?
- **Useful explanation:** "The trial case took 6 minutes, 4 minutes less than the earlier case. Because the cases were different, that comparison alone cannot show that the new process caused the reduction. To assess the process, compare similar cases or account for the differences between them."

The general point is about a missing comparison condition, not a rule that all explanations need numbers or a statistical lesson. If the cases *were* comparable, the explanation should say what supports that judgment and avoid claiming more precision than the evidence permits.

## Connect a decision to its local rule

Question: "Why is another review optional?" Given facts: this branch requires one approval; someone else has already approved it.

- **Gap:** "Someone else approved it, so another review is optional." A reader outside the conversation may not know how many approvals are required.
- **Connected explanation:** "This branch requires one approval. It has already received one from another reviewer, so an additional review is optional under that rule."

The one-approval threshold is necessary here even for a reader who understands code review generally. An overview of every review policy is not.

## Keep an example in its own scope

Question: "Does a trial extension apply to every member?" Given facts: members who enrolled before June receive a one-month extension; the example member enrolled in May. No rule for later enrollments was provided.

A useful answer states the rule, then applies it: "The extension applies to members who enrolled before June. The member who enrolled in May qualifies under that rule. The supplied information does not establish whether people who enrolled in June or later can receive a different extension."

The May example does not expand the rule to every member. The absent later-enrollment rule is a limit on this answer, not a reason to invent a policy.

## Order information around the reader's task

Question: "How do I get access after approval?" Given steps: approval is recorded, an administrator grants access, and the user receives an invitation email. Background notes contain several meetings about why the process changed.

For this reader, the process sequence belongs in the explanation: after approval is recorded, the administrator grants access, then an invitation email arrives. The meeting history does not help the reader understand the sequence and should be omitted unless the request asks why the process changed. If the time to invitation is unknown, do not promise one.

## Explain a mechanism without teaching unrelated basics

Question: "Why can a cached result be stale after an update?" The reader knows what a cache is. Given facts: updates change the source record; cached copies are refreshed every five minutes.

A useful answer connects the two: "An update changes the source record immediately, but a cached copy may still hold the earlier value until its next refresh, which occurs every five minutes. During that interval, a read from the cache can return the older value." A general tutorial on caching is unnecessary. This example assumes reads may use that cache; if that fact is not established in the actual task, check it before claiming the observed read came from the cache.
