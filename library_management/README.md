# Library Management System

A beginner-friendly Python command-line project for managing books, members, and borrowing.

## Features

- Add and search books
- Update and remove books and members
- Categories, multiple copies, and availability filtering
- Register members with roles and active/inactive accounts
- Borrow, return, renew, and track loan history
- Overdue-loan detection and automatic late fines
- Statistics, popular-book reports, and CSV exports
- Save data automatically in `library_data.json`
- Unit tests using Python's standard library

## Run the application

```bash
cd library_management
python library_manager.py
```

## Run tests

```bash
cd library_management
python -m unittest -v
```

The test suite covers persistence, validation, multiple copies, overdue fines,
renewals, reports, and CSV exports.

## Run the Java version

The Java implementation is provided in `LibraryManager.java`.

```bash
cd library_management
javac LibraryManager.java
java LibraryManager
```

The Java version automatically saves its data in `library_data_java.bin`.
