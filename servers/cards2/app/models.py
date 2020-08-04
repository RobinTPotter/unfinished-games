from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from config import Config
import json

import uuid

from app.logconfig import logger
from app import socketio

class Player(UserMixin):
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.name = username
        self.set_password(password)
        self.games = []
    def set_password(self, password):
        self.password = generate_password_hash(password)
        logger.info('password reset')
    def check_password(self, password):
        ok = check_password_hash(self.password, password)
        logger.info('password check {0}'.format(ok))
        return ok or Config.NOPASSWORD_CHECK

class Game():
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.players = []
        self.turn = -1
        
    def list_players(self):
        return self.players
    
    def is_player(self,id):
        logger.info('players are {}'.format(self.players))
        logger.info('checking {}'.format(id))
        if id in self.players:
            logger.info('{} in players'.format(id))
            return True            
        else:
            logger.info('{} NOT in players'.format(id))
            return False
    
    def is_open(self):
        if self.turn==-1:
            logger.info('game is open')
            return True            
        else:
            logger.info('game is closed')
            return False
    
    def join(self,id):
        logger.info('joining...')
        if not self.is_player(id):
            self.players.append(id)
            logger.info('{} joined {}'.format(id,self.id))
            return True
    
    def start(self):
        if self.turn==-1:
            self.turn=0
            