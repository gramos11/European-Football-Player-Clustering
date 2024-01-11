# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:31:29 2023

@author: Graduate
"""

import pandas as pd
import requests
import numpy as np

url = 'https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats'
response = requests.get(url).text.replace('<!--', '').replace('-->', '')
df = pd.read_html(response, header=1)[1]
df = df[df['Rk'] != 'Rk'].reset_index(drop=True)
df['Nation'] = df['Nation'].str[-3:]
df['Pos'] = df['Pos'].str[:2]
keep_cols = np.r_[0:11, 26:37]
df = df.iloc[:, keep_cols]
df.columns = [col.replace('.1', '') for col in df.columns]
df.iloc[:, 6] = df.iloc[:, 6].str[:2]
df.iloc[:, 6:] = df.iloc[:, 6:].astype(float)

shooting_url = 'https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats'
response2 = requests.get(shooting_url).text.replace('<!--', '').replace('-->', '')
df2 = pd.read_html(response2, header=1)[1]
df2 = df2[df2['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[11:16, 22:26]
df2 = df2.iloc[:, keep_cols]
df2 = df2.astype(float)

passing_url = 'https://fbref.com/en/comps/Big5/passing/players/Big-5-European-Leagues-Stats'
response3 = requests.get(passing_url).text.replace('<!--', '').replace('-->', '')
df3 = pd.read_html(response3, header=1)[1]
df3 = df3[df3['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[8:13, 23:32]
df3 = df3.iloc[:, keep_cols]
df3 = df3.drop(['xAG'], axis=1)
df3 = df3.astype(float)
div_cols = np.r_[1:3, 4:13]
df3.iloc[:, div_cols] = df3.iloc[:, div_cols].div(df3.iloc[:, 0], axis=0)
df3 = df3.drop(['90s'], axis=1)

passingType_url = 'https://fbref.com/en/comps/Big5/passing_types/players/Big-5-European-Leagues-Stats'
response4 = requests.get(passingType_url).text.replace('<!--', '').replace('-->', '')
df4 = pd.read_html(response4, header=1)[1]
df4 = df4[df4['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[8, 10:24]
df4 = df4.iloc[:, keep_cols]
df4 = df4.astype(float)
df4 = df4.iloc[:, 1:].div(df4.iloc[:, 0], axis=0)

creation_url = 'https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats'
response5 = requests.get(creation_url).text.replace('<!--', '').replace('-->', '')
df5 = pd.read_html(response5, header=1)[1]
df5 = df5[df5['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[8, 10:17, 18:25]
df5 = df5.iloc[:, keep_cols]
df5 = df5.astype(float)
div_cols = np.r_[2:8, 9:15]
df5.iloc[:, div_cols] = df5.iloc[:, div_cols].div(df5.iloc[:, 0], axis=0)
df5.columns = [col.replace('.1', 'GCA') for col in df5.columns]
df5 = df5.drop(['90s'], axis=1)

defend_url = 'https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats'
response6 = requests.get(defend_url).text.replace('<!--', '').replace('-->', '')
df6 = pd.read_html(response6, header=1)[1]
df6 = df6[df6['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[8:25]
df6 = df6.iloc[:, keep_cols]
df6 = df6.astype(float)
div_cols = np.r_[1:8, 9:17]
df6.iloc[:, div_cols] = df6.iloc[:, div_cols].div(df6.iloc[:, 0], axis=0)
df6.columns = [col.replace('.1', 'Drib') for col in df6.columns]
df6 = df6.drop(['90s'], axis=1)

pos_url = 'https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats'
response7 = requests.get(pos_url).text.replace('<!--', '').replace('-->', '')
df7 = pd.read_html(response7, header=1)[1]
df7 = df7[df7['Rk'] != 'Rk'].reset_index(drop=True)
keep_cols = np.r_[8:31]
df7 = df7.iloc[:, keep_cols]
df7 = df7.astype(float)
div_cols = np.r_[1:10, 11, 13:23]
df7.iloc[:, div_cols] = df7.iloc[:, div_cols].div(df7.iloc[:, 0], axis=0)
df7 = df7.drop(['90s'], axis=1)

data = pd.concat([df, df2, df3, df4, df5, df6, df7], axis=1)

data.to_csv('Big5Europe_playerstatsFULL.csv', index=False)
