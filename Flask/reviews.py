from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    review = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, review):
        self.title = title
        self.review = review 

with app.app_context():
    db.create_all()

@app.route('/')
def show_reviews():
    review = reviews.query.all()
    print(review)
    return render_template('index.html', review=review)

@app.route('/add', methods=['POST'])
def add_review():
    title = request.form['title']
    review = request.form['review']
    new_review = reviews(title=title, review=review)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('show_reviews'))

@app.route('/toggle/<int:id>')
def toggle_seen(id):
    review = reviews.query.get(id)
    review.seen = not review.seen
    db.session.commit()
    return redirect(url_for('show_reviews'))

@app.route('/delete/<int:id>')
def delete_review(id):
    review = reviews.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('show_reviews'))

if __name__ == '__main__':
    app.run(debug=True)
