import json
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import swifter

import numpy as np

def encode_text_in_batches(df, batch_size=64):
    embeddings = []

    for i in tqdm(range(0, len(df), batch_size)):
        batch_text = df.iloc[i:i+batch_size]["text"].tolist()
        batch_embeddings = model_sentence.encode(batch_text)
        embeddings.extend(batch_embeddings)

    return embeddings


if __name__ == '__main__':

    model_sentence = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device="cuda")
    files = os.listdir("Data/jsons")


    df = pd.DataFrame()
    print("Reading files...")
    for file in tqdm(files):
        df = pd.concat([df, (pd.read_json(f"Data/jsons/{file}", lines=True))])   


    print("Dropping duplicates...") 
    df = df.drop_duplicates(subset=["url"]).reset_index(drop=True)
    print("Applying textparser...")
    swifter.set_npartitions(12)
    df["text"] = df["content"].swifter.apply(lambda x: BeautifulSoup(x, "html.parser").get_text())
    print("Encoding text...")
    df["embedding"] = encode_text_in_batches(df, batch_size=64)
    print("Saving dataframe...")
    df.to_pickle("Data/master_df.pickle")


 

