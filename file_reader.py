import pandas as pd


class FileReader:

    def __init__(self, file):
        dot = file.find(".")
        self.name = file[:dot]
        self.ext = file[dot+1:]

    def read_excel(self) -> pd.DataFrame:
        df = pd.read_excel(self.name + "." + self.ext)
        df.reset_index(inplace=True)
        df.rename(columns={'index':'user_id'}, inplace=True)
        return df.fillna("-")
