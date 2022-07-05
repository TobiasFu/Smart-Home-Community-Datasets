##Using Textblob to generate the polarity/subjectivity of each post 
##Appending the polarity/subjectivity to the data frame
import pandas as pd 
from textblob import TextBlob

if __name__ == "__main__":

    ##How to access the data
    with open("automation_posts_12_06.csv", 'r', encoding='utf-8') as f:
        # deserialize file to Python object
        df = pd.read_csv(f)

    df['polarity'] = df['text'].apply(lambda x: TextBlob(x).polarity)
    df['subjective'] = df['text'].apply(lambda x: TextBlob(x).subjectivity)

    df.to_csv("test_file.csv")
