
import polars as pl
import time
from finvader import finvader


class Scoring_finvader:

    def __init__(self, year: str, month: str):
        self.year = year
        self.month = month
        try:
            self.reading()
            self.scoring()
            self.saving()
        except FileNotFoundError:
            pass

    def reading(self):
        self.data = pl.read_csv(f"C:\\Users\\eitan\\Downloads\\masters\\data\\{self.year}_{self.month}.csv", has_header=True)

    def scoring(self):
        self.data = self.data.with_columns(pl.Series(name="Finvader Score", values=self.data["Sentences"].apply(
            lambda t: finvader(t, use_sentibignomics=True, use_henry=True, indicator='compound'))))

    def saving(self):
        self.data.write_csv(f"C:\\Users\\eitan\\Downloads\\masters\\data\\{self.year}_{self.month}_finvader.csv", has_header=True)


def one_to_rule_them_all(months: list, years: list):
    for year in years:
        print(year)
        for month in months:
            print(month)
            Scoring_finvader(year=year, month=month)



years = ["2016","2017","2018","2019", "2020"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]

one_to_rule_them_all(months, years)

months2021 = ["January", "February", "March", "April", "May"]
year2021 = ["2021"]
one_to_rule_them_all(months2021, year2021)