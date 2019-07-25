from flask import Flask, request, render_template,redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "blogz.db"))
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):

        self.username = username
        self.password = password

@app.before_request
def require_login():
    
    allowed_routes = ['login', 'register']

    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/The-Mountain', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_post_id = int(request.form['blog-post-id'])
        blog_post = Blog.query.get(blog_post_id)
        db.session.add(blog_post)
        db.session.commit()
        return redirect('/The-Mountain')    

    blog_posts = Blog.query.all()

    return render_template(
        'the-mountain.html', 
        title='The Mountain!', 
        blog_posts=blog_posts,
        )

@app.route('/Go-Tell-It-On-A-Mountain', methods=['POST', 'GET'])
def add_blog_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['blog_post']
        post = {'title': title, 'body':body}
        new_post = Blog(title,body)
        db.session.add(new_post)
        db.session.commit()
        return render_template(
            'i-said-it.html',
            title='I said it!',
            post=post,
        )

    return render_template(
        'telling-it-on-a-mountain.html',
        title='Go Tell it on a Mountain!'
    )

@app.route('/I-said-it!')
def display_post():

    post_id = request.args.get('id')
    post = Blog.query.get(post_id)

    return render_template(
        'i-said-it.html',
        title='I said it!',
        post=post
    )

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:

            flash('Logged in')
            session['username'] = username

            return redirect('/ ') 

        if not user:

            flash('User does not exist', 'error')

        if  user and user.password != password:

            flash('Password does not match user', 'error')   

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user and password == verify:

            db.session.add(User(username, password))
            db.session.commit()
            session['username'] = username

            return redirect('/')

        if existing_user:
            flash('Duplicate User', 'error')

        if not existing_user and password != verify:
            flash('Passwords do not match!', 'error')

    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()
