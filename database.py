from sqlite3 import connect

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import numpy as np
import tqdm


class DatabaseHandler:

    def __init__(self, db_path: str) -> None :
        self.con = connect(db_path)
        self.cur = self.con.cursor()

    def create_table(self, table_name: str, columns: list) -> None:
        try:
            query = f""" CREATE TABLE {table_name} ({", ".join([column for column in columns])}); """
            return self.cur.execute(query)
        except Exception as e:
            print(e)
            pass

    def insert_value(self, table_name: str, values: tuple) -> None:
        query = f""" INSERT INTO {table_name} VALUES {values} ;"""
        return self.cur.execute(query)

# ------------------------------------
    # Summons data from database
    def summons(self, table_name, columns: list=None, colfil: str=None, where: list=None) -> pd.DataFrame:
        """
        Executes a SQL query to retrieve data from a specified table and returns the result as a Pandas DataFrame.

        The method allows filtering the results based on specific column values and supports 
        selecting specific columns from the table. It handles SQL injection risks by using parameterized queries.

        Parameters:
        ----------
        table_name : str
            The name of the database table from which to retrieve data.
            
        columns : list, optional
            A list of column names to select from the table. If None, all columns will be selected. 
            It should be of type list, e.g., ['column1', 'column2'].
            
        colfil : str, optional
            The column name to filter the results by. Must be provided if the 'where' parameter is specified.
            
        where : list, optional
            A list of values to filter the results. The function will return rows where the specified 
            'colfil' column matches any of the values in this list. 
            Must be a non-empty list if provided.

        Returns:
        -------
        pd.DataFrame
            A Pandas DataFrame containing the retrieved data. The DataFrame will replace 
            any '-' values with NaN to ensure consistency in data representation.

        Raises:
        ------
        ValueError
            If either 'colfil' or 'where' is specified without the other, or if 'where' is not a non-empty list.

        TypeError
            If the 'columns' parameter is not of type list.
        """
        if columns:
            if not isinstance(columns, list):
                raise TypeError (f"The columns type should be list, but you sent {type(columns)}")
            columns_str = ", ".join(columns)
            query = f"SELECT {columns_str} FROM {table_name}"
        else:
            query = f"SELECT * FROM {table_name}"

        if (colfil is not None and where is None) or (colfil is None and where is not None):
            raise ValueError( f"""Parameters 'where' and 'colfil' are two dependent parameters and must be set. But currently one of these two parameters does not have a value. You can use all the nature of the data without setting these two parameters. If you need the data of a specific column, set 'columns' and if you want to access all the data, just enter the table name. """)

        if colfil and where:
            if not isinstance(where, list) or len(where) == 0:
                raise ValueError("The 'where' parameter must be a non-empty list.")

            placeholders = ", ".join(['?'] * len(where))
            query += f" WHERE {colfil} IN ({placeholders})"

        self.cur.execute(query, where)

        headers = [x[0] for x in self.cur.description]
        data = self.cur.fetchall()
        df = pd.DataFrame(data , columns=headers)

        return df.replace("-", np.nan)
# ------------------------------------

    def transfer_to_database(self, table_name: str, df: pd.DataFrame) -> None:
        lenght = len(df)
        pbar = tqdm.tqdm(desc="Transfering...", dynamic_ncols=True, colour="green", mininterval=1, total=lenght)
        for index , (action, created_at, source_event_id, device_id, post_page_offset, tokens, post_index_in_post_list, post_token) in df.iterrows(): 
            values = (action, created_at, source_event_id, device_id, post_page_offset, tokens, post_index_in_post_list, post_token) 
            self.insert_value(table_name, values)
            pbar.update(1) 
        return self.con.commit()

    def __exit__(self):
        cur.close()
        con.close()
