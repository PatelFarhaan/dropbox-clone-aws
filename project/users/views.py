import sys
sys.path.append('../../')

import os
import boto3
import shutil
from project import db, app
from project.users.models import Users, Storage
from project.users.lambda_sns import lambda_message_sns
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, url_for, redirect, request, Blueprint, session

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('users.login'))


@users_blueprint.route('/register', methods=['GET','POST'])
def register():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', None)
        name = request.form.get('name', None)
        password = request.form.get('password', None)
        mobile_number = request.form.get('mobile_number', None)
        repeat_password = request.form.get('repeat_password', None)


        if email is None or email == '':
            return render_template('register.html', warning='Email cannot be Empty')

        if password is None or password == '':
            return render_template('register.html', warning='Password cannot be Empty')

        if repeat_password is None or repeat_password == '':
            return render_template('register.html', warning='Confirm Password cannot be Empty')

        if mobile_number == None:
            return render_template('login.html', warning='Mobile Number cannot be Empty')

        if name is None or name == '':
            return render_template('register.html', warning='Name cannot be Empty')


        if not (password == repeat_password):
            return render_template('register.html', warning='Both passwords should be same.')


        existing_user_email = Users.query.filter_by(email=email).first()

        if existing_user_email is not None:
            return render_template('register.html', warning='Email already exists. Please login to continue')

        else:
            new_user = Users(email=email, name=name, mobile_number=mobile_number, hashed_password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            lambda_message_sns(name, mobile_number)
            return redirect(url_for('users.login'))
    return render_template('register.html')



@users_blueprint.route('/login', methods=['GET','POST'])
def login():
    session.clear()
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


@users_blueprint.route('/after-login', methods=['GET', 'POST'])
@login_required
def after_login():
    user = Users.query.filter_by(email=session['email']).first()
    error_flag = False

    try:
        page = request.args.get('page', 1, type=int)
        user_storage_files = Storage.query.filter_by(user_id=user.id).paginate(page=page, per_page=5)
    except:
        error_flag = True

    if request.method == 'POST':
        file_obj = request.files.get('file_obj', None)
        if file_obj:
            file_path = os.getcwd() + '/tmp/'
            if not os.path.exists(file_path):
                os.mkdir(file_path)

            file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file_obj.filename))
            file_obj_path = file_path + f'{file_obj.filename}'
            resp = max_file_size(file_obj_path)
            shutil.rmtree(file_path)
            if not resp:
                return render_template('after_login.html', user_name=user.name, user_storage_files=user_storage_files,
                                       warning='Please upload a file less than 10 MB in size!')
            file_desc = request.form.get("file_desc",None)
            filename = file_obj.filename.replace(' ', '')
            filename = f"{current_user.id}-{filename}"
            storage_files = Storage.query.all()
            files_list = []

            for i in storage_files:
                files_list.append(i.filename)

            if filename is None or filename == '':
                if error_flag:
                    return render_template('after_login.html', user_name=user.name, warning='Please select a fle to upload')
                else:
                    return render_template('after_login.html', user_name=user.name, user_storage_files=user_storage_files,
                                           warning='Please select a fle to upload')
            elif filename in files_list:
                return render_template('after_login.html', user_name=user.name, user_storage_files=user_storage_files,
                                       warning='File already exists. Try with a new file name')

            public_url = file_upload_to_s3(file_obj, filename)
            storage_obj = Storage(
                file=public_url,
                user_id=user.id,
                filename=filename,
                file_desc=file_desc)
            db.session.add(storage_obj)
            db.session.commit()
            page = request.args.get('page', 1, type=int)
            user_storage_files = Storage.query.filter_by(user_id=user.id).paginate(page=page, per_page=5)
            return render_template('after_login.html', user_name=user.name, user_storage_files=user_storage_files)
        else:
            filename = request.form.get('delete_filename', None)
            if filename:
                try:
                    bucket = 'putbox-darshan'
                    s3 = boto3.resource('s3',
                                        aws_access_key_id='***REMOVED_AWS_ACCESS_KEY***',
                                        aws_secret_access_key='***REMOVED_AWS_SECRET_KEY***')
                    file_obj = s3.Object(bucket, filename)
                    file_obj.delete()
                    storage_obj_delete = Storage.query.filter_by(filename=filename).first()
                    db.session.delete(storage_obj_delete)
                    db.session.commit()
                    return redirect(url_for('users.after_login'))
                except:
                    return redirect(url_for('users.after_login'))
        return redirect(url_for('users.after_login'))

    if error_flag:
        return render_template('after_login.html', user_name=user.name)
    else:
        return render_template('after_login.html', user_name=user.name, user_storage_files=user_storage_files)



def file_upload_to_s3(file, object_name):
    bucket = 'putbox-darshan'
    s3 = boto3.client(
        's3',
        aws_access_key_id='***REMOVED_AWS_ACCESS_KEY***',
        aws_secret_access_key='***REMOVED_AWS_SECRET_KEY***'
    )
    s3.upload_fileobj(file, bucket, object_name, ExtraArgs={"ACL": "public-read"})
    public_url = f"https://putbox-darshan.s3-us-west-1.amazonaws.com/{object_name}"
    return public_url


def max_file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        if file_info.st_size > 10000000:
            return False
        else:
            return True