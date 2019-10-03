# from project.models import BlogPost
from flask import render_template, request, Blueprint


core_blueprint = Blueprint('core', __name__, template_folder='templates')


@core_blueprint.route('/home')
def home():
    return render_template ('home.html')

@core_blueprint.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    # return render_template('index.html', blog_posts=blog_posts)
    return render_template('index.html')


@core_blueprint.route('/info')
def info():
    return render_template('info.html')
