from project import db
from project.models import Users
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
        email = request.form.get('email', None)
        name = request.form.get('name', None)
        password = request.form.get('password', None)
        gender = request.form.get('gridRadios', None)
        repeat_password = request.form.get('repeat_password', None)
        dob = request.form.get('date_of_birth', None)
        resume = request.files.get('resume', None)
        resume_name = resume.filename

        if email is None or email == '':
            return render_template('register.html', warning='Email cannot be Empty')

        if password is None or password == '':
            return render_template('register.html', warning='Password cannot be Empty')

        if repeat_password is None or repeat_password == '':
            return render_template('register.html', warning='Confirm Password cannot be Empty')

        if name is None or name == '':
            return render_template('register.html', warning='Name cannot be Empty')

        if gender is None:
            return render_template('register.html', warning='Gender cannot be Empty')

        if dob is None or dob == '':
            return render_template('register.html', warning='Date of Birth cannot be Empty')

        if resume is None or resume.filename == '':
            return render_template('register.html', warning='Resume cannot be Empty')

        if not (password == repeat_password):
            return render_template('register.html', warning='Both passwords should be same.')



        import boto3

        bucket = 'application-tracking-system-test'
        s3 = boto3.client('s3',
                          aws_access_key_id='ASIAXORRZPURJFTDV6NH',
                          aws_secret_access_key='PKJW2YdtuWauC69t06R8cyoB9p1zW6vBXy0tu6ls',
                          aws_session_token='FQoGZXIvYXdzEDoaDHCIiNOXHkcuipq8/CKCAkOCge4lCXFZIwNRkXmSXKniaZ8yDRKKDbw6LFv3k9eyaa21xolA5XA5L9U2T7ucZ+zHqGbvhM89yuDFV4RGGTCBYRtxZ7vE70pvegzVlXp7zWcR1TsnVmnSfyRuKMITOt3uq0+QG3uLOj4uQ6MWmaFRbumuwe78UFai/TTDsSQ6nv+JIY8+RYCpU3MZ+167p2qVfECNLJAhH01xc/hy/miHkbcwKoLT6AP6Rp3rbDsZvSneggh7W6lcs+72Ls/ ETgapyfsWhbKtF / lk1OPrQqhtWo6P0IKhyRabWOhaRvzpPZPrGSxVyTH1UwWylI5UpteF0upzU3afg5rhXW6l4tPa6yiL69bsBQ=='
                          )

        def upload_file_to_s3(file, bucket_name, acl="public-read"):

            try:

                resp = s3.upload_fileobj(
                    file,
                    bucket_name,
                    file.filename,
                    ExtraArgs={
                        "ACL": acl,
                        "ContentType": file.content_type
                    }
                )
                print(resp)

            except Exception as e:
                # This is a catch all exception, edit this part to fit your needs.
                print("Something Happened: ", e)

        upload_file_to_s3(resume, bucket)



        # existing_user_email = Users.query.filter_by(email=email).first()
        # existing_user_username = Users.query.filter_by(username=username).first()

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


# @users_blueprint.route('/<username>')
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = Users.query.filter_by(username=username).first_or_404()
    # blog_post = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    # return render_template('user_blog_post.html',
    #                         blog_post=blog_post,
    #                         user=user)