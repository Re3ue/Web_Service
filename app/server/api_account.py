########## ########## ########## ##########

# Import : Internal
from datetime import datetime

# Import : External
from flask import Blueprint, request, jsonify, session

# Import : File
from .db import open_db

########## ########## ########## ##########

blueprint_api_account = Blueprint('blueprint_api_account', __name__)

########## ########## ########## ##########
# API - Account : Sign In / Sign Out
########## ########## ########## ##########

# API - Account : Sign In
@blueprint_api_account.route('/api/sign_in', methods = ['POST'])
def sign_in() :
    sign_in_data = request.get_json() # Get Sign In Data

    account_name = sign_in_data.get('name')
    account_password = sign_in_data.get('password')

    # Check : Require
    if (not account_name) or (not account_password) :
        return jsonify({"error" : "Miss Require Fields"})
    
    # SQL Query
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor:
            sql = "SELECT account_id FROM account WHERE account_name = %s AND account_password = %s"
            
            cursor.execute(sql, ( account_name, account_password ))

            account = cursor.fetchone() # Get Account

            if not account :
                return jsonify({"result" : 0, "error" : "Not Exist : Account"})

            account_id = account['account_id']

            session['account_id'] = account_id # Create Session - "account_id"

        return jsonify({"result" : 1, "account_id" : account_id})

    except Exception as e :
        print(f"[ ERROR ] Fail to Sign In : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Sign In"})

    finally :
        connect_db.close()

# API - Account : Sign Out
@blueprint_api_account.route('/api/sign_out', methods = ['POST'])
def sign_out() :
    try :
        session.pop("account_id", None) # Delete Session - "account_id"

        return jsonify({"result" : 1})
    
    except Exception as e :
        return jsonify({"result" : 0, "error" : "Fail to Sign Out"})

########## ########## ########## ##########
# API - Account : Create / Edit / Delete
########## ########## ########## ##########

# API - Account : Create Account
@blueprint_api_account.route('/api/create_account', methods = ['POST'])
def create_account() :
    account_data = request.get_json() # Get Account Data

    account_name = account_data.get('name')
    account_password = account_data.get('password')

    account_create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    account_edit_date = ""

    # Check : Require
    if (not account_name) or (not account_password) :
        return jsonify({"error" : "Miss Require Fields"})
    
    # SQL Query : Insert to Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "INSERT INTO account (account_name, account_password, account_create_date, account_edit_date) VALUES (%s, %s, %s, %s)"

            cursor.execute(sql, ( account_name, account_password, account_create_date, account_edit_date ))

            connect_db.commit()

            account_id = cursor.lastrowid # Get Account ID : Last Account

            session['account_id'] = account_id # Session : Save - Account ID

        return jsonify({"result" : 1, "account_id" : account_id})
    
    except Exception as e :
        print(f"[ ERROR ] Fail to Create Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Create Account"})
    
    finally :
        connect_db.close()
    
# API - Account : Edit Account

# API - Account : Delete Account

########## ########## ########## ##########
# API - Account : Get All / Get A / Search
########## ########## ########## ##########

# API - Account : Get All Account

# API - Account : Get A Account

# API - Account : Search Account
