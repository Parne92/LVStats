from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import validates
from flask_login import UserMixin

from FlaskProject.LVS_app.views import db

class Player(UserMixin, db.Model):
    __tablename__ = 'player'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(20), unique = True)
    password = db.Column(db.String(100))
    rating = db.Column(Float)

    def __str__(self):
        return self.name

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(Integer, primary_key = True)
    position = db.Column(String(10))
    playerid = Column(Integer, ForeignKey('player.id', ondelete="CASCADE"))
    rating = Column(Float)
    game_date = Column(DateTime)
    goals = Column(Integer)
    assists = Column(Integer)
    tackles = Column(Integer)
    saves = Column(Integer)
    time = Column(Integer)
    
    def __str__(self):
        return f"{self.player}, {self.position}: {self.rating} ON {self.game_date:%x}"