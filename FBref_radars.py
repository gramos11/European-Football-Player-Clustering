# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:45:37 2023

@author: Graduate
"""
from FBref_percentiles import percentiles
import matplotlib.pyplot as plt
import numpy as np



def radar_plotter_comp(data, player1_name, player2_name):
    # Get stats and position for player 1
    stats1 = data[data['Player'] == player1_name]
    position1 = stats1.iloc[0]['Main Position']
    percentiles1 = percentiles(data, player1_name)

    # Get stats and position for player 2
    #stats2 = data[data['Player'] == player2_name]
    #position2 = stats2.iloc[0]['Main Position']
    percentiles2 = percentiles(data, player2_name)

    labels = ['NPG', 'npxG', 'Shots', 'Ast', 'xAG', 'npxG + xAG', 'SCA', 'Pass Attempts', 'Pass Cmp%', 'PrgP', 'PrgC', 'Take-Ons', 'Touches (Att Pen)', 'PrgR', 'Tkl', 'Int', 'Blk', 'Clr']

    # Create a polar plot
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)

    # Calculate the angles for each axis of the plot
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    # Add the first axis to complete the circle
    angles = np.concatenate((angles, [angles[0]]))

    # Normalize the percentile values to be between 0 and 1 for both players
    normalized_percentiles1 = [p / 100 for p in percentiles1]
    normalized_percentiles1.append(normalized_percentiles1[0])
    normalized_percentiles2 = [p / 100 for p in percentiles2]
    normalized_percentiles2.append(normalized_percentiles2[0])

    # Plot the radar chart for player 1
    ax.plot(angles, normalized_percentiles1, 'o-', linewidth=2, label=player1_name)
    ax.fill(angles, normalized_percentiles1, alpha=0.25)

    # Plot the radar chart for player 2
    ax.plot(angles, normalized_percentiles2, 'o-', linewidth=2, label=player2_name)
    ax.fill(angles, normalized_percentiles2, alpha=0.25)

    # Set the labels for each axis
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)

    # Set the limit for the radial axis
    ax.set_ylim([0, 1])

    # Add a title to the plot
    plot_caption = f'{player1_name} and {player2_name} percentiles compared to {position1}s in the Big 5 European Leagues for 2023-24 season.'
    plt.title(plot_caption, fontsize=10)
    plt.suptitle(f'{player1_name} and {player2_name} per 90 Minutes', y=1.05, fontsize=18, fontweight='bold')

    # Add a legend to the plot
    ax.legend(loc='upper right')

    return fig


radar_plotter_comp(data, 'Harry Kane', 'Jonas Wind')
radar_plotter_comp(data, 'Harry Kane', 'Lautaro Martinez')
radar_plotter_comp(data, 'Harry Kane', 'Lois Openda')

