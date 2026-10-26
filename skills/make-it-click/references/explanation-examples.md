# Explanation examples

These examples show four ways to make an explanation usable.\
The ways are to select premises, link facts, separate a case from a rule, and order the answer.\
They support judgment, and they are not required patterns or evaluation prompts.\
`SKILL.md` contains the workflow.

## A measured change is not yet a causal effect

Question: "The old process took 10 minutes and the trial took 6. Did the new process save 4 minutes?"

- **Unsupported leap**: "Yes, the new process saved 4 minutes."\
  The two durations alone do not show that the process caused the difference.
- **Too much detail**: a long introduction to sampling theory and statistical tests hides the immediate question: were the cases comparable?
- **Useful explanation**: "The trial case took 6 minutes, 4 minutes less than the earlier case. Because the cases were different, that comparison alone cannot show that the new process caused the reduction. To assess the process, compare similar cases or account for the differences between them."

The general point is a missing condition for the comparison.\
Explanations do not always need numbers or a lesson in statistics.\
If the cases were comparable, the explanation states what supports that judgment.\
It claims only the precision that the evidence supports.

## Connect a decision to its local rule

Question: "Why is another review optional?"\
Given facts: this branch requires one approval, and another person has already approved it.

- **Gap**: "Someone else approved it, so another review is optional."\
  A reader outside the conversation may not know how many approvals are required.
- **Connected explanation**: "This branch requires one approval. It has already received one from another reviewer, so an additional review is optional under that rule."

The rule of one approval is necessary here, even for a reader who knows code review in general.\
An overview of every review policy is not necessary.

## Keep an example in its own scope

Question: "Does a trial extension apply to every member?"\
Given facts: members who enrolled before June receive an extension of one month, and the example member enrolled in May.\
The facts give no rule for later enrollments.

A useful answer states the rule, and then applies it: "The extension applies to members who enrolled before June. The member who enrolled in May qualifies under that rule. The supplied information does not establish whether people who enrolled in June or later can receive a different extension."

The May example applies only to members who enrolled before June.\
The missing rule for later enrollments is a limit of this answer.\
State the limit, and leave the policy for later enrollments open.

## Order information around the task of the reader

Question: "How do I get access after approval?"\
Given steps: the approval is recorded, an administrator grants access, and the user receives an invitation email.\
The background notes describe several meetings about why the process changed.

For this reader, the explanation gives the sequence: after the approval is recorded, the administrator grants access, and then an invitation email arrives.\
The meeting history does not help the reader follow the sequence.\
Include it only when the request asks why the process changed.\
State a time for the invitation only when the time is known.

## Explain a mechanism without unrelated basics

Question: "Why can a cached result be stale after an update?"\
The reader knows what a cache is.\
Given facts: updates change the source record, and cached copies refresh every five minutes.

A useful answer connects the two facts: "An update changes the source record immediately, but a cached copy may still hold the earlier value until its next refresh, which occurs every five minutes. During that interval, a read from the cache can return the older value."

A general tutorial on caching is not necessary.\
This example assumes that reads can use that cache.\
If the actual task does not establish that fact, check it.\
Check it before you say that the observed read came from the cache.
