from database import DatabaseHandler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

TABLE_NAME = "divar_query"
FILTER = "action"

if __name__ == "__main__":
    db = DatabaseHandler("divar.db")


    load_post_page_df = db.summons(TABLE_NAME, colfil=FILTER,  where=["load_post_page"]) 
    load_post_page_df.drop(columns=["post_index_in_post_list", "post_token"], inplace=True)

    click_post_df = db.summons(TABLE_NAME, colfil=FILTER, where=["click_post"])
    click_post_df.drop(columns=["post_page_offset", "tokens"], inplace=True)

    load_post_page_duplicates = load_post_page_df.duplicated().sum()
    click_post_duplicates = click_post_df.duplicated().sum()

    tables = ['load_post_page_df', 'click_post_df']
    duplicates = [load_post_page_duplicates, click_post_duplicates]
    unique_records = [len(load_post_page_df) - load_post_page_duplicates, len(click_post_df) - click_post_duplicates]

    plt.figure(figsize=(15, 4))
    bar_width = 0.4
    index = range(len(tables))

    plt.bar(index, unique_records, bar_width, label="Unique Records", color='blue')
    plt.bar([i + bar_width for i in index], duplicates, bar_width, label="Duplicate Records", color='red')

    # Labeling the chart
    plt.xlabel("Tables")
    plt.ylabel("Record Count")
    plt.title("Duplicate vs Unique Records in Tables")
    plt.xticks([i + bar_width/2 for i in index], tables)
    plt.legend()

    plt.savefig("./image/barplot.png")
