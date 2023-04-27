"""
Reduced complexity as instances are treated as nodes
and the share of accounts from servers between them as edges.

-> would be better to use accounts as nodes and follow relationships as edges
    and then work with subgraphs of the network
"""

import pandas as pd
import networkx as nx
import json
import matplotlib.pyplot as plt

# Read in the data
climatejustice_rocks = [json.loads(line) for line in open(f"Data/fediverse-climatejustice.rocks-toots.log", "r", encoding="utf-8")]
mastodon_green = [json.loads(line) for line in open(f"Data/fediverse-mastodon.green-toots.log", "r", encoding="utf-8")]
metalhead_club = [json.loads(line) for line in open(f"Data/fediverse-metalhead.club-toots.log", "r", encoding="utf-8")]
obo_sh = [json.loads(line) for line in open(f"Data/fediverse-obo.sh-toots.log", "r", encoding="utf-8")]
rollenspiel_social = [json.loads(line) for line in open(f"Data/fediverse-rollenspiel.social-toots.log", "r", encoding="utf-8")]
todon_eu = [json.loads(line) for line in open(f"Data/fediverse-todon.eu-toots.log", "r", encoding="utf-8")]
veganism_social = [json.loads(line) for line in open(f"Data/fediverse-veganism.social-toots.log", "r", encoding="utf-8")]


list_of_data = [climatejustice_rocks, mastodon_green,  obo_sh, rollenspiel_social, metalhead_club, todon_eu, veganism_social]
names_of_servers = ["climatejustice.rocks", "mastodon.green", "obo.sh", "rollenspiel.social", "todon.eu", "veganism.social"]

# Add server and account_unique columns
for list in list_of_data:
    for toot in list:
        toot['server'] = toot['account']['acct'].split("@")[-1]
        toot['account_unique'] = toot['account']['acct']

# Create dataframes
list_of_df = []
for list in list_of_data:
    df = pd.DataFrame(list)
    df = df.drop_duplicates(subset=['account_unique']).reset_index(drop=True)
    list_of_df.append(df)


# Create a list of all connections from downloaded instances to other instances
list_of_connections = []
for df in list_of_df:
    no_accounts_from_servers = df["server"].value_counts()
    list_of_connections.append(no_accounts_from_servers)

#normalise connections
for connections in list_of_connections:
    total = sum(connections)
    for server in connections.index:
        connections[server] = connections[server]/total


# Create a df of servers and their connections
df_connections = pd.DataFrame()
x = 0
for i, connections in enumerate(list_of_connections):    
    for server in connections.index:        
        if server in names_of_servers:
            df_connections.at[x, "server"] = names_of_servers[i]
            df_connections.at[x, "origin_server"] = server
            df_connections.at[x, "weight"] = connections[server]
            x += 1
            
# Create a graph
G = nx.from_pandas_edgelist(df_connections, "server", "origin_server", "weight", create_using=nx.DiGraph())

# Create a list of edge weights
edge_weights = [d["weight"] * 100 for _, _, d in G.edges(data=True)]


# Plot the graph
plt.figure(figsize=(10,10))
nx.draw(G, with_labels=True, node_size=100, font_size=10, font_color="black", node_color="green", edge_color="black", width=edge_weights)

#save the graph as image
plt.savefig("network_analysis.png", dpi=300)