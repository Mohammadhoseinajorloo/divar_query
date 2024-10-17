from database import DatabaseHandler
from metrics import Metrics

import pandas as pd


if __name__ == "__main__":
    # read load and click data from database
    db = DatabaseHandler("divar.db")
    load_post_page_df = db.summons('load_post_page_action') 
    click_post_df = db.summons("click_post_action")

    # merge load and click data read from database and rename columns
    divar_query_df = pd.merge(load_post_page_df, click_post_df, on="source_event_id", how="left")
    divar_query_df.columns = [
            "action_load",
            "create_at_load",
            "source_event_id",
            "device_id_load",
            "post_page_offset",
            "tokens",
            "action_click",
            "create_at_click",
            "device_id_click",
            "post_index_in_post_list",
            "post_token",
        ]

    # handel missing values in data 
    divar_query_df.fillna({"action_click": "NOTCLICKED"}, inplace=True)
    divar_query_df.fillna({"create_at_click": "TIMELESS"}, inplace=True)
    divar_query_df.fillna({"post_index_in_post_list": "NOINDEX"}, inplace=True)
    divar_query_df.fillna({"post_token": "NOTCLICKED"}, inplace=True)
    divar_query_df.fillna({"device_id_click": "NODEVICE"}, inplace=True)
    divar_query_df.dropna(subset=["device_id_load"], inplace=True)

    divar_query_metric = divar_query_df.groupby("source_event_id").size().reset_index(name="query_count")
    # Calculate Four Metric User Bihavior Analysis
    met = Metrics(divar_query_df)

    # Calculate Click-Througe Rate
    divar_query_metric = met.ctr()

'''
    adcr = met.avrage_distanc_click_rank()
    click_percentage = met.click_perc()
    fcr = met.first_click_rank()
    dq = met.dark_query()
    br = met.bunose_rank()
'''
