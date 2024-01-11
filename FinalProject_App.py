# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 20:06:22 2023

@author: Graduate
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
import streamlit as st
from unidecode import unidecode
import numpy as np

data = pd.read_csv('Big5Europe_playerstatsFULL.csv')
data = data.fillna(0)
data['Player'] = data['Player'].apply(unidecode)

positions = pd.read_csv('Player_Positions.csv', encoding='ISO-8859-1', sep='\t')
positions['Player'] = positions['Player'].apply(unidecode)
merged_data = pd.merge(data, positions, on='Player', how='left')
data = merged_data.dropna(subset=['Main Position'])

# Select features for PCA (adjust the range as needed)
feature_indices = list(range(11, 109))
features = data.iloc[:, feature_indices]

# Scale features
scaler = StandardScaler()
try:
    scaled_features = scaler.fit_transform(features)
except ValueError:
    features.replace([np.inf, -np.inf], 0, inplace=True)
    scaled_features = scaler.fit_transform(features)

# Apply PCA
num_components = 25  # Choose the number of components based on your requirements
pca = PCA(n_components=num_components, random_state=1129)
pca_result = pca.fit_transform(scaled_features)

# Create a DataFrame with PCA results
pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i}' for i in range(1, num_components + 1)])

data = data.reset_index(drop=True)
pca_df = pca_df.reset_index(drop=True)
data_with_pca = pd.concat([data, pca_df], axis=1)

st.title("Player Similarity App")

# Input: Player Name
player_name_input = st.text_input("Enter a player's name:")

if st.button("Find Similar Players"):
    # Find the position of the entered player
    selected_player = pd.DataFrame(data_with_pca[data_with_pca['Player'] == player_name_input].iloc[0]).T

    if not selected_player.empty:
        selected_position = selected_player['Main Position'].values[0]

        # Filter data based on position
        filtered_data = data_with_pca[data_with_pca['Main Position'] == selected_position]

        # Reset index to avoid misalignment
        filtered_data = filtered_data.reset_index(drop=True)

        pca_feature_indices = list(range(110, 110 + num_components))
        pca_features = filtered_data.iloc[:, pca_feature_indices]

        # scaler = StandardScaler()
        # try:
        #     scaled_features = scaler.fit_transform(features)
        # except ValueError:
        #     features.replace([np.inf, -np.inf], 0, inplace=True)
        #     scaled_features = scaler.fit_transform(features)

        # Apply K-Means Clustering
        num_clusters = 15
        kmeans = KMeans(n_clusters=num_clusters, random_state=1129)
        clusters = kmeans.fit_predict(pca_features)

        filtered_data['Cluster'] = clusters

        # Find cluster of the entered player
        player_index = filtered_data.index[filtered_data['Player'] == player_name_input].tolist()

        if player_index:
            player_index = player_index[0]
            player_cluster = clusters[player_index]

            # Get other players in the same cluster
            cluster_players = filtered_data[filtered_data['Cluster'] == player_cluster]

            #selected_features_scaled = scaler.transform(selected_player.iloc[:, 11:105].values)
            #similarity_scores = cosine_similarity(selected_features_scaled, cluster_players.iloc[:, 11:105].values).T

            similarity_scores = cosine_similarity(selected_player.iloc[:, 110:135].values, cluster_players.iloc[:, 110:135].values).T

            # Add similarity scores to the DataFrame
            cluster_players['Similarity'] = similarity_scores.flatten()

            cluster_players = cluster_players[cluster_players['Player'] != player_name_input]

            # Sort players by similarity
            sorted_players = cluster_players.sort_values(by='Similarity', ascending=False)[:10]

            # Display similar players
            st.write(f"Players in the same cluster as {player_name_input} in the position of {selected_position} (sorted by similarity):")
            for i, (_, row) in enumerate(sorted_players.iterrows(), 1):
                st.write(f"{i}. {row['Player']} ({row['Age']:.0f} years old): {row['Squad']} - Similarity: {row['Similarity']:.4f}")
        else:
            st.write(f"Player {player_name_input} not found in the filtered dataset.")
    else:
        st.write(f"Player {player_name_input} not found.")



