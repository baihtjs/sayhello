from sayhello import db
from datetime import datetime
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    def __repr__(self):
        return 'Message %r'% self.name