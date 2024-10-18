from .painter import DrawPlot
import pandas as pd
import numpy as np

class Metrics:
    def __init__(self, query_df: pd.DataFrame):
        self.qd = query_df
        self.dp = DrawPlot()

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


    def acpg(self) -> pd.DataFrame:
        filled_nan = self.qd.replace("NOINDEX", np.nan)
        unique_rank = filled_nan.groupby("source_event_id")["post_index_in_post_list"].unique().apply(lambda x: round(np.mean(x), 2)).reset_index(name="acpg")
        unique_rank.fillna({"acpg": 0}, inplace=True)
        return unique_rank.acpg
            

    def is_click_top_tree_rate(self):
        filled_nan = self.qd.replace("NOINDEX", np.nan)
        click_on_top_3 = filled_nan[filled_nan['post_index_in_post_list'].between(1, 3)]
        top_3_clicks = click_on_top_3.groupby('source_event_id')['post_index_in_post_list'].count() > 0
        result = top_3_clicks.reindex(filled_nan['source_event_id'].unique(), fill_value=False).reset_index(name="is_click_top_tree")
        return result.is_click_top_tree


    def dark_query(self) -> float:
        dark_queries = self.lppa[self.lppa.post_page_offset < 10]
        dark_query_count = dark_queries.source_event_id.nunique()
        total_query_count = self.lppa.source_event_id.nunique()
        return (dark_query_count / total_query_count) * 100


    def bunose_rank(self):
        load_queries = self.lppa["source_event_id"].unique()
        clicked_queries = self.cpa["source_event_id"].unique()
        bounced_queries = set(load_queries) - set(clicked_queries)
        bounced_coount = len(bounced_queries)
        total_load_coount = len(load_queries)
        return (bounced_coount / total_load_coount) * 100 if total_load_coount > 0 else 0
