# Methods and principles behind information-centered writing

Use this reference when a structural choice needs a reasoned method, not just a formatting convention.
It summarizes ideas adapted from primary standards, official method descriptions, and publisher-maintained guides.
These methods are not mutually exclusive, and this Skill does not claim formal conformance to any of them.

## Information Mapping: identify the reader question and information unit

**Core idea:** Analyze information by the question it answers, arrange it in accessible blocks, and label blocks so readers can locate them.

The Information Mapping provider identifies six information types:

| Information Mapping type | Reader question |
| --- | --- |
| Procedure | How do I do it? |
| Process | What happens, and how does it work? |
| Structure | What are its components? |
| Principle | What rule or guidance applies? |
| Concept | What is this? |
| Fact | What is known? |

### Information Mapping principles

Information Mapping also presents six organizing principles that can inform the writing decisions here.

| Principle | Practical question for this Skill |
| --- | --- |
| Chunking | Has the content been divided into manageable, meaningful units? |
| Relevance | Does each unit contain information that belongs to its subject and reader task? |
| Labeling | Can readers infer a unit's contents and scope from its name? |
| Consistency | Are comparable units represented using compatible terms and patterns? |
| Integrated graphics | Do tables and diagrams clarify the adjacent content rather than stand apart as decoration? |
| Accessible detail | Can readers reach needed details without carrying irrelevant detail through every step? |

These principles are guidance for organization and retrieval, not a rule to cap every list at a fixed number of items.
The list reflects the provider's published six-principle summary; other descriptions of the historical method may count or group principles differently.

**Apply when:** A paragraph, list, or section mixes descriptions, steps, rules, examples, and reference facts without signaling their differences.

- Identify the reader question before choosing the grouping.
- Choose a unit that can be meaningfully labeled and consumed for a reader task.
- Group closely related conditions, definitions, and examples; do not fragment solely to make blocks shorter.
- Prefer a recognizable format for repeated information, while checking whether the actual reader task justifies it.
- Use labels that describe the contained information rather than labels derived from source location or production history.

**Limit:** The six types are part of Information Mapping's method, not an exhaustive ontology this Skill imposes on all writing.
Narrative, persuasive, social, and hybrid writing may need other distinctions.
Avoid treating vendor-specific layout conventions as mandatory for Markdown artifacts.

**Sources:** [Information Mapping: Methodology](https://informationmapping.com/pages/information-mapping-methodology); [Information Mapping: Six organizing principles](https://informationmapping.com/blogs/news/conquering-documentation-debt); [Information Mapping: Types](https://support.informationmapping.com/hc/en-us/articles/213446789-Present-your-information-in-a-clear-and-consistent-way); [Information Mapping: Maps and Blocks](https://support.informationmapping.com/hc/en-us/articles/213440709-Structure-your-content-using-Maps-and-Blocks).

## DITA: separate information types from assembly

**Core idea:** DITA distinguishes topic types such as concept, task, and reference, and separates authored topics from the maps that organize them into deliverables.

- Concept topics explain what something is.
- Task topics help someone accomplish a task.
- Reference topics supply precise facts for lookup.
- Topics are meaningful units of authoring; maps represent hierarchy and relationships among topics.

**Apply when:** Defining independent fields, documenting procedures, separating current facts from explanation, or restructuring a large set of files.

- Use the distinction between explaining a concept, prescribing a task, and presenting a reference to detect mixed-purpose sections.
- Consider whether one topic needs an independent section or file, but do not equate topic with file.
- Decide navigation and presentation order at the artifact-collection level when necessary.
- Keep a topic self-contained when it must be usable directly, not only through a parent document.

**Limit:** DITA is an XML architecture with its own exact constraints.
These heuristics do not require converting Markdown to DITA, using XML tags, or applying a fixed three-type template to every piece of writing.

**Sources:** [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing); [The topic as the basic unit of information](https://dita-lang.org/2.0/dita/archspec/base/topicdefined); [Definition of DITA maps](https://dita-lang.org/2.0/dita/archspec/base/definition-of-ditamaps).

## Diátaxis: distinguish what readers are trying to do

**Core idea:** Four forms of technical documentation support different reader needs.

| Form | Reader need | Primary function |
| --- | --- | --- |
| Tutorial | Learn by doing | Lead a guided learning experience |
| How-to | Accomplish a goal | Guide practical action |
| Reference | Find precise information | Describe facts and machinery |
| Explanation | Understand a topic | Provide context and reasons |

**Apply when:** A README, guide, reference page, or instruction set tries to teach, instruct, catalogue, and justify everything simultaneously.

- Determine which reader job the current artifact primarily serves.
- Move substantially independent instructional or explanatory material to a more suitable section or destination when the reader benefits.
- Allow concise context inside a procedure when execution requires it.
- Link to supporting detail rather than forcing every reader through it.

**Limit:** Do not split every mixed-purpose artifact into four files.
A short message or executable agent task may legitimately contain definitions, instructions, and safeguards because the combined unit serves one concrete task.

**Sources:** [Diátaxis: Start here](https://diataxis.fr/start-here/); [Diátaxis map](https://diataxis.fr/map/).

## Google Technical Writing: organize before polishing

**Core idea:** A useful outline, informative headings, focused paragraphs, parallel list items, and meaningful tables make information easier to scan and act on.

- Focus a paragraph on one coherent topic instead of limiting it by an arbitrary sentence count.
- Keep list items parallel in logical category as well as grammar.
- Use numbered lists when order changes meaning; otherwise consider bullets.
- Prefer tables for repeated multi-attribute records and lookup; avoid them for a simple one-column inventory or page layout.
- Compare a large standalone document with a set of smaller linked documents on reader needs, not file length alone.
- Make the content and scope of headings predictable.

**Apply when:** A document contains dense run-in enumerations, arbitrary bullet groupings, misleading headings, or ineffective section boundaries.

**Limit:** Editing heuristics are not laws.
If a short paragraph or two-column comparison better serves the actual reader, use it even when another form could be mechanically constructed.

**Sources:** [Lists and tables](https://developers.google.com/tech-writing/one/lists-and-tables); [Paragraphs](https://developers.google.com/tech-writing/one/paragraphs); [Organizing large documents](https://developers.google.com/tech-writing/two/large-docs); [Tables](https://developers.google.com/style/tables).

## Plain language and ISO 24495-1: test the outcome for the reader

**Core idea:** Plain-language practice asks whether intended readers can get relevant information, find it, understand it, and use it.
The International Plain Language Federation summarizes ISO 24495-1:2023 around four governing principles:

- **Relevant:** Readers get what they need, not an indiscriminate dump of available content.
- **Findable:** Readers can locate information at the moment of use.
- **Understandable:** The meaning, conditions, and relationships can be understood.
- **Usable:** Readers can decide or act with the information.

**Apply when:** A structure looks tidy but still burdens the reader, omits prerequisites, exposes irrelevant drafting history, or scatters needed conditions.

**Limit:** These are outcome criteria, not a prescription that every piece of content must use short sentences, headings, or tables.
The published ISO standard contains more detail than this summary; the full normative text is not reproduced here.

**Sources:** [ISO 24495-1:2023](https://www.iso.org/standard/78907.html); [International Plain Language Federation: ISO standard](https://www.iplfederation.org/iso-standard/).

## W3C WAI: represent the hierarchy semantically

**Core idea:** Heading levels represent the structure of the content and enable navigation, including for assistive technologies.
An equal-level heading begins a new peer section, while a lower-level heading begins a subsection of a higher-level section.

**Apply when:** Subtopics that should share a meaningful parent are presented as unrelated peer headings, or decorative heading sizes distort containment.

- Choose levels according to containment, not desired font size.
- Use descriptive titles that match the actual information scope.
- Avoid skipping levels for newly introduced subsections when possible.

**Limit:** Heading markup alone cannot repair incorrect grouping or misplaced content.
Determine the semantic relationships first.

**Source:** [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/).

## How to resolve conflicting recommendations

1. Preserve applicable requirements, reader needs, facts, and permissions before optimizing presentation.
2. Determine whether the problem is content selection, information type, grouping, hierarchy, placement, or formatting.
3. Compare the relevant methods only at the level they actually address.
4. Prefer the option that improves readers' ability to find, understand, and use accurate information with less reconstruction or unnecessary navigation.
5. Verify that the chosen structure does not lose meaning, required context, accessibility, or standalone behavior.

No single method overrides the reader's actual task or the destination medium's constraints.
These combined decision rules are the design of this Skill, not a quotation from any one source.
