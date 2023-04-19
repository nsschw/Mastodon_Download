import pandas as pd
import json
import plotly.express as px

# Read in the data
climatejustice_rocks = [json.loads(line) for line in open(f"Data/fediverse-climatejustice.rocks-toots.log", "r", encoding="utf-8")]
mastodon_green = [json.loads(line) for line in open(f"Data/fediverse-mastodon.green-toots.log", "r", encoding="utf-8")]
metalhead_club = [json.loads(line) for line in open(f"Data/fediverse-metalhead.club-toots.log", "r", encoding="utf-8")]
obo_sh = [json.loads(line) for line in open(f"Data/fediverse-obo.sh-toots.log", "r", encoding="utf-8")]
rollenspiel_social = [json.loads(line) for line in open(f"Data/fediverse-rollenspiel.social-toots.log", "r", encoding="utf-8")]
todon_eu = [json.loads(line) for line in open(f"Data/fediverse-todon.eu-toots.log", "r", encoding="utf-8")]
veganism_social = [json.loads(line) for line in open(f"Data/fediverse-veganism.social-toots.log", "r", encoding="utf-8")]


list_of_data = [climatejustice_rocks, mastodon_green, metalhead_club, obo_sh, rollenspiel_social, todon_eu, veganism_social]
names_of_servers = ["climatejustice.rocks", "mastodon.green", "metalhead.club", "obo.sh", "rollenspiel.social", "todon.eu", "veganism.social"]


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)


# Add server and account_unique columns
for instance in list_of_data:
    for toot in instance:
        toot['server'] = toot['account']['acct'].split("@")[-1]
        toot['account_unique'] = toot['account']['acct']

# Create dataframes
list_of_df = []
for instance in list_of_data:
    df = pd.DataFrame(instance)
    df = df.drop_duplicates(subset=['account_unique']).reset_index(drop=True)
    list_of_df.append(df)

# Create a list of dataframes with the jaccard similarity
df_jaccard = pd.DataFrame()
counter = 0
for i, df in enumerate(list_of_df):
    for h, df2 in enumerate(list_of_df):
        jaccard = jaccard_similarity(df['account_unique'].unique(), df2['account_unique'].unique())
        df_jaccard.at[counter, "jaccard"] = jaccard
        df_jaccard.at[counter, "server1"] = names_of_servers[i]
        df_jaccard.at[counter, "server2"] = names_of_servers[h]
        counter += 1

    
#plot heatmap using plotly
fig = px.imshow(df_jaccard.pivot(index='server1', columns='server2', values='jaccard'), color_continuous_scale="YlOrRd")
fig.write_html("jaccard_distance.html")