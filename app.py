from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Art %r>' %self.id



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    arts = Art.query.order_by(Art.date.desc()).all()
    return render_template("posts.html", arts=arts)

@app.route('/posts/<int:id>')
def posts_detail(id):
    art = Art.query.get(id)
    return render_template("posts-detail.html", art=art)

@app.route('/posts/<int:id>/delete')
def posts_del(id):
    art = Art.query.get_or_404(id)
    try:
        db.session.delete(art)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    art = Art.query.get(id)
    if request.method == 'POST':
        art.title = request.form['title']
        art.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        art = Art.query.get(id)

        return render_template("posts-update.html", art=art)


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return 'UserID: ' + name + " - " + str(id)

@app.route('/create-art', methods=['POST', 'GET'])
def create_art():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        art = Art(title=title, text=text)

        try:
            db.session.add(art)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-art.html")

if __name__ == '__main__':
    app.run(debug=True)