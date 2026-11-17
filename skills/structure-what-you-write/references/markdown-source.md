# Default Markdown source conventions

Use this reference when you write or revise the source of a Markdown document.\
The conventions of the target repository or medium take precedence.\
Use these defaults only for the points that those conventions do not cover.

The defaults make the source show the structure of the information.\
A reader of the source can then see which lines form one unit, and which level each separation belongs to.

## Line breaks

Write all the sentences of one paragraph or one list item on one line.\
Join the sentences with spaces, not with a trailing `\` or other hard line breaks.\
A line for each sentence makes you build a paragraph or an item as a sequence of sentences, not as one subject.

## Content directly below a heading

Put only these forms directly below a heading:

- one introductory sentence
- a table
- a code block
- numbered steps
- a list of links to reference material

Write explanations and rules as items with bold labels.\
Indent the content of each label as child items below it.

## Labeled items

Use the form `- **Label**: value` only when each sibling item has one piece of content.\
When one sibling has more than one piece of content, give every sibling a label and child items.

**Mixed forms:**

````markdown
- **Scope**: the files under `docs/`.
- **Exceptions**: the generated files. Also the files that a tool owns.
````

**One form for all siblings:**

````markdown
- **Scope**

  - The files under `docs/`.

- **Exceptions**

  - The generated files.
  - The files that a tool owns.
````

## Blank lines

Put blank lines so that each blank line shows one level of separation:

- Put a blank line before and after each item that has children.\
  This applies to an item with or without a label, at every depth.
- Put a blank line between the text of such an item and its first child.
- Write items that have no children on consecutive lines, without blank lines.

## Steps

Write the steps of a procedure as numbered steps by default.\
Give each step its own heading, with its number in the heading, such as `### 3. Build the archive`, when one of these conditions applies:

- The step contains a table, a code block, or several paragraphs.
- The content of the step needs deep indentation inside a list item.
- Other text refers to the step, and a link to the step helps the reader.
- Readers find the steps through an outline of the headings.

Inside a step heading, keep the details as labeled items.\
Use a heading of a lower level only when the content of the step needs separate sections.\
These choices apply to the procedure of the document.\
An output format that the procedure describes, such as the body of a pull request, follows its own conventions.
