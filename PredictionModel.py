import sqlite3
import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from tensorflow.keras import models, layers


def goal_results(row):
    if row.winner == 'A':
        return row.goal_difference * -1
    else:
        return row.goal_difference


def point_results(row):
    if row.winner == 'A':
        return 0
    elif row.winner == 'D':
        return 1
    else:
        return 3


class PredictionModel:
    def __init__(self):
        self.conn = sqlite3.connect('premier_league.db')
        try:
            self.model = tf.keras.models.load_model('model')
        except Exception:
            self.model = self.learn_model()

    def learn_model(self):
        sql_query = pd.read_sql_query(
            "select * from Historical_matches", self.conn)
        df = pd.DataFrame(sql_query, columns=['home_team', 'away_team', 'season', 'winner', 'goal_difference'])
        df['season'] = [x[:-3] for x in df['season']]
        df['season'] = df['season'].astype('int32')

        df['result'] = df.apply(goal_results, axis=1)
        df['points'] = df.apply(point_results, axis=1)

        for i in range(1, 5):
            df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'home_team', 'result']].groupby(['next_season', 'home_team']).mean()
            result_by_year = result_by_year.rename({'next_season': 'season'})
            df = df.join(result_by_year, rsuffix="_{i}", on=['season', 'home_team']).fillna(0)
            # df = df.drop(columns = ['season_1'])

            df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'home_team', 'points']].groupby(['next_season', 'home_team']).sum()
            result_by_year = result_by_year.rename({'next_season': 'season'})
            df = df.join(result_by_year, rsuffix=f"_h{i}", on=['season', 'home_team']).fillna(27)

            df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'away_team', 'points']].groupby(['next_season', 'away_team']).sum()
            result_by_year = result_by_year.rename({'next_season': 'season'})
            df = df.join(result_by_year, rsuffix=f"_a{i}", on=['season', 'away_team']).fillna(27)

            df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'home_team', 'away_team', 'result']]
            result_by_year = result_by_year.rename(columns={'next_season': 'season'})
            df = df.merge(result_by_year, how='left', suffixes=[None, f"_same_team_h{i}"],
                          on=['season', 'home_team', 'away_team'])
            df = df.rename(columns={'resultNone': 'result'})

            '''df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'home_team', 'away_team', 'result']]
            result_by_year = result_by_year.rename(columns={'next_season':'season', 'home_team':'away_team', 'away_team':'home_team'})
            print(result_by_year)
            df = df.merge(result_by_year, how='left', suffixes=[None, f"_same_team_a{i}"], on=['season', 'home_team', 'away_team'])
            df = df.rename(columns={'resultNone' : 'result'})'''

        df = df.drop(columns=['next_season']).fillna(0)
        dummy = pd.get_dummies(df.winner)
        df = pd.concat([df, dummy], axis=1)
        df = df.loc[df['season'] > 1998]
        df = df.drop(columns=['season', 'points', 'winner', 'goal_difference', 'home_team', 'away_team'])
        x = df.drop(columns=['result', 'A', 'D', 'H']).to_numpy()
        y = df[['A', 'H', 'D']].to_numpy()

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        network = models.Sequential()
        network.add(layers.Dense(128, activation='relu', input_shape=(x_train.shape[1],)))
        network.add(layers.Dense(32, activation='relu'))
        network.add(layers.Dense(3, activation='softmax'))
        network.compile(optimizer='adam', loss=tf.keras.losses.CategoricalCrossentropy(), metrics=['acc'])
        network.fit(x_train, y_train, epochs=90, batch_size=128, validation_split=0.2)
        network.save('model')
        return network
