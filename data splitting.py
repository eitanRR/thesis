import spacy
import pandas as pd
import polars as pl


nlp_english = spacy.load("en_core_web_sm",disable=["ner","tokenizer","tagger","lemmatizer","textcat","custom"])


def reading_data(year,month):
    reading = pd.read_pickle(f'C:\\Users\\eitan\\Downloads\\masters\\{month}{year}.pkl', compression='xz',
                             storage_options=None)
    if len(reading)>0:
        reading_headlines = reading["Headline"]
        reading_articles = reading["Article"]
    else:
        reading_headlines, reading_articles = 0,0
    return reading_headlines, reading_articles

def splitting(headlines,articles):
    sentences = []
    for i in range(0,len(headlines)):
        data_split = articles[i]
        article = nlp_english(data_split)
        headline = headlines[i]
        sentences.append(headline)
        # new memory slab
        for sent in article.sents:
            sent_ = str(sent)
            sentences.append(sent_)
    data_sents = pl.DataFrame({"sentences": sentences})
    return data_sents


def one_to_rule_them_all(months,years):
    for year in years:
        print(year)
        for month in months:
            print(month)
            headlines, articles = reading_data(year, month)
            data_sents_pl = splitting(headlines, articles)
            data_sents_pl.write_csv(f"C:\\Users\\eitan\\Downloads\\masters\\data\\{year}_{month}.csv", has_header=False)




years = ["2015", "2016", "2017"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]

one_to_rule_them_all(months, years)
