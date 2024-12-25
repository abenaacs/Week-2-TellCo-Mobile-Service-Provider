import pandas as pd


def extract_data(query):

    # Load dataset
    data = pd.read_excel(
        "C:/Users/hp/Desktop/Academic_Folders/Kifiya AI Mastery/week 2/week-2-TellCo Mobile Service Provider/data/Week2_challenge_data_source.xlsx"
    )
    return data
