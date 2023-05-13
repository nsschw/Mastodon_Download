import pandas as pd
import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import plotly.graph_objects as go


df = pd.read_pickle('data/master_df.pickle')
df["unique_user_id"] = df["account"].apply(lambda x: x["acct"])

#count the number of posts per user
df_count = df.groupby('unique_user_id').count().reset_index()

#filter out users with less than k posts
k = 5
df_count = df_count[df_count['id'] >= 5]

#filter out users with less than k posts
df = df[df['unique_user_id'].isin(df_count['unique_user_id'])]

# Create a dataframe with the average embedding per user
df_avg = df.groupby('unique_user_id').agg({'embedding': np.mean}).reset_index()



#plot the average embedding using umap and plotly graph objects
reducer = umap.UMAP()
embedding = reducer.fit_transform(np.stack(df_avg['embedding'].values))
df_avg['umap-2d-one'] = embedding[:,0]
df_avg['umap-2d-two'] = embedding[:,1]

fig = go.Figure(data=go.Scatter(
    x=df_avg['umap-2d-one'],
    y=df_avg['umap-2d-two'],
    mode='markers',
    marker=dict(
        size=5,
        color=df_avg['umap-2d-one'], #set color equal to a variable
        colorscale='Viridis', # one of plotly colorscales
        showscale=True
    )
))
fig.write_html("umap.html")



#plot the average embedding per user  and plotly graph objects
tsne = TSNE(n_components=2, verbose=1)
tsne_results = tsne.fit_transform(np.stack(df_avg['embedding'].values))
df_avg['tsne-2d-one'] = tsne_results[:,0]
df_avg['tsne-2d-two'] = tsne_results[:,1]

fig = go.Figure(data=go.Scatter(
    x=df_avg['tsne-2d-one'],
    y=df_avg['tsne-2d-two'],
    mode='markers',
    marker=dict(
        size=5,
        color=df_avg['tsne-2d-one'], #set color equal to a variable
        colorscale='Viridis', # one of plotly colorscales
        showscale=True
    )
))
fig.write_html("tsne.html")