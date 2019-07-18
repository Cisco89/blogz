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

    def __init__(self, title, body):
        self.title = title
        self.body = body

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

if __name__ == '__main__':
    app.run()
