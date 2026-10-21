# cmd-prompt reviewer notes

## Architecture

A beginner-friendly Python CLI for managing books, members, and borrowing records. Core domain logic lives in `library_management/library_manager.py`, with `Library` owning in-memory state and JSON persistence; the same file contains CLI presentation and input handling. Tests in `library_management/test_library_manager.py` use only Python’s standard `unittest` and temporary JSON files.

## Conventions

- Use dataclasses for persisted domain entities: `Book` and `Member` in `library_management/library_manager.py`; serialize them with `dataclasses.asdict`.
- Keep books and members indexed by integer IDs in dictionaries (`dict[int, Book]` and `dict[int, Member]`), while JSON stores lists and converts IDs back to integers in `_load()`.
- Domain operations validate inputs and raise `ValueError` with user-facing messages. Examples include required text checks in `add_book()` and `register_member()`, and existence/state checks in `borrow_book()` and `return_book()`.
- Normalize user-provided text at the boundary with `.strip()`. Book searches additionally lowercase both query and searchable fields (`search_books()`).
- Mutating operations persist immediately by calling `self.save()` after successful changes. New persistence paths are created with `mkdir(parents=True, exist_ok=True)`.
- Keep CLI interaction in `run_cli()` and presentation helpers such as `display_books()`, while library behavior remains callable independently for tests.
- Tests construct `Library` with a temporary path (`test_library_manager.py`) rather than using the default `library_data.json`; follow this pattern to avoid filesystem pollution.
- Use standard-library typing and modern annotations, including `from __future__ import annotations` and `int | None`.

## Intentional non-standard choices

- Persistence is deliberately simple JSON rather than a database. The default file is relative to the process working directory (`library_data.json`), as documented in `library_management/README.md`.
- `Library` auto-loads in `__init__` and auto-saves every successful mutation; callers do not need an explicit transaction or save step.
- CLI and domain code share one module; this is intentional for the small beginner-focused application.
- The CLI catches both validation/input `ValueError` and malformed JSON (`json.JSONDecodeError`) and prints an error instead of terminating.

## Watch out for

- Do not bypass validation or mutate `books`, `members`, or `borrowed_by` without saving; that breaks the persistence contract.
- Preserve the distinction between missing IDs and invalid borrowing state, since tests and CLI messages rely on the specific `ValueError` cases.
- When changing JSON fields or dataclasses, update both `_load()` reconstruction and `save()` serialization, plus persistence tests.
- Avoid using the default data file in tests; use `TemporaryDirectory` as in `test_library_manager.py`.
- Be careful with truthiness checks for IDs or state display: `display_books()` uses `if book.borrowed_by`; current IDs start at 1, so changing ID semantics could make this incorrect.