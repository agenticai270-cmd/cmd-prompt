# cmd-prompt reviewer notes

## Architecture

This repository contains a beginner-friendly library-management CLI implemented in both dependency-free Python and Java. The Python implementation is the feature-rich, JSON-backed domain layer: `Library` manages `Book`, `Member`, and `Loan` records, persistence, validation, reports, and CSV exports. `LibraryManager.java` is a simpler standalone CLI using Java serialization and separate storage, while `test_library_manager.py` exercises the Python implementation with temporary files.

## Conventions

- Python domain entities are `@dataclass` records: `Book`, `Member`, and `Loan` in `library_management/library_manager.py`.
- Python IDs are integer dictionary keys and are allocated with `_next_id`, using `max(items, default=0) + 1`; preserve this behavior when adding entities.
- Mutating Python operations validate inputs, update in-memory state, call `save()`, and return the affected object where useful. Examples include `add_book`, `register_member`, `borrow_book`, and `renew_loan`.
- Validation is centralized in helpers such as `_text`, `_positive`, `_require_book`, and `_require_member`; public operations raise `ValueError` with user-facing messages rather than defining custom exception types.
- Book availability is represented by both `copies` and `available_copies`. Borrowing decrements availability, returning increments it, and changing copy totals accounts for currently borrowed copies (`update_book`).
- Dates are persisted as ISO strings (`date.isoformat()`) and reconstructed with `date.fromisoformat`; loan durations and fines use `DEFAULT_LOAN_DAYS` and `DAILY_FINE`.
- JSON persistence serializes dataclasses with `asdict` and writes version `2` records containing `books`, `members`, and `loans` (`library_manager.py`).
- Tests use only the standard library’s `unittest`, create isolated `TemporaryDirectory` storage, and assert exact domain behavior and error-message fragments (`test_library_manager.py`).
- The Java CLI keeps its implementation self-contained in `LibraryManager.java`, uses private static helper methods, prompts through `ask`, and reports recoverable input/storage failures from `main`.

## Intentional non-standard choices

- The Java and Python versions are not feature-parity implementations. Java intentionally supports only basic books, members, borrowing, returning, and serialized storage; Python provides categories, multiple copies, roles, loan history, fines, renewals, reports, and exports.
- Python loading explicitly migrates legacy books containing `borrowed_by` into open `Loan` records (`_migrate_legacy_loans`); do not flag the compatibility branch or its automatic save as unnecessary complexity.
- Python persistence writes to a `.tmp` sibling and replaces the target (`save()`), rather than writing directly to the JSON file.
- Python allows a year of `0` because validation rejects only negative years; Java follows the same non-negative rule.

## Watch out for

- Do not introduce updates that allow `available_copies` to exceed `copies` or `copies` to fall below the number currently borrowed.
- Preserve protection against removing books with active loans and members with open loans.
- Ensure inactive members cannot borrow, and loan operations continue to reject missing books, members, or unavailable copies.
- When changing persisted fields, maintain compatibility with legacy JSON defaults handled by `_book_from_dict` and the `borrowed_by` migration.
- Avoid using the Java data file for Python or vice versa: Python uses `library_data.json`; Java uses `library_data_java.bin`.
- New Python behavior should be covered with the existing `unittest` style and temporary persistence files rather than relying on repository-local data.