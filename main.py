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

    divar_query_metric = pd.DataFrame(divar_query_df.source_event_id.unique(), columns=["source_event_id"])

    # Calculate Four Metric User Bihavior Analysis
    met = Metrics(divar_query_df)

    # Calculate Click-Througe Rate
    divar_query_metric ["click-througe rate (CTR)"] = met.ctr()

    # Position of first click
    divar_query_metric ["position of first click (PFC)"] = met.pfc()

    # Avrage click position gap
    divar_query_metric ["avrage click positon gap (ACPG)"] = met.acpg()

    # Top-3 click rate
    divar_query_metric ["is_click_top_tree_rate?"] = met.is_click_top_tree_rate()

    # Dark query percent
    dark_query_percent = met.dark_query_percent()
    print(f"Dark_Query_Percent: {dark_query_percent}%")

    # Bounce rate 
    bounce_rate_percent = met.bounce_rate_percent()
    print(f"Bounce_Rate: {bounce_rate_percent}%")
