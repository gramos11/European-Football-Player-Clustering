# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:25:10 2023

@author: Graduate
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from unidecode import unidecode
import numpy as np

data = pd.read_csv('Big5Europe_playerstatsFULL.csv')
data = data.fillna(0)
data['Player'] = data['Player'].apply(unidecode)

positions = pd.read_csv('Player_Positions.csv', encoding='ISO-8859-1', sep='\t')
positions['Player'] = positions['Player'].apply(unidecode)
merged_data = pd.merge(data, positions, on='Player', how='left')
data = merged_data.dropna(subset=['Main Position'])

feature_indices = list(range(11, 109))
features = data.iloc[:, feature_indices]

scaler = StandardScaler()
try:
    scaled_features = scaler.fit_transform(features)
except ValueError:
    features.replace([np.inf, -np.inf], 0, inplace=True)
    scaled_features = scaler.fit_transform(features)

num_components = 25  # Choose the number of components based on your requirements
pca = PCA(n_components=num_components, random_state=1129)
pca_result = pca.fit_transform(scaled_features)

pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i}' for i in range(1, num_components + 1)])
data = data.reset_index(drop=True)
pca_df = pca_df.reset_index(drop=True)
data_with_pca = pd.concat([data, pca_df], axis=1)

selected_player = pd.DataFrame(data_with_pca[data_with_pca['Player'] == 'Harry Kane'].iloc[0]).T
selected_position = selected_player['Main Position'].values[0]
filtered_data = data_with_pca[data_with_pca['Main Position'] == selected_position]
filtered_data = filtered_data.reset_index(drop=True)
pca_feature_indices = list(range(110, 110 + num_components))
pca_features = filtered_data.iloc[:, pca_feature_indices]

k_values = range(1, 25)  # You can adjust this range based on your needs
inertia_values = []
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=1129)
    kmeans.fit(pca_features)
    inertia_values.append(kmeans.inertia_)

plt.figure(figsize=(8, 6))
plt.plot(k_values, inertia_values, marker='o')
plt.title('Elbow Plot for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.savefig('elbow.png')
plt.show()

num_clusters = 15
kmeans = KMeans(n_clusters=num_clusters, random_state=1129)
clusters = kmeans.fit_predict(pca_features)

filtered_data['Cluster'] = clusters
player_index = filtered_data.index[filtered_data['Player'] == 'Harry Kane'].tolist()
player_index = player_index[0]
player_cluster = clusters[player_index]
cluster_players = filtered_data[filtered_data['Cluster'] == player_cluster]
similarity_scores = cosine_similarity(selected_player.iloc[:, 110:135].values, cluster_players.iloc[:, 110:135].values).T
cluster_players['Similarity'] = similarity_scores.flatten()
cluster_players = cluster_players[cluster_players['Player'] != 'Harry Kane']
sorted_players = cluster_players.sort_values(by='Similarity', ascending=False)[:10]


import seaborn as sns

sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=filtered_data)
plt.title('Cluster Scatterplot')
plt.show()


import seaborn as sns

similarity_matrix = cosine_similarity(cluster_players.iloc[:, 110:135].values).T
sns.heatmap(similarity_matrix, cmap='viridis', xticklabels=cluster_players['Player'], yticklabels=cluster_players['Player'])
plt.title('Cosine Similarity Heatmap')
plt.show()
