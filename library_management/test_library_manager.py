import tempfile
import unittest
from pathlib import Path

from library_manager import Library


class LibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.library = Library(Path(self.temp_dir.name) / "data.json")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_search_and_persist_book(self) -> None:
        book = self.library.add_book("1984", "George Orwell", 1949)
        self.assertEqual(self.library.search_books("orwell")[0].book_id, book.book_id)

        loaded = Library(self.library.data_file)
        self.assertEqual(loaded.books[book.book_id].title, "1984")

    def test_borrow_and_return_book(self) -> None:
        book = self.library.add_book("Dune", "Frank Herbert", 1965)
        member = self.library.register_member("Asha", "asha@example.com")
        self.library.borrow_book(book.book_id, member.member_id)
        self.assertEqual(self.library.books[book.book_id].borrowed_by, member.member_id)
        self.library.return_book(book.book_id)
        self.assertIsNone(self.library.books[book.book_id].borrowed_by)

    def test_cannot_borrow_book_twice(self) -> None:
        book = self.library.add_book("Dune", "Frank Herbert", 1965)
        first = self.library.register_member("Asha", "asha@example.com")
        second = self.library.register_member("Ravi", "ravi@example.com")
        self.library.borrow_book(book.book_id, first.member_id)
        with self.assertRaisesRegex(ValueError, "already borrowed"):
            self.library.borrow_book(book.book_id, second.member_id)


if __name__ == "__main__":
    unittest.main()
