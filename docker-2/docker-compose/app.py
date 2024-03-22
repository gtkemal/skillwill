from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from redis import Redis, RedisError
import os

app = Flask(__name__)

# Configure SQLAlchemy with PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Connect to Redis
redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)

class VisitorCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    # Increment visit count in Redis
    try:
        visits = redis.incr('counter')
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    # Update visit count in PostgreSQL
    visit_count = VisitorCount.query.first()
    if not visit_count:
        visit_count = VisitorCount(count=1)
        db.session.add(visit_count)
    else:
        visit_count.count += 1
    db.session.commit()

    return f"<h3>Welcome to the Flask App!</h3><p>Redis Visits: {visits}</p><p>PostgreSQL Visits: {visit_count.count}</p>"

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
