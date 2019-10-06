import sys
sys.path.append('../../')


from project import db
from project.admin.models import Admin
from werkzeug.security import generate_password_hash



admin_obj = Admin(admin_email='patel.farhaan@gmail.com',
                  admin_hashed_password=generate_password_hash('***REMOVED_PASSWORD***')
                  )
db.session.add(admin_obj)
db.session.commit()
print("Admin Created Successfully!!!")