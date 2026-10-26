# Commit Types Reference

This file is an original summary for this repository.\
The message structure and the meaning of the types are based on the [Conventional Commits specification](https://www.conventionalcommits.org) (CC BY 3.0).

Use this reference when the type, a breaking-change marker, the body, or a footer is not obvious.\
An explicit convention of the target repository takes precedence over this reference.

## Decision sequence

1. Identify the confirmed main intent of the commit from the request and the evidence.\
   The file extension and the syntax show only what changed.
2. Identify the effect that a user or a consumer can see.
3. Decide whether the change keeps backward compatibility.
4. Apply the rules of the target repository for type, scope, release, and language.
5. Select the type, and decide whether the message needs a body, a footer, or a breaking-change marker.

If missing intent leaves two possible types, ask the user, or mark the type `Unresolved`.

## Common types

| Type | Main intent | Evidence that identifies it |
| --- | --- | --- |
| `feat` | Add a new capability or supported behavior | A consumer can do a new, intended thing |
| `fix` | Restore behavior that should already work | An existing expectation, contract, or documented behavior was broken |
| `refactor` | Improve the internal structure, and keep the observable behavior | The public behavior and the compatibility stay the same |
| `perf` | Improve performance, and keep the intended result | Time, memory, throughput, or resource use is the main change |
| `docs` | Change only documentation or comments | No product, build, test, or operational behavior changes, under the convention of the repository |
| `test` | Add or change tests, and keep the production behavior | Test coverage or test infrastructure is the main change |
| `build` | Change the build system, packaging, or dependencies | The construction of artifacts or the resolution of dependencies is the main change |
| `ci` | Change the configuration or automation of continuous integration | The execution of CI is the main change |
| `style` | Change formatting without a change of meaning | Whitespace, formatting, or other code changes that affect only presentation |
| `chore` | Do repository maintenance that no more specific type covers | The convention of the repository allows `chore` for that maintenance |

A repository can define different or additional meanings.\
For example, a repository can treat a Skill, a schema, a configuration file, or a document as a product surface.\
Then a change of its behavior is `feat` or `fix`, whatever the filename is.

## Unclear cases

- **A null guard**:

  - `fix`: it restores an existing expectation.
  - `feat`: it accepts input as new supported behavior.
  - `refactor`: the observable behavior stays the same on purpose.

- **A dependency update**: the type of its main effect on the product, when the convention of the repository requires that.\
  `build` is not automatic.

- **A change of UI appearance**:

  - `feat`: it changes the experience on purpose.
  - `fix`: it repairs a defect.
  - `style`: it is code formatting with no visible effect.

- **A move or a rename of files**: `refactor` only when the structure is the main purpose and the behavior stays the same.\
  Otherwise, the type of the behavior that the move delivers.

- **Generated files, lockfiles, and documentation**: they can go in the same commit as the behavior that they support, when they are inseparable results of it.

## Breaking changes

A breaking change makes an incompatible change to a public API, schema, configuration contract, supported environment, data format, migration requirement, or other expectation of consumers.

Mark it in one of these two ways:

```text
feat(api)!: remove the legacy endpoint
```

```text
feat(api): replace the legacy endpoint

BREAKING CHANGE: clients must migrate from `/v1/legacy` to `/v2/current`.
```

The breaking-change marker is independent of the type.\
A `fix`, a `refactor`, or another allowed type can also be breaking.

## Body and footers

Add a body when the subject cannot hold the context for a decision.\
Examples are why the change was necessary, how two changes relate, and what migration is necessary.\
Keep the subject short, and put the body after a blank line.

Add footers for the structured metadata that the target workflow requires, such as these:

- `BREAKING CHANGE: <description>`
- `Refs: #123`
- another trailer that the repository explicitly requires

Add only the Issue references, co-author lines, release notes, and other trailers that evidence or repository policy supports.
