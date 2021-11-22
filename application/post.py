from flask import Blueprint, render_template, flash, redirect, abort, request
from flask.helpers import url_for
from flask_login import login_required, current_user
from application.forms import PostForm
from application.models import Post
from application import db
from application.routes import elapsed_time

blueprint = Blueprint('post', __name__, url_prefix='/post')


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new_post():

    form = PostForm()
    if form.validate_on_submit():

        post = Post(content=form.content.data, author=current_user)

        # Store in the database
        db.session.add(post)
        db.session.commit()

        flash("Your post has been created!", 'success')
        return redirect(url_for('routes.index'))

    return render_template('create_post.html', title='New Post', form=form)


@blueprint.route("/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    # Abort if current user isn't the author
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():

        post.content = form.content.data
        post.edited = True
        db.session.commit()
        flash("Your post has been updated!", 'success')

        return redirect(url_for('routes.index'))

    elif request.method == 'GET':

        form.content.data = post.content

    return render_template('edit_post.html', title='Edit Post', form=form, post=post, elapsed_time=elapsed_time)


@blueprint.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    # Abort if current user isn't the author
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')

    return redirect(url_for('routes.index'))
