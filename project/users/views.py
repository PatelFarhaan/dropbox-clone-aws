from project import db
from project.models import Users
from project.users.forms import UpdateUserForm
from project.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint, session


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        email = request.form.get('email', None)
        name = request.form.get('name', None)
        password = request.form.get('password', None)
        repeat_password = request.form.get('repeat_password', None)

        if email is None or email == '':
            return render_template('register.html', warning='Email cannot be Empty')

        if password is None or password == '':
            return render_template('register.html', warning='Password cannot be Empty')

        if repeat_password is None or repeat_password == '':
            return render_template('register.html', warning='Confirm Password cannot be Empty')

        if name is None or name == '':
            return render_template('register.html', warning='Name cannot be Empty')


        if not (password == repeat_password):
            return render_template('register.html', warning='Both passwords should be same.')


        existing_user_email = Users.query.filter_by(email=email).first()

        if existing_user_email is not None:
            return render_template('register.html', warning='Email already exists. Please login to continue')

        else:
            new_user = Users(email=email,
                            name=name,
                            hashed_password=generate_password_hash(password))

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('users.login'))
    return render_template('register.html')


@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email', 'None')
        password = request.form.get('password', 'None')

        if email == None:
            return render_template('login.html', warning='Email cannot be Empty')

        if password == None:
            return render_template('login.html', warning='Password cannot be Empty')

        user = Users.query.filter_by(email=email).first()

        if user == None:
            return render_template('login.html', warning='Email Does not exist!!!')

        elif check_password_hash(user.hashed_password, password):
            login_user(user)
            session['email'] = user.email
            return redirect(url_for('users.after_login'))
        else:
            return render_template('login.html', warning='Password is incorrect')
    return render_template('login.html')


@users_blueprint.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Information updated Successfully')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


# @users_blueprint.route('/<username>')
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = Users.query.filter_by(username=username).first_or_404()
    # blog_post = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    # return render_template('user_blog_post.html',
    #                         blog_post=blog_post,
    #                         user=user)


@users_blueprint.route('/after-login', methods=['GET', 'POST'])
def after_login():
    user_name = Users.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        file_obj = request.files.get('file_obj', None)
        filename = file_obj.filename

    return render_template('after_login.html', user_name=user_name.name)