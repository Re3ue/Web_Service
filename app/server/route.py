########## ########## ########## ##########

# Import : External
from flask import Blueprint, render_template

########## ########## ########## ##########

blueprint_route = Blueprint('blueprint_route', __name__)

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
