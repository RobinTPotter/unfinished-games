
from app.models import Player, Game

from app.logconfig import logger

users = {}
p1=Player('robin', 'nobby')
p2=Player('nobby', 'robin')
users[p1.id] = p1 
users[p2.id] = p2



games = {}
ng = Game()
games[ng.id] = ng

logger.info('ceated default users and 2 games {}'.format(users))
logger.info('ceated default users and 2 games {}'.format(games))

def get_game_from_id(game_id):
    game_out = None
    
    if game_id in games:
        game_out = games[game_id]
        
    return game_out    
    
def get_user_from_id(user_id):
    user = None
    
    if user_id in users:
        user = users[user_id]
        
    return user    
     
def get_user_from_name(name):
    user = None
    
    list = [users[u] for u in users if users[u].name==name]
    if len(list)==1: return list[0]
    else: return None
    