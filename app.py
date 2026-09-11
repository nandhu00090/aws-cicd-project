import time
import os
import redis
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Puthu Database Table (Tracker)
class MediaTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., MCU, Anime
    release_year = db.Column(db.Integer, nullable=False)
    arc_details = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
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
    # Sort by Year logically
    media_list = MediaTracker.query.order_by(MediaTracker.release_year.asc()).all()
    return render_template('index.html', count=count, media_list=media_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
