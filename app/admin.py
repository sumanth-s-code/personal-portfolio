"""
Admin module for the Personal Portfolio app.

Provides routes for the admin panel to manage projects and blog posts.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from .db import get_db

bp = Blueprint('admin', __name__)

def admin_required(func):
    """
    Decorator to require admin login for a route.
    """
    from functools import wraps
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in as admin to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view

@bp.route('/dashboard')
@admin_required
def dashboard():
    """
    Admin dashboard displaying projects and blog posts.
    """
    db = get_db()
    projects = db.execute(
        'SELECT id, title, created FROM projects ORDER BY created DESC'
    ).fetchall()
    blog_posts = db.execute(
        'SELECT id, title, created FROM blog_posts ORDER BY created DESC'
    ).fetchall()
    return render_template('admin_dashboard.html', projects=projects, blog_posts=blog_posts)

@bp.route('/project/new', methods=['GET', 'POST'])
@admin_required
def new_project():
    """
    Create a new project.
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        link = request.form.get('link', '').strip()
        if not title or not description:
            flash('Title and description are required.', 'danger')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO projects (title, description, link) VALUES (?, ?, ?)',
                (title, description, link)
            )
            db.commit()
            flash('Project added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin_edit_project.html', project=None)

@bp.route('/project/edit/<int:project_id>', methods=['GET', 'POST'])
@admin_required
def edit_project(project_id):
    """
    Edit an existing project.
    """
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        link = request.form.get('link', '').strip()
        if not title or not description:
            flash('Title and description are required.', 'danger')
        else:
            db.execute(
                'UPDATE projects SET title = ?, description = ?, link = ? WHERE id = ?',
                (title, description, link, project_id)
            )
            db.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    else:
        project = db.execute(
            'SELECT id, title, description, link FROM projects WHERE id = ?',
            (project_id,)
        ).fetchone()
        if project is None:
            flash('Project not found.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return render_template('admin_edit_project.html', project=project)

@bp.route('/project/delete/<int:project_id>', methods=['POST'])
@admin_required
def delete_project(project_id):
    """
    Delete a project.
    """
    db = get_db()
    db.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    db.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@bp.route('/blog/new', methods=['GET', 'POST'])
@admin_required
def new_blog():
    """
    Create a new blog post.
    """
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'danger')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO blog_posts (title, content) VALUES (?, ?)',
                (title, content)
            )
            db.commit()
            flash('Blog post added successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin_edit_blog.html', post=None)

@bp.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def edit_blog(post_id):
    """
    Edit an existing blog post.
    """
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('Title and content are required.', 'danger')
        else:
            db.execute(
                'UPDATE blog_posts SET title = ?, content = ? WHERE id = ?',
                (title, content, post_id)
            )
            db.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    else:
        post = db.execute(
            'SELECT id, title, content FROM blog_posts WHERE id = ?',
            (post_id,)
        ).fetchone()
        if post is None:
            flash('Blog post not found.', 'danger')
            return redirect(url_for('admin.dashboard'))
        return render_template('admin_edit_blog.html', post=post)

@bp.route('/blog/delete/<int:post_id>', methods=['POST'])
@admin_required
def delete_blog(post_id):
    """
    Delete a blog post.
    """
    db = get_db()
    db.execute('DELETE FROM blog_posts WHERE id = ?', (post_id,))
    db.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
