########## ########## ########## ##########

# Import : Internal
from datetime import datetime
import os

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
    account_display_name = account_data.get('displayName')
    
    account_country = account_data.get('country')
    account_birth = account_data.get('birth')

    account_image = "/static/image/image_account/account_default.avif" 

    account_create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    account_edit_date = account_create_date

    # Check : Require
    if (not account_name) or (not account_password) or (not account_display_name) :
        return jsonify({"error" : "Miss Require Fields"})
    
    # SQL Query : Insert to Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = """
            INSERT INTO account (
                account_name, account_password, account_display_name,
                account_country, account_birth,
                account_image,
                account_create_date, account_edit_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, ( account_name, account_password, account_display_name, account_country, account_birth, account_image, account_create_date, account_edit_date ))

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
@blueprint_api_account.route('/api/edit_account_post/<int:account_id>', methods = ['POST'])
def edit_account(account_id) :
    account_form_data = request.form # Get Account Form Data

    account_name = account_form_data.get('name')
    account_password = account_form_data.get('password')
    account_display_name = account_form_data.get('displayName')
    account_birth = account_form_data.get('birth') or None
    account_country = account_form_data.get('country') or None
    account_image = request.files.get('image') or None # Get - with "request.files.get()" : O / with "account_form_data.get()" : X

    print(f"[ DEBUG ] \"account_image\" : {account_image}", flush = True)

    # Check : Require
    if (not account_name) or (not account_password) or (not account_display_name) :
        return jsonify({"error" : "Miss Require Fields"})

    account_image_file_path = ""

    # Save : Image File to Server
    if (account_image) and (account_image.filename != "") :
        filename = f"account_{account_id}_{account_image.filename}"

        print(f"[ DEBUG ] \"filename\" : {filename}", flush = True)

        image_account_path = os.path.join("static", "image/image_account")

        os.makedirs(image_account_path, exist_ok = True) # Check - Path : Directory

        image_file_save_path = os.path.join(image_account_path, filename)
        
        account_image.save(image_file_save_path)

        account_image_file_path = f"/static/image/image_account/{filename}"

        print(f"[ DEBUG ] \"account_image_file_path\" : {account_image_file_path}", flush = True)

    # Save : Edit Date to DB
    account_edit_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # SQL Query : Insert to Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            # Exist : Image File
            if account_image_file_path :
                sql = """
                    UPDATE account
                    SET account_name = %s,
                        account_password = %s,
                        account_display_name = %s,
                        account_birth = %s,
                        account_country = %s,
                        account_image = %s,
                        account_edit_date = %s
                    WHERE account_id = %s
                """
            
                cursor.execute(sql, ( account_name, account_password, account_display_name, account_birth, account_country, account_image_file_path, account_edit_date, account_id ))
            # Not Exist : Image File
            else :
                sql = """
                    UPDATE account
                    SET account_name = %s,
                        account_password = %s,
                        account_display_name = %s,
                        account_birth = %s,
                        account_country = %s,
                        account_edit_date = %s
                    WHERE account_id = %s
                """
            
                cursor.execute(sql, ( account_name, account_password, account_display_name, account_birth, account_country, account_edit_date, account_id ))

            connect_db.commit()

        return jsonify({"result" : 1, "account_id" : account_id})
    
    except Exception as e :
        print(f"[ ERROR ] Fail to Edit Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Edit Account"})
    
    finally :
        connect_db.close()

# API - Account : Delete Account
@blueprint_api_account.route('/api/delete_account/<int:account_id>', methods = ['DELETE'])
def delete_account(account_id) :
    try :
        session_account_id = session['account_id'] # Get Account ID from Session

        connect_db = open_db()

        # Check #1
        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account WHERE account_id = %s"

            cursor.execute(sql, ( session_account_id, ))

            account = cursor.fetchone() # Get Fetch One

            if not account :
                return jsonify({"result" : 0, "error" : "Fail to Delete Account"}) # Not Valid Access

        # Check #2
        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account WHERE account_id = %s"
                
            cursor.execute(sql, ( account_id, ))

            account = cursor.fetchone() # Get Fetch One

            if not account :
                return jsonify({"result" : 0, "error" : "Fail to Delete Account"}) # Not Valid Access
            
            if session_account_id != account['account_id'] :
                return jsonify({"result" : 0, "error" : "Fail to Delete Account"}) # Not Valid Access

        # Do
        with connect_db.cursor() as cursor :
            sql = "DELETE FROM account WHERE account_id = %s"

            cursor.execute(sql, ( account_id ))

            connect_db.commit()

            session.pop("account_id", None) # Delete Session - "account_id"

            return jsonify({"result" : 1})

    except Exception as e :
        print(f"[ ERROR ] Fail to Delete Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Delete Account"})
    
    finally :
        connect_db.close()

########## ########## ########## ##########
# API - Account : Get All / Get A / Search
########## ########## ########## ##########

# API - Account : Get All Account

# API - Account : Get A Account

# API - Account : Search Account
