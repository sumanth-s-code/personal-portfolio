"""
Public routes module for the Personal Portfolio app.

Defines view functions for the public portfolio pages.
"""

from flask import Blueprint, render_template
from .db import get_db

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    """
    Home page that displays projects and blog posts.
    """
    db = get_db()
    projects = db.execute(
        'SELECT id, title, description, link, created FROM projects ORDER BY created DESC'
    ).fetchall()
    blog_posts = db.execute(
        'SELECT id, title, created FROM blog_posts ORDER BY created DESC'
    ).fetchall()
    return render_template('index.html', projects=projects, blog_posts=blog_posts)

@bp.route('/project/<int:project_id>')
def project_detail(project_id):
    """
    Display details of a single project.
    """
    db = get_db()
    project = db.execute(
        'SELECT id, title, description, link, created FROM projects WHERE id = ?',
        (project_id,)
    ).fetchone()
    if project is None:
        return "Project not found", 404
    return render_template('project.html', project=project)

@bp.route('/blog/<int:post_id>')
def blog_detail(post_id):
    """
    Display details of a single blog post.
    """
    db = get_db()
    post = db.execute(
        'SELECT id, title, content, created FROM blog_posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    if post is None:
        return "Blog post not found", 404
    return render_template('blog.html', post=post)