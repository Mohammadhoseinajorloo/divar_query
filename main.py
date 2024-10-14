from database import DatabaseHandler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    db = DatabaseHandler("divar.db")

    load_post_page_df = db.summons('load_post_page_action') 
    click_post_df = db.summons("click_post_action")


    # Query Percent (less than 10 results)
    dark_queries = load_post_page_df[load_post_page_df.post_page_offset < 10]
    dark_query_count = dark_queries.source_event_id.nunique()

    total_query_count = load_post_page_df.source_event_id.nunique()

    dark_query_percent = (dark_query_count / total_query_count) * 100
    print(f"Dark Query Percent (less than 10 results): {dark_query_percent:.2f}%")


    # Query Percent (Click not user)
    load_queries = load_post_page_df["source_event_id"].unique()
    clicked_queries = click_post_df["source_event_id"].unique()

    bounced_queries = set(load_queries) - set(clicked_queries)
    bounced_coount = len(bounced_queries)
    total_load_coount = len(load_queries)

    bounce_rate = (bounced_coount / total_load_coount) * 100 if total_load_coount > 0 else 0
    print(f"Bounce Rate: {bounce_rate:.2f}%")
    
    




