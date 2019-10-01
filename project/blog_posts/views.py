from project import db
from project.models import BlogPost
from project.blog_posts.forms import BlogPostForm
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, abort, flash, Blueprint

blogpost_blueprint = Blueprint('blogpost', __name__)


@blogpost_blueprint.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():

        new_post = BlogPost(user_id=current_user.id,
                            title=form.title.data,
                            text=form.text.data)
        db.session.add(new_post)
        db.session.commit()
        flash('New Post Created!!!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


@blogpost_blueprint.route('/<int:blog_post_id>')
@login_required
def blog_post(blog_post_id):
    blogpost = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',
                           title=blogpost.title,
                           date=blogpost.date,
                           text=blogpost.text,
                           post=blogpost)


@blogpost_blueprint.route('/<int:blog_post_id>/update', methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blogpost = BlogPost.query.get_or_404(blog_post_id)

    if blogpost.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blogpost.title=form.title.data
        blogpost.text=form.text.data
        blogpost.user_id=current_user.id
        db.session.commit()
        flash("Blog Post Updated Successfully!!!")
        return redirect(url_for('blogpost.blog_post', blog_post_id=blogpost.id))

    elif request.method == 'GET':

        form.title.data = blogpost.title
        form.text.data = blogpost.text

    return render_template('create_post.html', title='updating', form=form)


@blogpost_blueprint.route('/<int:blog_post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blogpost = BlogPost.query.get_or_404(blog_post_id)

    if blogpost.author != current_user:
        abort(403)

    db.session.delete(blogpost)
    db.session.commit()
    flash("Blog Post Deleted!!!")
    return redirect(url_for('core.index'))
