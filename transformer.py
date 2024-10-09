from parser import args
from database import DatabaseHandler
from file_reader import FileReader
import pandas as pd


def transfering_excle_to_database(file: str, db: str) -> None:

    # read data from excle file
    filereader = FileReader(file)
    df = filereader.read_excel()

    # trnsfer data excel file and insert in sqlite database
    databasehander = DatabaseHandler(db)
    databasehander.create_table("divar_query", df.columns)
    databasehander.transfer_to_database("divar_query", df)


transfering_excle_to_database(args.transforme[0], args.transforme[1])
