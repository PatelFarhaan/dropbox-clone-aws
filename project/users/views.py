from project import db
from project.models import User, BlogPost
from project.users.forms import UpdateUserForm
from project.users.picture_handler import add_profile_pic
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, Blueprint


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
        name = request.form.get('name', 'None')
        email = request.form.get('email', 'None')
        password = request.form.get('password', 'None')
        gender = request.form.get('gridRadios', 'None')
        repeat_password = request.form.get('repeat_password', 'None')
        # dob = request.form.get('date_of_birth', 'None')
        resume = request.files.get('resume', 'not resume')
        from werkzeug import secure_filename
        # resp = resume.save(secure_filename(resume.filename))
        print(resume)
        # print(name, email, password, repeat_password, gender, dob)

        existing_user_email = User.query.filter_by(email=email).first()
        # existing_user_username = User.query.filter_by(username=username).first()

        # if existing_user_email is not None:
        #     return render_template('register.html', warning='Email already exists. Please login to continue')
        # elif existing_user_username is  not None:
        #     return render_template('register.html', warning='Username already exists. Please try with a new username')

        # if password != repeat_password:
        #     return render_template('register.html', warning='Passwords should be same!!!')
        # else:
            # new_user = User(email=email,
                            # username=username.replace(' ', ''),
                            # password=password)

            # db.session.add(new_user)
            # db.session.commit()
            # return redirect(url_for('users.login'))
    return render_template('register.html')


@users_blueprint.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email', 'None')
        password = request.form.get('password', 'None')
        user = User.query.filter_by(email=email).first()

        if user == None:
            return render_template('login.html', warning='Email Does not exist!!!')
        elif user.check_hashed_password(password) and user is not None:
            login_user(user)
            return redirect(url_for('core.index'))
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


@users_blueprint.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_post = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_post.html',
                            blog_post=blog_post,
                            user=user)