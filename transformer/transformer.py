import sys

WORK_DIR = '/home/mohammad/Documents/EDUCATIONAL/data_science/divar_task'
sys.path.append(WORK_DIR)

from database import DatabaseHandler
from file_reader import FileReader
from parser import args
import pandas as pd


def transfering_excle_to_database(file: str, db: str) -> None:

    # read data from excle file
    filereader = FileReader(file)
    df = filereader.read_excel()

    load_post_page_df = df[df.action == "load_post_page"]
    load_post_page_df = load_post_page_df.drop(columns=["post_index_in_post_list", "post_token"])

    click_post_df = df[df.action == "click_post"]
    click_post_df = click_post_df.drop(columns=["tokens", "post_page_offset"])
    click_post_df = click_post_df.iloc[:, 4:]
    click_post_df = click_post_df.reset_index(names="id")

    # trnsfer data excel file and insert in sqlite database
    databasehander = DatabaseHandler(db)
    databasehander.create("load_post_page_action", load_post_page_df.columns)
    databasehander.create("click_post_action", click_post_df.columns, "id", "load_post_page_action", "source_event_id")
    
    databasehander.transfer("load_post_page_action", load_post_page_df)
    databasehander.transfer("click_post_action", click_post_df)


transfering_excle_to_database(args.transforme[0], args.transforme[1])
