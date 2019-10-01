from flask import render_template, request, Blueprint


admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_email = request.form.get('admin_email', None)
        admin_password = request.form.get('admin_password', None)
    return render_template ('admin.html')


@admin_blueprint.route('/create-rc-hr-accounts', methods=['GET', 'POST'])
def create_rc_hr_accounts():
    if request.method == 'POST':
        pass
    return render_template('hr_recruiter_account_create.html')