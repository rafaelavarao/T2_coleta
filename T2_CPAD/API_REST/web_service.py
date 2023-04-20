from flask import Flask
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
import pandas as pd
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

#Lendo o csv
df = pd.read_csv('games.csv')
#Mudando o nome da primeira coluna para "Index"
df.rename({'Unnamed: 0' : 'Index'}, axis=1, inplace=True)

##Transformando o data frame em dicionario
GAMES = df.to_dict()

 #Todo
# shows a single games and lets you delete a Country

def abort_if_game_doesnt_exist(games_id):
    if games_id not in GAMES:
        abort(404, message=f'Games {games_id} doesn\'t exist')

parser = reqparse.RequestParser()
parser.add_argument('Index')
parser.add_argument('Title')
parser.add_argument('Release Date')
parser.add_argument('Team')
parser.add_argument('Rating')
parser.add_argument('Times Listed')
parser.add_argument('Number of Reviews')
parser.add_argument('Genres')
parser.add_argument('Summary')
parser.add_argument('Reviews')
parser.add_argument('Plays')
parser.add_argument('Playing')
parser.add_argument('Backlogs')
parser.add_argument('Wishlist')

class Games(Resource):
    def get(self, games_id):
        abort_if_game_doesnt_exist(games_id)
        return GAMES[games_id]

    def delete(self, games_id):
        abort_if_game_doesnt_exist(games_id)
        del GAMES[games_id]
        return '', 204

    def put(self, games_id):
        args = parser.parse_args()
        content = {'Index': args['Index'], 'Title': args['Title'],
                   'Release Date': args['Release Date'], 'Team': args['Team'],
                   'Rating': args['Rating'], 'Times Listed': args['Times Listed'],
                   'Number of Reviews': args['Number of Reviews'], 'Genres': args['Genres'],
                   'Summary': args['Summary'], 'Reviews': args['Reviews'],
                   'Plays': args['Plays'], 'Playing': args['Playing'],
                   'Backlogs': args['Backlogs'], 'Wishlist': args['Wishlist']}
        GAMES[games_id] = content
        return content, 201


class GameList(Resource):
    def get(self):
        return GAMES
    
    def post(self):
        args = parser.parse_args()
        games_id = max(GAMES.keys()) + 1
        GAMES[games_id] = {'Index': args['Index'], 'Title': args['Title'],
                           'Release Date': args['Release Date'], 'Team': args['Team'],
                           'Rating': args['Rating'], 'Times Listed': args['Times Listed'],
                           'Number of Reviews': args['Number of Reviews'], 'Genres': args['Genres'],
                           'Summary': args['Summary'], 'Reviews': args['Reviews'],
                           'Plays': args['Plays'], 'Playing': args['Playing'],
                           'Backlogs': args['Backlogs'], 'Wishlist': args['Wishlist']}
        return GAMES[games_id], 201
    

## Actually setup the Api resource routing here
api.add_resource(GameList, '/game', endpoint="Game")
api.add_resource(Games, '/game/<int:games_id>', endpoint="gamesId")


if __name__ == '__main__':
    app.run(debug=False)
    
