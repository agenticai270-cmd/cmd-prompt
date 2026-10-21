"""Simple JSON-backed library management system."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    year: int
    borrowed_by: int | None = None


@dataclass
class Member:
    member_id: int
    name: str
    email: str


class Library:
    """Manage books and members, with optional persistence to a JSON file."""

    def __init__(self, data_file: str | Path = "library_data.json") -> None:
        self.data_file = Path(data_file)
        self.books: dict[int, Book] = {}
        self.members: dict[int, Member] = {}
        self._load()

    def _load(self) -> None:
        if not self.data_file.exists():
            return
        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        self.books = {
            int(item["book_id"]): Book(**item) for item in data.get("books", [])
        }
        self.members = {
            int(item["member_id"]): Member(**item) for item in data.get("members", [])
        }

    def save(self) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "books": [asdict(book) for book in self.books.values()],
            "members": [asdict(member) for member in self.members.values()],
        }
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def _next_id(items: dict[int, Any]) -> int:
        return max(items, default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> Book:
        if not title.strip() or not author.strip():
            raise ValueError("Title and author are required.")
        if year < 0:
            raise ValueError("Year cannot be negative.")
        book = Book(self._next_id(self.books), title.strip(), author.strip(), year)
        self.books[book.book_id] = book
        self.save()
        return book

    def register_member(self, name: str, email: str) -> Member:
        if not name.strip() or not email.strip():
            raise ValueError("Name and email are required.")
        member = Member(self._next_id(self.members), name.strip(), email.strip())
        self.members[member.member_id] = member
        self.save()
        return member

    def search_books(self, query: str = "") -> list[Book]:
        query = query.strip().lower()
        return [
            book
            for book in self.books.values()
            if not query
            or query in book.title.lower()
            or query in book.author.lower()
        ]

    def borrow_book(self, book_id: int, member_id: int) -> None:
        book = self.books.get(book_id)
        if book is None:
            raise ValueError("Book not found.")
        if member_id not in self.members:
            raise ValueError("Member not found.")
        if book.borrowed_by is not None:
            raise ValueError("Book is already borrowed.")
        book.borrowed_by = member_id
        self.save()

    def return_book(self, book_id: int) -> None:
        book = self.books.get(book_id)
        if book is None:
            raise ValueError("Book not found.")
        if book.borrowed_by is None:
            raise ValueError("Book is not currently borrowed.")
        book.borrowed_by = None
        self.save()


def display_books(library: Library, query: str = "") -> None:
    books = library.search_books(query)
    if not books:
        print("No books found.")
        return
    for book in books:
        status = (
            f"Borrowed by member #{book.borrowed_by}"
            if book.borrowed_by
            else "Available"
        )
        print(f"#{book.book_id} | {book.title} | {book.author} ({book.year}) | {status}")


def run_cli() -> None:
    library = Library()
    menu = """
Library Management System
1. Add book
2. List/search books
3. Register member
4. List members
5. Borrow book
6. Return book
7. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                book = library.add_book(
                    input("Title: "),
                    input("Author: "),
                    int(input("Publication year: ")),
                )
                print(f"Added book #{book.book_id}.")
            elif choice == "2":
                display_books(library, input("Search (leave blank for all): "))
            elif choice == "3":
                member = library.register_member(input("Name: "), input("Email: "))
                print(f"Registered member #{member.member_id}.")
            elif choice == "4":
                if not library.members:
                    print("No members found.")
                for member in library.members.values():
                    print(f"#{member.member_id} | {member.name} | {member.email}")
            elif choice == "5":
                library.borrow_book(int(input("Book ID: ")), int(input("Member ID: ")))
                print("Book borrowed successfully.")
            elif choice == "6":
                library.return_book(int(input("Book ID: ")))
                print("Book returned successfully.")
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Please choose a number from 1 to 7.")
        except (ValueError, json.JSONDecodeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run_cli()
