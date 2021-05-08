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

def reverse_point_results(row):
    if row.winner == 'H':
        return 0
    elif row.winner == 'D':
        return 1
    else:
        return 3

class PredictionModel:
    def __init__(self):
        self.conn = sqlite3.connect('premier_league.db')
        try:
            self.model = tf.keras.models.load_model('model.h5')
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
        df['a_points'] = df.apply(reverse_point_results, axis=1)

        df = self.prepare_data(df)


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
        network.compile(optimizer='adam', loss="categorical_crossentropy", metrics=['acc'])

        network.fit(x_train, y_train, epochs=90, batch_size=128, validation_split=0.2)
        network.save('model.h5')
        return network

    def prepare_data(self, df):
        for i in range(1, 5):
            df['next_season'] = df['season'] + i
            result_by_year = df[['next_season', 'home_team', 'result']].groupby(['next_season', 'home_team']).sum()
            result_by_year['result'] -= \
            df[['next_season', 'away_team', 'result']].groupby(['next_season', 'away_team']).sum()['result']
            result_by_year['result'] = result_by_year['result'] / 38
            result_by_year = result_by_year.rename({'next_season': 'season'})
            df = df.join(result_by_year, rsuffix=f"_{i}", on=['season', 'home_team']).fillna(0)

            result_by_year = df[['next_season', 'home_team', 'points']].groupby(['next_season', 'home_team']).sum()
            result_by_year['points'] += \
            df[['next_season', 'away_team', 'a_points']].groupby(['next_season', 'away_team']).sum()['a_points']
            result_by_year = result_by_year.rename({'next_season': 'season'})
            df = df.join(result_by_year, rsuffix=f"_h{i}", on=['season', 'home_team']).fillna(38)
            result_by_year = result_by_year.rename({'home_team': 'away_team'})
            df = df.join(result_by_year, rsuffix=f"_a{i}", on=['season', 'away_team']).fillna(38)

            result_by_year = df[['next_season', 'home_team', 'away_team', 'result']]
            result_by_year = result_by_year.rename(columns={'next_season': 'season'})
            df = df.merge(result_by_year, how='left', suffixes=[None, f"_same_team_h{i}"],
                          on=['season', 'home_team', 'away_team'])
            df = df.rename(columns={'resultNone': 'result'}).fillna(0)
        df = df.drop(columns=['next_season', 'a_points']).fillna(0)
        return df

    def predict_season(self, season: int):
        if season > 2020 or season < 1998:
            return 0

        sql_query = pd.read_sql_query(
            "select * from Historical_matches", self.conn)
        df = pd.DataFrame(sql_query, columns=['home_team', 'away_team', 'season', 'winner', 'goal_difference'])
        df['season'] = [x[:-3] for x in df['season']]
        df['season'] = df['season'].astype('int32')

        df['result'] = df.apply(goal_results, axis=1)
        df['points'] = df.apply(point_results, axis=1)
        df['a_points'] = df.apply(reverse_point_results, axis=1)

        if season == 2020:
            teams_2020 = ["Liverpool", "Manchester City", "Manchester United", "Chelsea", "Leicester City",
                          "Tottenham Hotspur",
                          "Wolverhampton Wanderers", "Arsenal", "Sheffield United", "Burnley", "Southampton", "Everton",
                          "Newcastle United", "Crystal Palace", "Brighton & Hove Albion", "West Ham United",
                          "Aston Villa",
                          "Leeds United", "West Bromwich Albion", "Fulham"]
            a = []
            for team in teams_2020:
                for t in teams_2020:
                    if t != team:
                        a.append([team, t, season, 0, 0])
            sdf = pd.DataFrame(a, columns=['home_team', 'away_team', 'season', 'winner', 'goal_difference'])
            df = df.append(sdf)

        df = self.prepare_data(df)
        df = df.loc[df['season'] == season]

        if season != 2020:
            dummy = pd.get_dummies(df.winner)
            df = pd.concat([df, dummy], axis=1)
        matches = df[['home_team', 'away_team']]
        df = df.drop(columns=['season', 'points', 'winner', 'goal_difference', 'home_team', 'away_team'])
        if season == 2020:
            X = df.drop(columns=['result']).to_numpy()
        else:
            X = df.drop(columns=['result', 'A', 'D', 'H']).to_numpy()

        predictions = self.model.predict(X)

        results = []
        for i in range(predictions.shape[0]):
            prediction = np.where(predictions[i] == np.max(predictions[i]))

            if prediction[0] == 0:
                results.append('A')
            if prediction[0] == 1:
                results.append('H')
            if prediction[0] == 2:
                results.append('D')

        matches['winner'] = results
        matches['points'] = matches.apply(point_results, axis=1)
        matches['a_points'] = matches.apply(reverse_point_results, axis=1)

        table = matches[['home_team', 'points']].groupby(['home_team']).sum()
        table['points'] += matches[['away_team', 'a_points']].groupby(['away_team']).sum()['a_points']
        table = table.sort_values(by='points', ascending=False)

        return matches, table
