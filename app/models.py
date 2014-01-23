#encoding:utf-8
from app import db
import md5

team_users = db.Table('team_users',
        db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        )

team_admins = db.Table('team_admins',
        db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        )

team_tags = db.Table('team_tags',
        db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        )

user_likes = db.Table('user_likes',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
        )

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40))
    events = db.relationship('Event', lazy='dynamic')

class Team(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(40), unique=True)
    intro = db.Column(db.String(240))
    image_url = db.Column(db.String(92), default='')
    events = db.relationship('Event', lazy='dynamic')
    admins = db.relationship('User', lazy='dynamic', secondary=team_admins)
    tags = db.relationship('Tag', lazy='dynamic', secondary=team_tags)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    email = db.Column(db.String(150), unique = True)
    pwdhash = db.Column(db.String(32))
    image_url = db.Column(db.String(92), default='')
    like_events = db.relationship('Event', lazy='dynamic', secondary=user_likes)
    teams = db.relationship('Team', lazy='dynamic', backref=db.backref('users',
        lazy='dynamic'),  secondary=team_users)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = md5.new(password).hexdigest()

    def check_password(self, password):
        return self.pwdhash == md5.new(password).hexdigest()
    
    # likes
    def like(self, event):
        if not self.is_like(event):
            self.like_events.append(event)
            event.likes += 1
    
    def dislike(self, event):
        if self.is_like(event):
            self.like_events.remove(event)
            event.likes -= 1

    def is_like(self, event):
        return event in self.like_events.all()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(180))
    content = db.Column(db.String(450))
    likes = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime)
    photos = db.relationship('Photo', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(380))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.String(180))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

