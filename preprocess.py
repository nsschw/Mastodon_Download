import pandas as pd
import numpy as np
import json
import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


def process_file(args):
    file, model = args

    DATELIST = ["2023-04-19", "2023-04-20", "2023-04-21", "2023-04-22", "2023-04-23", "2023-04-24", "2023-04-25"]

    if not os.path.exists(f"Data/jsons"):
        os.makedirs(f"Data/jsons")    
    
    if file[-3:] == "log":
        with open(f"Data/{file}", "r", encoding="utf-8") as f:
            for line in f:
                try:
                    json_line = json.loads(line)
                    date = json_line["created_at"][:10]
                    server = os.path.splitext(file)[0]

                    if date in DATELIST:                    
                        with open(f"Data/jsons/{date}_{server}.json", "a", encoding="utf-8") as date_file:
                            date_file.write(json.dumps(json_line) + "\n")

                except Exception as e:
                    print(e)

if __name__ == '__main__':

    model_sentence = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device="cuda")
    files = os.listdir("Data")
    with Pool() as p:
        p.map(process_file, [(file, model_sentence) for file in files])