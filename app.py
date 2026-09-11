import time
import os
import redis
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Table (Model)
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create tables automatic-a
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
    # User form submit panna Database-la save panra code
    if request.method == 'POST':
        name = request.form.get('visitor_name')
        if name:
            new_visitor = Visitor(name=name)
            db.session.add(new_visitor)
            db.session.commit()
        return redirect(url_for('home'))

    # Display panra code
    count = get_hit_count()
    visitors = Visitor.query.order_by(Visitor.id.desc()).limit(5).all()
    return render_template('index.html', count=count, visitors=visitors)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
