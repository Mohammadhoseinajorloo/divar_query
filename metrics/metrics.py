from .painter import DrawPlot
import pandas as pd

class Metrics:
    def __init__(self, load_post_page_action: pd.DataFrame, click_post_action: pd.DataFrame):
        self.lppa = load_post_page_action
        self.cpa = click_post_action
        self.dp = DrawPlot()

    def ctr(self) -> float:
        post_page_offset_count = self.lppa.groupby("source_event_id")["post_page_offset"].agg("count").reset_index(name="Post_Page_Offset_Count")
        post_page_offset_count["Ad_Count"] = post_page_offset_count.Post_Page_Offset_Count * 24
        post_token_count = self.cpa.groupby("source_event_id")["post_token"].agg("count").reset_index(name="Post_Token_count")
        result = pd.merge(post_page_offset_count, post_token_count, on="source_event_id", how="left")
        result.fillna(0, inplace=True)
        result["Click_Percentage"] = round((result.Post_Token_count / result.Ad_Count) * 100 , 2)
        return result.Click_Percentage.mean()


    def avrage_distanc_click_rank(self, draw_plot: bool=False, type_plot="dist") -> pd.DataFrame:
        combined_df = pd.merge(self.lppa, self.cpa, on="source_event_id", how="left")
        avrage_click_rank = combined_df.groupby("source_event_id")["post_index_in_post_list"].agg("mean").reset_index(name="Avrage_Click_Rank")
        avrage_click_rank.fillna(0, inplace=True)

        if draw_plot:
            self.dp.draw_boxplot(avrage_click_rank, type_plot)
        
        return avrage_click_rank
            

    def click_perc(self, draw_plot: bool=False, type_plot="grouped") -> pd.DataFrame:
        post_page_offset_count = self.lppa.groupby("source_event_id")["post_page_offset"].agg("count").reset_index(name="Post_Page_Offset_Count")
        post_page_offset_count["Ad_Count"] = post_page_offset_count.Post_Page_Offset_Count * 24
        post_token_count = self.cpa.groupby("source_event_id")["post_token"].agg("count").reset_index(name="Post_Token_count")
        result = pd.merge(post_page_offset_count, post_token_count, on="source_event_id", how="left")
        result.fillna(0, inplace=True)
        result["Click_Percentage"] = round((result.Post_Token_count / result.Ad_Count) * 100 , 2)


        if draw_plot:
            self.dp.draw_barplot(result, type_plot)

        return result


    def first_click_rank(self, draw_plot: bool=False) -> pd.DataFrame:
        merge_df = pd.merge(self.lppa, self.cpa, on="source_event_id", how="left")
        click_count_df = merge_df.groupby("source_event_id")["action_y"].agg("count").reset_index(name="Click_count")
        click_more_one_index = click_count_df[click_count_df.Click_count >= 1].index
        click_more_one_df = merge_df.iloc[click_more_one_index]
        first_click_ranks = click_more_one_df.groupby("source_event_id")["post_index_in_post_list"].agg("min")

        if draw_plot:
            self.dp.draw_kdeplot(first_click_ranks)

        return first_click_ranks


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
