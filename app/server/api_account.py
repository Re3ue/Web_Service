########## ########## ########## ##########

# Import : Internal
from datetime import datetime
import os

# Import : External
from flask import Blueprint, request, jsonify, session
from .authenticate import authenticate_sign_in_sign_out, authenticate_session_account_target_account, authenticate_session_account_post_account
import bcrypt

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
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success ( State : Sign Out ) => Can Access
    if not authenticate_result :
        sign_in_data = request.get_json() # Get Sign In Data

        input_account_name = sign_in_data.get('name')
        input_account_password_raw = sign_in_data.get('password')

        # Check : Require
        if (not input_account_name) or (not input_account_password_raw) :
            return jsonify({"result" : 0, "error" : "Miss Require Fields"})
        
        # SQL Query
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor:
                sql = "SELECT account_id, account_password FROM account WHERE account_name = %s"
                
                cursor.execute(sql, ( input_account_name, ))

                account = cursor.fetchone() # Get Account

                if not account :
                    return jsonify({"result" : 0, "error" : "Not Exist : Account"})
                
                account_password = account['account_password'] # Get Password ( Hash )

                # Check - Success : Account - Password
                if bcrypt.checkpw(input_account_password_raw.encode('utf-8'), account_password.encode('utf-8')) :
                    account_id = account['account_id']

                    session['account_id'] = account_id # Create Session - "account_id"
                
                # Check - Fail : Account - Password
                else :
                    return jsonify({"result" : 0, "error" : "Fail to Sign In - Password"})

            return jsonify({"result" : 1, "account_id" : account_id})

        except Exception as e :
            print(f"[ ERROR ] Fail to Sign In : {e}")

            return jsonify({"result" : 0, "error" : f"Fail to Sign In - {e}"})

        finally :
            connect_db.close()
    
    # Authenticate - Fail ( State : Sign In ) => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

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
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success ( State : Sign Out ) => Can Access
    if not authenticate_result :
        account_data = request.get_json() # Get Account Data

        account_name = account_data.get('name')
        account_display_name = account_data.get('displayName')
        account_password_raw = account_data.get('password')
        
        account_country = account_data.get('country')
        account_birth = account_data.get('birth')

        account_image = "/static/image/image_account/account_default.avif" 

        account_create_date = datetime.now().strftime("%Y%m%d_%H%M")
        account_edit_date = ""

        # Check : Require
        if (not account_name) or (not account_display_name) or (not account_password_raw) :
            return jsonify({"result" : 0, "error" : "Miss Require Fields"})
        
        # Hash ( Password )
        account_password = bcrypt.hashpw(account_password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # SQL Query : Insert to Account Table
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                # Check - Exist : "account_name" / "account_display_name"
                sql = "SELECT * FROM account WHERE account_name = %s OR account_display_name = %s"

                cursor.execute(sql, ( account_name, account_display_name ))

                exist_flag = True

                exist_flag = cursor.fetchone()

                if exist_flag :
                    return jsonify({"result": 0, "error": "Fail to Create Account - Exist \"account_name\" OR \"account_display_name\""})
                
                sql = """
                INSERT INTO account (
                    account_name, account_display_name, account_password,
                    account_country, account_birth,
                    account_image,
                    account_create_date, account_edit_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql, ( account_name, account_display_name, account_password, account_country, account_birth, account_image, account_create_date, account_edit_date ))

                connect_db.commit()

                account_id = cursor.lastrowid # Get Account ID : Last Account

                session['account_id'] = account_id # Session : Save - Account ID

            return jsonify({"result" : 1, "account_id" : account_id})
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Create Account : {e}")

            return jsonify({"result" : 0, "error" : f"Fail to Create Account - {e}"})
        
        finally :
            connect_db.close()

    # Authenticate - Fail ( State : Sign In ) => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})
    
# API - Account : Edit Account
@blueprint_api_account.route('/api/edit_account_post/<int:account_id>', methods = ['POST'])
def edit_account(account_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_target_account(account_id)

    # Authenticate - Success => Can Access
    if authenticate_result :
        account_form_data = request.form # Get Account Form Data

        account_name = account_form_data.get('name')
        account_display_name = account_form_data.get('displayName')
        account_password_raw = account_form_data.get('password')

        account_birth = account_form_data.get('birth') or None
        account_country = account_form_data.get('country') or None

        account_image = request.files.get('image') or None # Get - with "request.files.get()" : O / with "account_form_data.get()" : X

        # print(f"[ DEBUG ] \"account_image\" : {account_image}", flush = True)

        # Check : Require
        if (not account_name) or (not account_display_name) or (not account_password_raw) :
            return jsonify({"result" : 0, "error" : "Miss Require Fields"})
        
        # Hash ( Password )
        account_password = bcrypt.hashpw(account_password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Check - Exist : "account_name" / "account_display_name"
        try : 
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_name = %s OR account_display_name = %s"

                cursor.execute(sql, ( account_name, account_display_name ))

                exist_flag = True

                exist_flag = cursor.fetchone()

                if exist_flag :
                    return jsonify({"result": 0, "error": "Fail to Create Account - Exist \"account_name\" OR \"account_display_name\""})
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Edit Account : {e}")

            return jsonify({"result" : 0, "error" : f"Fail to Edit Account - {e}"})
        
        finally :
            connect_db.close()

        account_image_file_path = ""

        # Save : Image File to Server
        if (account_image) and (account_image.filename != "") :
            account_image_file_name = f"account_{account_id}_{account_image.filename}"

            # print(f"[ DEBUG ] \"account_image_file_name\" : {account_image_file_name}", flush = True)

            account_image_directory_path = os.path.join("static", "image/image_account") # Get - Path : Directory

            os.makedirs(account_image_directory_path, exist_ok = True) # Check

            save_account_image_file_path = os.path.join(account_image_directory_path, account_image_file_name)
            
            account_image.save(save_account_image_file_path) # Save Image File to Server ( "save_account_image_file_path" )

            account_image_file_path = f"/static/image/image_account/{account_image_file_name}"

            # print(f"[ DEBUG ] \"account_image_file_path\" : {account_image_file_path}", flush = True)

        # Save : Edit Date to DB
        account_edit_date = datetime.now().strftime("%Y%m%d_%H%M")

        # SQL Query : Insert to Account Table
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                # Exist : Edit - Image File
                if account_image_file_path :
                    sql = """
                        UPDATE account
                        SET account_name = %s,
                            account_display_name = %s,
                            account_password = %s,
                            account_birth = %s,
                            account_country = %s,
                            account_image = %s,
                            account_edit_date = %s
                        WHERE account_id = %s
                    """
                
                    cursor.execute(sql, ( account_name, account_display_name, account_password, account_birth, account_country, account_image_file_path, account_edit_date, account_id ))
                
                # Not Exist : Edit - Image File
                else :
                    sql = """
                        UPDATE account
                        SET account_name = %s,
                            account_display_name = %s,
                            account_password = %s,
                            account_birth = %s,
                            account_country = %s,
                            account_edit_date = %s
                        WHERE account_id = %s
                    """
                
                    cursor.execute(sql, ( account_name, account_display_name, account_password, account_birth, account_country, account_edit_date, account_id ))

                connect_db.commit()

            return jsonify({"result" : 1, "account_id" : account_id})
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Edit Account : {e}")

            return jsonify({"result" : 0, "error" : f"Fail to Edit Account - {e}"})
        
        finally :
            connect_db.close()
    
    # Authenticate - Fail => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

# API - Account : Delete Account
@blueprint_api_account.route('/api/delete_account/<int:account_id>', methods = ['DELETE'])
def delete_account(account_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_target_account(account_id)

    # Authenticate - Success => Can Access
    if authenticate_result :
        try : 
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = "DELETE FROM account WHERE account_id = %s"

                cursor.execute(sql, ( account_id ))

                connect_db.commit()

                session.pop("account_id", None) # Delete Session - "account_id"

                return jsonify({"result" : 1})

        except Exception as e :
            print(f"[ ERROR ] Fail to Delete Account : {e}")

            return jsonify({"result" : 0, "error" : f"Fail to Delete Account - {e}"})
    
        finally :
            connect_db.close()
    
    # Authenticate - Fail => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

########## ########## ########## ##########
# API - Account : Get All / Get A / Search
########## ########## ########## ##########

# API - Account : Get All Account

# API - Account : Get A Account

# API - Account : Search Account
