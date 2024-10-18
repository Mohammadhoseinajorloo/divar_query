import pandas as pd
import numpy as np

class Metrics:
    def __init__(self, query_df: pd.DataFrame):
        self.qd = query_df

    def ctr(self) -> float:
        filled_nan = self.qd.replace("NOTCLICKED", np.nan)
        unique_page = filled_nan.drop_duplicates(subset=["source_event_id", "post_page_offset"])
        unique_page ["lentokens_per_page"] = unique_page["tokens"].apply(lambda x: len(x[1:-1].split(",")))
        ad_loaded = unique_page.groupby("source_event_id")["lentokens_per_page"].sum().reset_index(name="ad_loaded")
        ad_clicked = filled_nan.groupby("source_event_id")["post_token"].apply(lambda x:  x.dropna().nunique()).reset_index(name="ad_clicked")
        return round((ad_clicked.ad_clicked / ad_loaded.ad_loaded) * 100 , 2)

        
    def pfc(self) -> pd.Series:
        filled_nan = self.qd.replace("NOINDEX", np.nan)
        pfc = filled_nan.groupby('source_event_id')['post_index_in_post_list'].apply(lambda x: x.fillna(0).min()).reset_index(name="pfc")
        return pfc.pfc


    def acpg(self) -> pd.Series:
        filled_nan = self.qd.replace("NOINDEX", np.nan)
        unique_rank = filled_nan.groupby("source_event_id")["post_index_in_post_list"].unique().apply(lambda x: round(np.mean(x), 2)).reset_index(name="acpg")
        unique_rank.fillna({"acpg": 0}, inplace=True)
        return unique_rank.acpg
            

    def is_click_top_tree_rate(self) -> pd.Series:
        filled_nan = self.qd.replace("NOINDEX", np.nan)
        click_on_top_3 = filled_nan[filled_nan['post_index_in_post_list'].between(1, 3)]
        top_3_clicks = click_on_top_3.groupby('source_event_id')['post_index_in_post_list'].count() > 0
        result = top_3_clicks.reindex(filled_nan['source_event_id'].unique(), fill_value=False).reset_index(name="is_click_top_tree")
        return result.is_click_top_tree


    def dark_query_percent(self) -> float:
        result_counts = self.qd.groupby('source_event_id')['post_page_offset'].nunique()
        dark_queries = result_counts[result_counts < 10]
        dark_query_percent = (len(dark_queries) / result_counts.size) * 100
        return round(dark_query_percent, 2)


    def bounce_rate_percent(self):
        grouped = self.qd.groupby('source_event_id')
        no_click_queries = grouped.apply(lambda x: (x['post_token'] == "NOTCLICKED").all())
        bounce_rate = (no_click_queries.sum() / len(grouped)) * 100
        return round(bounce_rate, 2)
