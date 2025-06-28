########## ########## ########## ##########

# Import : Internal
from datetime import datetime

# Import : External
from flask import Blueprint, render_template, request, jsonify

# Import : File
from .db import open_db

########## ########## ########## ##########

blueprint_admin = Blueprint('blueprint_admin', __name__)

# Admin - Route
@blueprint_admin.route('/admin')
def admin() :
    return render_template('admin.html')

########## ########## ########## ########## 
## Admin - Account API
########## ########## ########## ########## 

# Admin - Account API : Get All
@blueprint_admin.route('/admin_api/get_all_account', methods = ['GET'])
def get_all_account() :
    # SQL Query : Get All Account from Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM account ORDER BY account_id DESC"
            
            cursor.execute(sql)

            all_account = cursor.fetchall() # Get All Account

            if not all_account :
                return jsonify({"result" : 0, "error" : "Not Exist : All Account"})
        
        return jsonify({"result" : 1, "all_account" : all_account})

    except Exception as e :
        print(f"[ ERROR ] Fail to Get All Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Get All Account"})
    
    finally :
        connect_db.close()

# Admin - Account API : Delete All
@blueprint_admin.route('/admin_api/delete_all_account', methods = ['DELETE'])
def delete_all_account() :
    # SQL Query : Delete All Data from Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "DELETE FROM account"
            
            cursor.execute(sql)

            connect_db.commit()

        return jsonify({"result" : 1})

    except Exception as e :
        print(f"[ ERROR ] Fail to Delete All Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Delete All Account"})
    
    finally :
        connect_db.close()

# Admin - Account API : Delete
@blueprint_admin.route('/admin_api/delete_account/<int:account_id>', methods = ['DELETE'])
def delete_account(account_id) :
    # SQL Query : Delete Account Data from Account Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "DELETE FROM account WHERE account_id = %s"

            cursor.execute(sql, ( account_id, ))

            connect_db.commit()

        return jsonify({"result" : 1})
    
    except Exception as e :
        print(f"[ ERROR ] Fail to Delete Account : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Delete Account"})
    
    finally :
        connect_db.close()

# Admin - Account API : Create
@blueprint_admin.route('/admin_api/create_account_100', methods = ['POST'])
def create_account_100() :
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            for i in range(100) :
                sql = """
                    INSERT INTO account (account_name, account_pw, account_create_date, account_edit_date)
                    VALUES (%s, %s, %s, %s)
                """

                account_name = f"test_{i}"
                account_pw = f"pw_{i}"
                account_create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                account_edit_date = ""

                cursor.execute(sql, ( account_name, account_pw, account_create_date, account_edit_date ))

            connect_db.commit()

        return jsonify({"result" : 1})

    except Exception as e :
        print(f"[ ERROR ] Fail to Create Account 100 : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Create Account 100"})

    finally :
        connect_db.close()

########## ########## ########## ########## 
## Admin - Post API
########## ########## ########## ########## 

# Admin - Post API : Get All
@blueprint_admin.route('/admin_api/get_all_post', methods = ['GET'])
def get_all_post() :
    # SQL Query : Get All Post from Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM post ORDER BY post_id DESC"
            
            cursor.execute(sql)

            all_post = cursor.fetchall() # Get All Post

            if not all_post :
                return jsonify({"result" : 0, "error" : "Not Exist : All Post"})
        
        return jsonify({"result" : 1, "all_post" : all_post})

    except Exception as e :
        print(f"[ ERROR ] Fail to Get All Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Get All Post"})
    
    finally :
        connect_db.close()

# Admin - Post API : Delete All
@blueprint_admin.route('/admin_api/delete_all_post', methods = ['DELETE'])
def delete_all_post() :
    # SQL Query : Delete All Data from Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "DELETE FROM post"
            
            cursor.execute(sql)

            connect_db.commit()

        return jsonify({"result" : 1})

    except Exception as e :
        print(f"[ ERROR ] Fail to Delete All Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Delete All Post"})
    
    finally :
        connect_db.close()

# Admin - Post API : Delete
@blueprint_admin.route('/admin_api/delete_post/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id) :
    # SQL Query : Delete Post Data from Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "DELETE FROM post WHERE post_id = %s"

            cursor.execute(sql, ( post_id, ))

            connect_db.commit()

        return jsonify({"result" : 1})
    
    except Exception as e :
        print(f"[ ERROR ] Fail to Delete Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Delete Post"})
    
    finally :
        connect_db.close()

# Admin - Post API : Create
@blueprint_admin.route('/admin_api/create_post_100', methods = ['POST'])
def create_post_100() :
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            for i in range(100) :
                sql = """
                    INSERT INTO post (post_title, post_content, post_create_date, post_edit_date)
                    VALUES (%s, %s, %s, %s)
                """

                post_title = f"TEST #{i}"
                post_content = f"CONTENT #{i}"
                post_create_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                post_edit_date = ""

                cursor.execute(sql, ( post_title, post_content, post_create_date, post_edit_date ))

            connect_db.commit()

        return jsonify({"result" : 1})

    except Exception as e :
        print(f"[ ERROR ] Fail to Create Post 100 : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Create Post 100"})

    finally :
        connect_db.close()