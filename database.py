from sqlite3 import connect
import pandas as pd
import tqdm


class DatabaseHandler:

    def __init__(self, db_path: str) -> None :
        self.con = connect(db_path)
        self.cur = self.con.cursor()

    def create_table(self, table_name: str, columns: list) -> None:
        try:
            query = f""" CREATE TABLE {table_name}({", ".join([column for column in columns])}); """
            return self.cur.execute(query)
        except Exception as e:
            print(e)
            pass

    def insert_value(self, table_name: str, values: tuple) -> None:
        query = f""" INSERT INTO {table_name} VALUES {values} """
        self.cur.execute(query)
        return self.con.commit()

    def transfer_to_database(self, table_name: str, df: pd.DataFrame) -> None:
        pbar = tqdm.tqdm(desc="Transfering...", dynamic_ncols=True, colour="green", mininterval=1, total=len(df))
        for index , (user_id, action, created_at, source_event_id, device_id, post_page_offset, tokens, post_index_in_post_list, post_token) in df.iterrows():
            values = (user_id, action, created_at, source_event_id, device_id, post_page_offset, tokens, post_index_in_post_list, post_token) 
            self.insert_value(table_name, values)
            pbar.update(1) 

    def __exit__(self):
        cur.close()
        con.close()
