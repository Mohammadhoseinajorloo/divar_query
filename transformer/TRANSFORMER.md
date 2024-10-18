# Excel to SQLite Transformer

This program is designed to transfer data from an Excel file into an SQLite database. It reads the contents of the specified Excel file and inserts the data into the corresponding table in the SQLite database, creating the database if it doesn't already exist. The tool is useful for database initialization, data migration, or integrating Excel data into an SQL-based application.

## Features
- **Excel File Parsing**: Reads data from one or multiple sheets in an Excel file.
- **SQLite Integration**: Automatically creates and connects to an SQLite database.
- **Column Mapping**: Matches Excel columns to SQLite table fields.
- **Data Validation**: Ensures proper data types and handles errors gracefully.
- **Batch Insertion**: Efficiently inserts data into the SQLite database in batches.
- **Error Handling**: Captures and logs any issues during data transfer.

## Prerequisites

Make sure you have the following Python packages installed:
- `openpyxl`: For reading `.xlsx` files.
- `sqlite3`: A standard library in Python for SQLite operations.
- `argparse`: A standard library in Python for command-line argument parsing.

You can install the necessary external dependencies using:

```bash
pip install -r requairment.txt
```

## Usage

To run the script, use the following command:

```bash
python transformer.py -t <path_to_excel_file> <path_to_sqlite_db>
```

- `<path_to_excel_file>`: Path to the Excel file (e.g., `data.xlsx`).
- `<path_to_sqlite_db>`: Path to the SQLite database (e.g., `database.db`). If the database does not exist, the program will create it.

### Example

```bash
python transformer.py -t data.xlsx database.db
```

This command will:
1. Parse the `data.xlsx` file.
2. Create (or connect to) `database.db`.
3. Insert the data from the Excel file into a table in the SQLite database.

### Command-line Options

| Flag                    | Arguments                              | Description                                        |
|-------------------------|----------------------------------------|----------------------------------------------------|
| `-t`, `--transform`      | `<EXCEL_FILE> <SQLITE_DB>`             | Transforms Excel data into an SQLite database.     |

## Script Structure

- **Excel File Parsing**: The program uses the `openpyxl` library to read Excel files. It can handle both `.xlsx` and `.xls` formats.
- **SQLite Database Management**: It uses Python's built-in `sqlite3` module to manage SQLite databases. If the database file doesn't exist, it creates a new one.
- **Batch Insertion**: Data from the Excel file is inserted into the SQLite database in batches to improve performance.

## Error Handling

If there are any errors during the transformation (e.g., invalid data, connection issues), they will be logged for further analysis. Make sure to review the error logs for debugging.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to contribute by submitting a pull request or opening an issue to improve functionality or add new features.

