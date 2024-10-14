from sqlite3 import connect, DatabaseError
from .generator_query import QueryGenerator

import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import numpy as np
import tqdm


class DatabaseHandler:

    def __init__(self, db_path: str) -> None :
        self.con = connect(db_path)
        self.cur = self.con.cursor()
        self.qg = QueryGenerator()

# ------------------------------------

    # Create table in database 
    def create (self, table_name: str, columns:list, foreign_key_col: str=None, ref_table: str=None, ref_col: str=None):
        """
        Create a table with optional foreign key constraint.

        Args:
            table_name (str): Name of the table to be created.
            columns (list): A list of column definitions for the table.
            foreign_key_col (str, optional): The column in the table that will act as a foreign key. Defaults to None.
            ref_table (str, optional): The referenced table for the foreign key. Required if `foreign_key_col` is provided. Defaults to None.
            ref_col (str, optional): The referenced column in the `ref_table` for the foreign key. Required if `foreign_key_col` is pro ided. Defaults to None.

        Raises:
            sqlite3.DatabaseError: If there's an error during table creation.
        """
        try:
            query = self.qg.create(table_name, columns, foreign_key_col, ref_table, ref_col)
#
            self.cur.execute(query)
            print(f"Table '{table_name}' created successfully.")

        except DatabaseError as e:
            print(f"Erro creating table '{table_name}' : {e}")
            raise

# ------------------------------------

    # insert data into database
    def insert(self, table_name: str, values: list) -> None:
        """
        Insert multiple rows into the database in a single transaction.

        Args:
            table_name (str): Name of the table where data will be inserted.
            values (list): List of tuples representing the values to be inserted.
            
        Returns:
            None
        """
        query = self.qg.insert(table_name, values)

        try:
            self.cur.executemany(query, values)
        except:
            print(f"Error during bach insert: {e}")
            raise

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
        query = self.qg.soummons (table_name, columns, colfil, where)

        self.cur.execute(query)

        headers = [x[0] for x in self.cur.description]
        data = self.cur.fetchall()
        df = pd.DataFrame(data , columns=headers)

        return df.replace("-", np.nan)

# ------------------------------------

    # transfer data from excel file into database
    def transfer(self, table_name: str, df: pd.DataFrame, batch_size: int=1000) -> None:
        """
        Transfer data from a DataFrame into the database table.

        Args:
            table_name (str): Name of the table where the data will be inserted.
            df (pd.DataFrame): The DataFrame containing the data to be transferred.
            batch_size (int): The number of records to insert in each batch. Default is 1000.
            
        Returns:
            None
        """
        if df.empty:
            print(f"No data to insert into {table_name}.")
            return 
                        

        total_records = len(df)
        pbar = tqdm.tqdm(desc=f"Inserting into {table_name}...", dynamic_ncols=True, colour="green", mininterval=1, total=total_records)

        try:

            for index in range(0 , total_records, batch_size):
                batch_df = df.iloc[index:index+batch_size]
                batch_values = [tuple(row) for row in batch_df.itertuples(index=False, name=None)]
                self.insert(table_name, batch_values)
                pbar.update(len(batch_values)) 
            self.con.commit()
            pbar.close()
            print(f"Data successfully transferred into {table_name}.")

        except Exception as e:
            print(f"Error during data transfer: {e}")
            self.con.rollback()
            raise

# ------------------------------------

    def __exit__(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()
