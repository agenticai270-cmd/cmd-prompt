# cmd-prompt reviewer notes

## Architecture

This is a beginner-friendly library-management CLI with parallel Python and Java implementations under `library_management/`. The Python implementation is the feature-rich version: `Library` owns books, members, loans, validation, reporting, CSV export, and JSON persistence in `library_manager.py`. The Java implementation is a smaller standalone CLI using serializable lists and `library_data_java.bin`; it is not a direct feature-for-feature equivalent.

## Conventions

- Python domain entities are `@dataclass` records: `Book`, `Member`, and `Loan` in `library_management/library_manager.py`.
- Python IDs are integer dictionary keys generated with `_next_id`, using `max(items, default=0) + 1`; operations resolve missing entities through `_require_book` and `_require_member`.
- Mutating Python operations validate inputs, update in-memory state, call `save()`, and return the affected entity where applicable. Examples include `add_book`, `update_member`, `borrow_book`, and `return_book`.
- Persistence is JSON-backed and versioned (`"version": 2`); writes use a sibling `.tmp` file followed by `replace()` for safer replacement (`library_manager.py`).
- Dates are persisted as ISO strings and converted with `date.fromisoformat`; loan date inputs remain injectable for deterministic tests (`borrowed_on` and `returned_on`).
- Book inventory tracks both total `copies` and `available_copies`. Updating copies must preserve the number currently borrowed; removing books or members is blocked when active loans exist.
- Validation uses `ValueError` with user-facing messages, including required text via `_text`, positive quantities via `_positive`, and explicit role/email checks (`library_manager.py`).
- Tests use Python’s standard `unittest`, temporary directories, and regex assertions on validation messages (`library_management/test_library_manager.py`).
- The Python CLI is run from the `library_management` directory; the Java version is compiled and run independently as documented in `library_management/README.md`.

## Intentional non-standard choices

- The Java implementation intentionally remains a simpler legacy-style feature set: one borrower per book, no loan history, roles, fines, renewals, categories, reports, or CSV export (`library_management/LibraryManager.java`). Do not flag its lack of parity with Python unless the change explicitly targets parity.
- Python saves after nearly every mutation and also saves after legacy migration; this is deliberate automatic persistence rather than a separate transaction layer.
- Legacy JSON containing a book-level `borrowed_by` field is intentionally migrated into an open `Loan` (`_migrate_legacy_loans`), preserving compatibility with older data.

## Watch out for

- Changes to loan state must keep `Book.available_copies` synchronized with open loans; borrowing decrements it and returning increments it.
- Do not bypass validation or persistence in new mutating `Library` methods.
- Preserve migration behavior for old records lacking `category`, `copies`, or `available_copies`, and avoid creating duplicate open loans during repeated loads.
- Be careful when changing copy counts: `update_book` rejects totals below currently borrowed copies.
- Tests and callers may depend on exact or partial error text such as `"not available"`, `"active loans"`, `"inactive"`, and `"Email"` (`test_library_manager.py`).
- Avoid treating the Java serialized file and Python JSON file as interchangeable; they are separate formats and paths.