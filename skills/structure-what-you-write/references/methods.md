# Methods and principles behind information-centered writing

Use this reference when a structural choice needs a reasoned method, not only a formatting convention.\
It summarizes ideas adapted from primary standards, official descriptions of methods, and guides that their publishers maintain.\
The methods can be used together, and this Skill does not claim formal conformance to any of them.

## Information Mapping: identify the question of the reader and the information unit

**Core idea**: analyze information by the question that it answers, arrange it in accessible blocks, and label the blocks so that readers can find them.

The provider of Information Mapping identifies six information types:

| Information Mapping type | Question of the reader |
| --- | --- |
| Procedure | How do I do it? |
| Process | What happens, and how does it work? |
| Structure | What are its components? |
| Principle | What rule or guidance applies? |
| Concept | What is this? |
| Fact | What is known? |

### Information Mapping principles

Information Mapping also gives six organizing principles that can inform the writing decisions here.

| Principle | Practical question for this Skill |
| --- | --- |
| Chunking | Is the content divided into manageable, meaningful units? |
| Relevance | Does each unit contain information that belongs to its subject and to the task of the reader? |
| Labeling | Can readers infer the content and the scope of a unit from its name? |
| Consistency | Do comparable units use compatible terms and patterns? |
| Integrated graphics | Do tables and diagrams make the content next to them clearer? |
| Accessible detail | Can readers reach the details that they need, without irrelevant details in every step? |

These principles guide organization and retrieval.\
They set no fixed maximum for the number of items in a list.\
The list follows the published summary of six principles by the provider.\
Other descriptions of the historical method can count or group the principles differently.

**Apply when**: a paragraph, list, or section mixes descriptions, steps, rules, examples, and reference facts, and does not show their differences.

- Identify the question of the reader before you choose the grouping.
- Choose a unit that can have a meaningful label, and that serves a task of the reader.
- Group closely related conditions, definitions, and examples, even when the blocks become longer.
- Use a recognizable format for repeated information, when the task of the reader supports it.
- Use labels that describe the information in the unit, not its location in the source or its history.

**Limit**: the six types are part of the method of Information Mapping.\
This Skill uses them as aids, not as a complete classification for all writing.\
Narrative, persuasive, social, and mixed writing can need other distinctions.\
The layout conventions of the vendor are optional for Markdown artifacts.

**Sources**: [Information Mapping: Methodology](https://informationmapping.com/pages/information-mapping-methodology); [Information Mapping: Six organizing principles](https://informationmapping.com/blogs/news/conquering-documentation-debt); [Information Mapping: Types](https://support.informationmapping.com/hc/en-us/articles/213446789-Present-your-information-in-a-clear-and-consistent-way); [Information Mapping: Maps and Blocks](https://support.informationmapping.com/hc/en-us/articles/213440709-Structure-your-content-using-Maps-and-Blocks).

## DITA: separate information types from assembly

**Core idea**: DITA separates topic types, such as concept, task, and reference.\
It also separates the authored topics from the maps that organize them into deliverables.

- Concept topics explain what something is.
- Task topics help someone do a task.
- Reference topics give precise facts to look up.
- Topics are meaningful units of authoring, and maps show the hierarchy and the relationships of topics.

**Apply when**: you define independent fields, document procedures, separate current facts from explanation, or restructure a large set of files.

- Use the difference between a concept, a task, and a reference to find sections with mixed purposes.
- Consider whether one topic needs its own section or file.\
  A topic and a file are different units.
- Decide the navigation and the order of presentation for the whole set of artifacts, when necessary.
- Keep a topic self-contained when readers must use it directly, not only through a parent document.

**Limit**: DITA is an XML architecture with its own exact constraints.\
These heuristics apply to Markdown as it is, without XML tags or a fixed template of three types.

**Sources**: [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing); [The topic as the basic unit of information](https://dita-lang.org/2.0/dita/archspec/base/topicdefined); [Definition of DITA maps](https://dita-lang.org/2.0/dita/archspec/base/definition-of-ditamaps).

## Diátaxis: distinguish what readers try to do

**Core idea**: four forms of technical documentation support different needs of readers.

| Form | Need of the reader | Main function |
| --- | --- | --- |
| Tutorial | Learn by doing | Lead a guided learning experience |
| How-to | Achieve a goal | Guide practical action |
| Reference | Find precise information | Describe facts and machinery |
| Explanation | Understand a topic | Give context and reasons |

**Apply when**: a README, guide, reference page, or instruction set tries to teach, instruct, list, and justify everything at the same time.

- Identify the main job of the reader that the current artifact serves.
- Move largely independent instructions or explanations to a better section or destination, when the reader benefits.
- Keep short context inside a procedure when the reader needs it to do the steps.
- Link to supporting detail, so that each reader can choose to read it.

**Limit**: split a document with mixed purposes only when the split helps the reader, not into four files by default.\
A short message or an agent task can correctly contain definitions, instructions, and safeguards, because the combined unit serves one concrete task.

**Sources**: [Diátaxis: Start here](https://diataxis.fr/start-here/); [Diátaxis map](https://diataxis.fr/map/).

## Google Technical Writing: organize before polishing

**Core idea**: a useful outline, informative headings, focused paragraphs, parallel list items, and meaningful tables make information easier to scan and use.

- Give a paragraph one coherent topic, and let the topic set its length.
- Keep list items parallel in logical category as well as in grammar.
- Use numbered lists when the order changes the meaning, and bullets in other cases.
- Use tables for repeated records with several attributes and for lookup.\
  Use a list for a simple inventory with one column.
- Choose between one large document and several linked documents by the needs of the readers, not by file length.
- Make the content and the scope of headings predictable.

**Apply when**: a document contains dense enumerations inside sentences, arbitrary groups of bullets, misleading headings, or weak section boundaries.

**Limit**: these editing heuristics are guidance.\
When a short paragraph or a comparison of two columns serves the reader better, use it.\
Use it even when another form is possible.

**Sources**: [Lists and tables](https://developers.google.com/tech-writing/one/lists-and-tables); [Paragraphs](https://developers.google.com/tech-writing/one/paragraphs); [Organizing large documents](https://developers.google.com/tech-writing/two/large-docs); [Tables](https://developers.google.com/style/tables).

## Plain language and ISO 24495-1: test the result for the reader

**Core idea**: plain-language practice asks whether the intended readers can get, find, understand, and use the relevant information.\
The International Plain Language Federation summarizes ISO 24495-1:2023 with four governing principles:

- **Relevant**: readers get what they need, not all available content.
- **Findable**: readers can find information at the moment that they use it.
- **Understandable**: readers can understand the meaning, the conditions, and the relationships.
- **Usable**: readers can decide or act with the information.

**Apply when**: a structure looks tidy, but it still burdens the reader, omits prerequisites, shows irrelevant drafting history, or scatters necessary conditions.

**Limit**: these are criteria for the result.\
They do not require short sentences, headings, or tables for all content.\
The published ISO standard contains more detail than this summary, and this file does not reproduce its normative text.

**Sources**: [ISO 24495-1:2023](https://www.iso.org/standard/78907.html); [International Plain Language Federation: ISO standard](https://www.iplfederation.org/iso-standard/).

## W3C WAI: represent the hierarchy semantically

**Core idea**: heading levels show the structure of the content, and they enable navigation, also for assistive technologies.\
A heading at the same level starts a new peer section, and a heading at a lower level starts a subsection.

**Apply when**: subtopics that need a meaningful shared parent appear as unrelated peer headings, or heading sizes chosen for appearance distort the containment.

- Choose heading levels by containment, not by the font size that you want.
- Use descriptive titles that match the actual scope of the information.
- When you add a subsection, use the next level below its parent.

**Limit**: heading markup alone cannot repair incorrect grouping or misplaced content.\
Determine the semantic relationships first.

**Source**: [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/).

## Resolve conflicting recommendations

1. Keep the applicable requirements, the needs of the readers, the facts, and the permissions before you improve the presentation.
2. Identify whether the problem is content selection, information type, grouping, hierarchy, placement, or formatting.
3. Compare the relevant methods only at the level that each one addresses.
4. Choose the option that helps readers find, understand, and use accurate information with the least reconstruction and navigation.
5. Verify that the chosen structure keeps the meaning, the required context, the accessibility, and the independent use.

The actual task of the reader and the constraints of the destination medium take precedence over each method.\
These combined decision rules are the design of this Skill, not a quotation from one source.
