import time
import os
import redis
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# 🛑 TRICK 1: Database URL illana, temporary SQLite-ah use pannu
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MediaTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    arc_details = db.Column(db.String(200), nullable=True)

def init_db():
    retries = 5
    while retries > 0:
        try:
            with app.app_context():
                db.create_all()
            break
        except Exception as e:
            retries -= 1
            time.sleep(3)

init_db()

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                # 🛑 TRICK 2: Redis illana crash aagama '0' nu anuppu
                return 0 
            retries -= 1
            time.sleep(0.5)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        year = request.form.get('year')
        arc = request.form.get('arc')
        
        if title and year:
            new_media = MediaTracker(title=title, category=category, release_year=year, arc_details=arc)
            db.session.add(new_media)
            db.session.commit()
        return redirect(url_for('home'))

    count = get_hit_count()
    media_list = MediaTracker.query.order_by(MediaTracker.release_year.asc()).all()
    return render_template('index.html', count=count, media_list=media_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

