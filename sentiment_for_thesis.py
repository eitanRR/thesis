import polars as pl
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk.sentiment.sentiment_analyzer as sentiment_analyser
import polars.selectors as cs
import namedtuple2

sid  = SentimentIntensityAnalyzer()

class Scoring_vader:

    def __init__(self, year: str, month: str):
        self.year=year
        self.month=month
        try:
            self.reading()
            self.scoring()
            self.saving()
        except FileNotFoundError:
            pass

    def reading(self):
        self.data = pl.read_csv(f"C:\\Users\\eitan\\Downloads\\masters\\data\\{self.year}_{self.month}.csv", has_header=False)
        if len(self.data) > 0:
            lst = self.data.columns
            self.data=self.data.rename({f"{lst[-1]}":"Sentences"})
            # preventing errors
            self.data = self.data.select(cs.all().cast(pl.Utf8))
            self.data = self.data.filter(pl.all(pl.col(pl.Float32, pl.Float64).is_not_nan())).drop_nulls()

    def scoring(self):
        self.Final_data: DataFrame = self.data.with_columns(pl.Series(name="Compounded Score by vader",values=self.data["Sentences"].apply(lambda t:sid.polarity_scores(t).get("compound"))))

    def saving(self):
        self.Final_data.write_csv(f"C:\\Users\\eitan\\Downloads\\masters\\data\\{self.year}_{self.month}.csv", has_header=True)


def one_to_rule_them_all(months: list, years: list):
    for year in years:
        print(year)
        for month in months:
            print(month)
            Scoring_vader(year=year, month=month)


years = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019", "2020"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]

one_to_rule_them_all(months, years)

months2021 = ["January", "February", "March", "April", "May"]
year2021 = ["2021"]
one_to_rule_them_all(months2021, year2021)