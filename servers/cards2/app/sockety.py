from app import socketio
from app.database import users, games, get_game_from_id, get_user_from_id
from app.logconfig import logger
from flask_login import current_user
from flask import jsonify
from flask_socketio import join_room, leave_room

print (dir(socketio))

@socketio.on('ready')
def ready(data):
    logger.info(current_user)
    logger.info(data)
    id = current_user.id
    name = current_user.name
    game = data['game']
    actual_game = get_game_from_id(game)
    if actual_game is not None:
        actual_game.players[id].ready = True
        socketio.emit('player_ready', {'name':name})
        say_game_ready(actual_game)
   