import pandas as pd
import numpy as np
import json
import os
from multiprocessing import Pool

def process_file(file):
    if file[-3:] == "log":
        try:
            with open(f"Data/{file}", "r", encoding="utf-8") as f:
                for line in f:
                    json_line = json.loads(line)
                    date = json_line["created_at"][:10]
                    server = os.path.splitext(file)[0]

                    if not os.path.exists(f"Data/jsons"):
                        os.makedirs(f"Data/jsons")

                    with open(f"Data/jsons/{date}_{server}.json", "a", encoding="utf-8") as date_file:
                        date_file.write(json.dumps(json_line) + "\n")

        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    files = os.listdir("Data")
    with Pool() as p:
        p.map(process_file, files)
        
"""
lambda x: BeautifulSoup(x, "html.parser").get_text()
"""