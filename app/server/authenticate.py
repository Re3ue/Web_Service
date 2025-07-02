########## ########## ########## ##########

# Import : External
from flask import session

# Import : File
from .db import open_db

########## ########## ########## ##########

# [ Authenticate ] Sign In / Sign Out
def authenticate_sign_in_sign_out() :
    try :
        session_account_id = session['account_id'] # Get Account ID from Session

        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account WHERE account_id = %s"

            cursor.execute(sql, ( session_account_id, ))

            account = cursor.fetchone() # Get Fetch One

            if account :
                return True # Sign In

            else :
                return False # Sign Out
    
    except Exception as e : 
        return False

########## ########## ########## ########## 
# Account
########## ########## ########## ########## 

# [ Authenticate ] Account : ( Session Account == Target Account ) ? ( Session Account != Target Account )
def authenticate_session_account_target_account(account_id) :
    try :
        session_account_id = session['account_id'] # Get Account ID from Session

        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account WHERE account_id = %s"

            cursor.execute(sql, ( session_account_id, ))

            target_account = cursor.fetchone() # Get Fetch One

            if not target_account :
                return False
            
            target_account_id = target_account['account_id']
            
            if (session_account_id == target_account_id) :
                return True # Session Account == Target Account
            
            return False # Session Account != Target Account
    
    except Exception as e : 
        return False

########## ########## ########## ########## 
# Post
########## ########## ########## ########## 

# [ Authenticate ] Post : ( Session Account == Post Account ) ? ( Session Account != Post Account )
def authenticate_session_account_post_account(post_id) :
    try :
        session_account_id = session['account_id'] # Get Account ID from Session
        
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM post WHERE post_id = %s"

            cursor.execute(sql, ( post_id, ))

            post = cursor.fetchone() # Get Fetch One

            if not post :
                return False

            if ( session_account_id == post['post_account_id'] ) :
                return True # Session Account == Post Account
            
            return False # Session Account != Post Account
    
    except Exception as e : 
        return False
