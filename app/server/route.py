########## ########## ########## ##########

# Import : External
from flask import Blueprint, render_template, session

# Import : File
from .db import open_db
from .authenticate import authenticate_sign_in_sign_out, authenticate_session_account_target_account, authenticate_session_account_post_account

########## ########## ########## ##########

blueprint_route = Blueprint('blueprint_route', __name__)

@blueprint_route.route('/')
def main() :
    return render_template('index.html')

@blueprint_route.route('/about')
def about() :
    return render_template('about.html')

@blueprint_route.route('/sign_in')
def sign_in() :
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success
    if not authenticate_result :
        return render_template('sign_in.html')

    # Authenticate - Fail
    return render_template('index.html')

@blueprint_route.route('/sign_up')
def sign_up() :
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success
    if not authenticate_result :
        return render_template('sign_up.html')

    # Authenticate - Fail
    return render_template('index.html')

# Post : Post ID
@blueprint_route.route('/post/<int:post_id>')
def post(post_id) :
    connect_db = open_db()

    with connect_db.cursor() as cursor :
        sql = "SELECT * FROM post WHERE post_id = %s"
            
        cursor.execute(sql, ( post_id, ))

        post = cursor.fetchone() # Get Fetch One

        if not post :
            return "No Post"

    return render_template('post.html', post = post)

# Edit Post
@blueprint_route.route('/edit_post_get/<int:post_id>')
def edit_post(post_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_post_account(post_id)

    # Authenticate - Success
    if authenticate_result :
        try :
            connect_db = open_db()
            
            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM post WHERE post_id = %s"
                    
                cursor.execute(sql, ( post_id, ))

                post = cursor.fetchone() # Get Fetch One

            return render_template('edit_post.html', post = post)
    
        except Exception as e :
            return render_template('index.html')

    # Authenticate - Fail
    return render_template('index.html')

# Create Post
@blueprint_route.route('/create_post')
def create_post() :
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success
    if authenticate_result :
        try :
            connect_db = open_db()

            account_id = session['account_id']

            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_id = %s"

                cursor.execute(sql, ( account_id, ))

                account = cursor.fetchone() # Get Fetch One

                if not account :
                    return render_template('index.html') # Not Right Access

            return render_template('create_post.html', account = account)
        
        except Exception as e :
            return render_template('index.html')

    # Authenticate - Fail
    return render_template('index.html')

# Profile : Account ID
@blueprint_route.route('/profile/<int:account_id>')
def profile(account_id) :
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success
    if authenticate_result :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account WHERE account_id = %s"

            cursor.execute(sql, ( account_id, ))

            account = cursor.fetchone() # Get Fetch One

            if not account :
                return "No Account"
            
        return render_template('profile.html', account = account)
    
    else :
        return render_template('index.html')

# Edit Account
@blueprint_route.route('/edit_account_get/<int:account_id>')
def edit_account(account_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_target_account(account_id)

    # Authenticate - Success
    if authenticate_result :
        try :
            session_account_id = session['account_id'] # Get Account ID from Session

            connect_db = open_db()

            # Check #1
            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_id = %s"

                cursor.execute(sql, ( session_account_id, ))

                account = cursor.fetchone() # Get Fetch One

                if not account :
                    return render_template('index.html') # Not Valid Access
            
            # Check #2
            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_id = %s"
                    
                cursor.execute(sql, ( account_id, ))

                account = cursor.fetchone() # Get Fetch One

                if not account :
                    return render_template('index.html') # Not Valid Access
                
                if session_account_id != account['account_id'] :
                    return render_template('index.html') # Not Valid Access

            return render_template('edit_account.html', account = account)
        
        except Exception as e :
            return render_template('index.html')
    
    # Authenticate - Fasil
    else :
        return render_template('index.html')
