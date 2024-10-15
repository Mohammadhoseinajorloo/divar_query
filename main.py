from database import DatabaseHandler
from metrics import Metrics


if __name__ == "__main__":
    db = DatabaseHandler("divar.db")
    load_post_page_df = db.summons('load_post_page_action') 
    click_post_df = db.summons("click_post_action")

    met = Metrics(load_post_page_df, click_post_df)
    ctr = met.ctr()
    adcr = met.avrage_distanc_click_rank()
    click_percentage = met.click_perc()
    fcr = met.first_click_rank()
    dq = met.dark_query()
    br = met.bunose_rank()
