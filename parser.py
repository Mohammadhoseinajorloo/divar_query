import argparse


PROGRAMM_NAME = "transformer"
DESCTIPTION = """ This program automates the process of transferring data from an Excel file (.xlsx or .xls) to an SQLite database. The application reads the content of the Excel file, processes it, and inserts the data into a specified SQLite database table. It supports multiple sheets within the Excel file and ensures that data types are preserved during the transfer. The program also allows for basic data validation and error handling to ensure that the data integrity is maintained during the process. """
FOOTER = """ This program is ideal for anyone looking to streamline data migration between Excel and SQLite for tasks like data analysis, reporting, or database initialization. """


parser = argparse.ArgumentParser(prog=PROGRAMM_NAME, description=DESCTIPTION, epilog=FOOTER)
parser.add_argument('-t', '--transforme', metavar=('EXCEL_FILE', 'SQLITE_DB'), nargs=2, help='transform excel data into sqlite database')


args = parser.parse_args()
