from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "build-a-blog.db"))
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    flag = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.flag = False

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_post_id = int(request.form['blog-post-id'])
        blog_post = Blog.query.get(blog_post_id)
        blog_post.flag = True
        db.session.add(blog_post)
        db.session.commit()
        return redirect('/')    

    blog_posts = Blog.query.filter_by(flag=False).all()
    flaged_posts = Blog.query.filter_by(flag=True).all() 

    return render_template(
        'build-a-blog.html', 
        title='Telling it on a Mountain!', 
        blog_posts=blog_posts,
        flaged_posts=flaged_posts,
        )

@app.route('/The-Mountain', methods=['POST', 'GET'])
def add_blog_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['blog_post']
        new_post = Blog(title,body)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

    return render_template(
        'the-mountain.html',
        title='The Mountain!'
    )

if __name__ == '__main__':
    app.run()
