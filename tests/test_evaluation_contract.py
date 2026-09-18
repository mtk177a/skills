import unittest

from scripts.evaluation_contract import (
    EvaluationContractError,
    normalize_evaluation_document,
)


def behavior_case(**changes: object) -> dict[str, object]:
    case: dict[str, object] = {
        "id": "case-1",
        "prompt": "Handle the request.",
        "expected_output": "A bounded result.",
    }
    case.update(changes)
    return case


def definition(case: dict[str, object]) -> dict[str, object]:
    return {"skill_name": "alpha-skill", "evals": [case]}


class EvaluationContractTests(unittest.TestCase):
    def normalize(
        self, case: dict[str, object], definition_kind: str = "behavior"
    ) -> dict[str, object]:
        return normalize_evaluation_document(
            definition(case),
            expected_skill="alpha-skill",
            definition_kind=definition_kind,
        )

    def test_normalizes_the_four_supported_input_forms(self) -> None:
        cases = (
            (
                behavior_case(prompt="Current request."),
                "single-turn",
                "Current request.",
            ),
            (
                behavior_case(
                    prompt=None,
                    turns=[
                        {"role": "user", "content": "First."},
                        {"role": "assistant", "content": "Second."},
                        "Third.",
                    ],
                ),
                "transcript",
                "User turn 1:\nFirst.\n\nAssistant turn 2:\nSecond.\n\nUser turn 3:\nThird.",
            ),
            (
                behavior_case(
                    prompt=None,
                    authoring_turns=["Draft the document."],
                    request="Review it with fresh eyes.",
                ),
                "authoring-transcript",
                "Prior authoring conversation:\n\nUser turn 1:\nDraft the document."
                "\n\nCurrent request:\nReview it with fresh eyes.",
            ),
            (
                behavior_case(
                    conversation=["We selected option A."],
                    prompt="Continue the implementation.",
                ),
                "conversation",
                "Conversation so far:\n\nUser turn 1:\nWe selected option A."
                "\n\nCurrent user request:\nContinue the implementation.",
            ),
        )
        for case, input_mode, prompt in cases:
            case = {key: value for key, value in case.items() if value is not None}
            with self.subTest(input_mode=input_mode):
                normalized = self.normalize(case)["cases"][0]
                self.assertEqual(input_mode, normalized["input_mode"])
                self.assertEqual(prompt, normalized["prompt"])

    def test_preserves_a_non_empty_title_in_the_normalized_case(self) -> None:
        normalized = self.normalize(behavior_case(title="Descriptive case"))

        self.assertEqual("Descriptive case", normalized["cases"][0]["title"])

        with self.assertRaisesRegex(EvaluationContractError, "title must be a non-empty string"):
            self.normalize(behavior_case(title=""))

    def test_rejects_unknown_fields_at_every_object_level(self) -> None:
        documents = (
            {**definition(behavior_case()), "schema_version": 1},
            {
                **definition(behavior_case()),
                "execution": {"coexistence_skills": [], "timeout": 1},
            },
            definition(behavior_case(unused=True)),
            definition(
                behavior_case(
                    assertions=[
                        {"id": "a", "text": "A.", "critical": True, "weight": 1}
                    ]
                )
            ),
            definition(
                behavior_case(
                    prompt=None,
                    turns=[{"role": "user", "content": "Request.", "name": "author"}],
                )
            ),
            definition(
                behavior_case(fixture={"files": {"input.txt": "text"}, "name": "fixture"})
            ),
        )
        for document in documents:
            document["evals"][0] = {
                key: value for key, value in document["evals"][0].items() if value is not None
            }
            with self.subTest(document=document):
                with self.assertRaisesRegex(EvaluationContractError, "unknown field"):
                    normalize_evaluation_document(
                        document,
                        expected_skill="alpha-skill",
                        definition_kind="behavior",
                    )

    def test_rejects_incomplete_or_mixed_input_forms(self) -> None:
        invalid_cases = (
            {"id": "missing", "expected_output": "Result."},
            behavior_case(turns=["Duplicate input."]),
            behavior_case(request="Missing authoring history."),
            behavior_case(authoring_turns=["Missing request."], prompt=None),
            behavior_case(conversation=["History."], turns=["Current."]),
        )
        for case in invalid_cases:
            case = {key: value for key, value in case.items() if value is not None}
            with self.subTest(case=case):
                with self.assertRaisesRegex(EvaluationContractError, "exactly one supported input form"):
                    self.normalize(case)

    def test_rejects_invalid_turn_roles_and_empty_content(self) -> None:
        invalid_turns = (
            [{"role": "system", "content": "Instruction."}],
            [{"role": "user", "content": ""}],
            [],
        )
        for turns in invalid_turns:
            with self.subTest(turns=turns):
                case = behavior_case(prompt=None, turns=turns)
                case.pop("prompt")
                with self.assertRaises(EvaluationContractError):
                    self.normalize(case)

    def test_rejects_duplicates_in_set_like_arrays(self) -> None:
        cases = (
            behavior_case(conditions=["candidate", "candidate"]),
            behavior_case(coexistence_skills=["beta-skill", "beta-skill"]),
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaisesRegex(EvaluationContractError, "duplicates"):
                    self.normalize(case)

        routing = behavior_case(expected_handlers=["alpha-skill", "alpha-skill"])
        with self.assertRaisesRegex(EvaluationContractError, "duplicates"):
            self.normalize(routing, "routing")

        with self.assertRaisesRegex(EvaluationContractError, "duplicates"):
            normalize_evaluation_document(
                {
                    "skill_name": "alpha-skill",
                    "execution": {"coexistence_skills": ["beta-skill", "beta-skill"]},
                    "evals": [behavior_case()],
                },
                expected_skill="alpha-skill",
                definition_kind="behavior",
            )

    def test_rejects_unsafe_and_duplicate_normalized_paths(self) -> None:
        for files in (["../outside.txt"], ["input.txt", "folder/../input.txt"], ["a//b", "a/b"]):
            with self.subTest(files=files):
                with self.assertRaises(EvaluationContractError):
                    self.normalize(behavior_case(files=files))

        for fixture in (
            {"files": {".git/config": "unsafe"}},
            {"files": {"a//b": "first", "a/b": "second"}},
        ):
            with self.subTest(fixture=fixture):
                with self.assertRaises(EvaluationContractError):
                    self.normalize(behavior_case(fixture=fixture))

    def test_rejects_nul_in_case_and_fixture_paths(self) -> None:
        cases = (
            behavior_case(files=["inputs/bad\0name.txt"]),
            behavior_case(fixture={"files": {"bad\0name.txt": "content"}}),
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaisesRegex(EvaluationContractError, "unsafe case input path"):
                    self.normalize(case)

    def test_rejects_fixture_file_and_directory_path_conflicts(self) -> None:
        fixtures = (
            {"files": {"a": "file", "a/b": "nested"}},
            {"files": {"a/b": "nested", "a": "file"}},
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                with self.assertRaisesRegex(
                    EvaluationContractError, "fixture file paths conflict: `a` and `a/b`"
                ):
                    self.normalize(behavior_case(fixture=fixture))

        normalized = self.normalize(
            behavior_case(fixture={"files": {"a": "first", "ab": "second"}})
        )
        self.assertEqual({"a": "first", "ab": "second"}, normalized["cases"][0]["inline_files"])

    def test_rejects_case_and_fixture_files_with_the_same_materialized_path(self) -> None:
        with self.assertRaisesRegex(
            EvaluationContractError,
            "case file `source.txt` and fixture file `inputs/source.txt` conflict",
        ):
            self.normalize(
                behavior_case(
                    files=["source.txt"],
                    fixture={"files": {"inputs/source.txt": "inline"}},
                )
            )

    def test_rejects_case_and_fixture_file_directory_conflicts(self) -> None:
        cases = (
            (
                behavior_case(
                    files=["source.txt"],
                    fixture={"files": {"inputs": "inline"}},
                ),
                "case file `source.txt` and fixture file `inputs` conflict",
            ),
            (
                behavior_case(
                    files=["source.txt"],
                    fixture={"files": {"inputs/source.txt/nested.txt": "inline"}},
                ),
                "case file `source.txt` and fixture file `inputs/source.txt/nested.txt` conflict",
            ),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                with self.assertRaisesRegex(EvaluationContractError, expected):
                    self.normalize(case)

    def test_case_and_fixture_conflict_diagnostic_is_stable(self) -> None:
        cases = (
            behavior_case(
                files=["z.txt", "source.txt"],
                fixture={"files": {"z-inline.txt": "other", "inputs/source.txt": "inline"}},
            ),
            behavior_case(
                files=["source.txt", "z.txt"],
                fixture={"files": {"inputs/source.txt": "inline", "z-inline.txt": "other"}},
            ),
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaisesRegex(
                    EvaluationContractError,
                    "case file `source.txt` and fixture file `inputs/source.txt` conflict",
                ):
                    self.normalize(case)

    def test_accepts_non_conflicting_case_and_fixture_path_prefixes(self) -> None:
        normalized = self.normalize(
            behavior_case(
                files=["source.txt"],
                fixture={"files": {"inputs/source.txt.bak": "inline"}},
            )
        )["cases"][0]

        self.assertEqual(["source.txt"], normalized["files"])
        self.assertEqual(
            {"inputs/source.txt.bak": "inline"}, normalized["inline_files"]
        )

    def test_behavior_requires_grading_and_forbids_expected_handlers(self) -> None:
        with self.assertRaisesRegex(EvaluationContractError, "requires assertions or expected_output"):
            self.normalize({"id": "case-1", "prompt": "Request."})
        with self.assertRaisesRegex(EvaluationContractError, "must not define expected_handlers"):
            self.normalize(behavior_case(expected_handlers=[]))

    def test_rejects_null_optional_fields_instead_of_ignoring_them(self) -> None:
        cases = (
            behavior_case(assertions=["Requirement."], expected_output=None),
            behavior_case(fixture=None),
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(EvaluationContractError):
                    self.normalize(case)

    def test_routing_requires_handlers_and_accepts_an_empty_handler_list(self) -> None:
        with self.assertRaisesRegex(EvaluationContractError, "requires expected_handlers"):
            self.normalize(behavior_case(), "routing")

        normalized = self.normalize(
            {"id": "route", "prompt": "Do not route.", "expected_handlers": []},
            "routing",
        )

        requirement = normalized["cases"][0]["grading_requirements"][0]
        self.assertEqual("routing-handlers", requirement["id"])
        self.assertEqual([], requirement["expected_handlers"])

    def test_rejects_case_ids_that_collide_after_normalization(self) -> None:
        document = {
            "skill_name": "alpha-skill",
            "evals": [behavior_case(id=1), behavior_case(id="1")],
        }

        with self.assertRaisesRegex(EvaluationContractError, "duplicate case id `1`"):
            normalize_evaluation_document(
                document,
                expected_skill="alpha-skill",
                definition_kind="behavior",
            )

    def test_requires_the_definition_skill_to_match_a_valid_skill_name(self) -> None:
        for skill_name in ("other-skill", "Alpha Skill"):
            with self.subTest(skill_name=skill_name):
                with self.assertRaisesRegex(EvaluationContractError, "skill_name must be"):
                    normalize_evaluation_document(
                        {"skill_name": skill_name, "evals": [behavior_case()]},
                        expected_skill="alpha-skill",
                        definition_kind="behavior",
                    )


if __name__ == "__main__":
    unittest.main()
