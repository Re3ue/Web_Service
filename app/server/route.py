########## ########## ########## ##########

# Import : External
from flask import Blueprint, render_template

########## ########## ########## ##########

blueprint_route = Blueprint('blueprint_route', __name__)

# All

@blueprint_route.route('/')
def main() :
    return render_template('index.html')

@blueprint_route.route('/about')
def about() :
    return render_template('about.html')

@blueprint_route.route('/profile')
def profile() :
    return render_template('profile.html')

@blueprint_route.route('/sign_in')
def sign_in() :
    return render_template('sign_in.html')

@blueprint_route.route('/sign_up')
def sign_up() :
    return render_template('sign_up.html')

# All - Post + ID

@blueprint_route.route('/post/<int:post_id>')
def post(post_id) :
    return render_template('post.html')

# Authenticate

@blueprint_route.route('/create_post')
def create_post() :
    return render_template('create_post.html')

@blueprint_route.route('/edit_post')
def edit_post() :
    return render_template('edit_post.html')
