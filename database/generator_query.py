class QueryGenerator:


# ------------------------------------

    # generate create query
    def create (self, table_name: str, columns:list, foreign_key_col: str, ref_table: str, ref_col: str) -> str:
        query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)}"""

        # Add foreign key if provided
        if foreign_key_col and ref_table and ref_col:
            query += f""", FOREIGN KEY ({foreign_key_col}) REFERENCES {ref_table}({ref_col})"""

        query += ");" 
        return query

# ------------------------------------

    # generate insert query
    def insert (self, table_name: str, values:list) -> str:
        placeholders = ", ".join(["?" for _ in values[0]])
        query = f""" INSERT INTO {table_name} VALUES ({placeholders}) """
        return query

# ------------------------------------

    # generate soummons query
    def soummons (self, table_name, columns: list, colfil: str, where: list):
        if columns:
            if not isinstance(columns, list):
                raise TypeError (f"The columns type should be list, but you sent {type(columns)}")
            columns_str = ", ".join(columns)
            return  f"SELECT {columns_str} FROM {table_name}"
        else:
            return f"SELECT * FROM {table_name}"

        if (colfil is not None and where is None) or (colfil is None and where is not None):
            raise ValueError( f"""Parameters 'where' and 'colfil' are two dependent parameters and must be set. But currently one of these two parameters does not have a value. You can use all the nature of the data without setting these two parameters. If you need the data of a specific column, set 'columns' and if you want to access all the data, just enter the table name. """)

        if colfil and where:
            if not isinstance(where, list) or len(where) == 0:
                raise ValueError("The 'where' parameter must be a non-empty list.")

            placeholders = ", ".join(['?'] * len(where))
            query += f" WHERE {colfil} IN ({placeholders})"
            return query
