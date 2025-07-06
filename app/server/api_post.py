########## ########## ########## ##########

# Import : Internal
from datetime import datetime
import os

# Import : External
from flask import Blueprint, request, jsonify, session
import bcrypt

# Import : File
from .db import open_db
from .authenticate import authenticate_sign_in_sign_out, authenticate_session_account_target_account, authenticate_session_account_post_account

########## ########## ########## ##########

blueprint_api_post = Blueprint('blueprint_api_post', __name__)

########## ########## ########## ##########
# API - Post : Create / Edit / Delete
########## ########## ########## ##########

# API - Post : Create Post
@blueprint_api_post.route('/api/create_post', methods = ['POST'])
def create_post() :
    authenticate_result = False

    authenticate_result = authenticate_sign_in_sign_out()

    # Authenticate - Success ( State : Sign In ) => Can Access
    if authenticate_result :
        post_account = None

        account_id = session['account_id']

        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_id = %s"
                
                cursor.execute(sql, ( account_id, ))

                post_account = cursor.fetchone() # Get A Post Account
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Get Post Account : {e}")

            return jsonify({"result" : 0, "error" : "Fail to Get Post Account"})

        finally :
            connect_db.close()

        post_account_id = post_account['account_id']
        post_account_display_name = post_account['account_display_name']

        post_title = request.form.get('title')
        post_content = request.form.get('content')

        # Get - with "request.files.get()" : O / with "account_form_data.get()" : X
        post_file = request.files.get('file') or None
        post_password_raw = request.form.get('password') or None

        # Check : Require
        if (not post_title) or (not post_content) :
            return jsonify({"result" : 0, "error" : "Miss Require Fields"})
        
        post_create_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        post_edit_date = ""
        
        post_file_file_path = ""

        # Save : Post File to Server
        if (post_file) and (post_file.filename != "") :
            post_file_file_name = f"post_{post_account_id}_{post_create_date}_{post_file.filename}"

            # print(f"[ DEBUG ] \"post_file_file_name\" : {post_file_file_name}", flush = True)

            post_file_directory_path = os.path.join("static", "image/image_post") # Get - Path : Directory

            os.makedirs(post_file_directory_path, exist_ok = True) # Check

            save_post_file_file_path = os.path.join(post_file_directory_path, post_file_file_name)
            
            post_file.save(save_post_file_file_path) # Save Post File to Server ( "save_post_file_file_path" )

            post_file_file_path = f"/static/image/image_post/{post_file_file_name}"

            print(f"[ DEBUG ] \"post_file_file_path\" : {post_file_file_path}", flush = True)

        post_password_hash = ""

        # Hash : Post Password
        if post_password_raw :
            post_password_hash = bcrypt.hashpw(post_password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # SQL Query : Insert to Post Table
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = """
                    INSERT INTO post (
                        post_account_id,
                        post_account_display_name,

                        post_title,
                        post_content,

                        post_file,
                        post_password,

                        post_create_date,
                        post_edit_date
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(sql, (
                    post_account_id,
                    post_account_display_name,

                    post_title,
                    post_content,

                    post_file_file_path if post_file_file_path else None,
                    post_password_hash if post_password_hash else None,
                    
                    post_create_date,
                    post_edit_date
                ))                

                connect_db.commit()

                post_id = cursor.lastrowid # Get Post ID : Last Post
            
            return jsonify({"result" : 1, "post_id" : post_id})

        except Exception as e :
            print(f"[ ERROR ] Fail to Create Post : {e}")

            return jsonify({"result" : 0, "error" : "Fail to Create Post"})
        
        finally :
            connect_db.close()

    # Authenticate - Fail ( Sate : Sign Out ) => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

# API - Post : Edit Post
@blueprint_api_post.route('/api/edit_post_post/<int:post_id>', methods = ['POST'])
def edit_post_post(post_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_post_account(post_id)

    # Authenticate - Success => Can Access
    if authenticate_result :
        post_account = None

        account_id = session['account_id']

        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = "SELECT * FROM account WHERE account_id = %s"
                
                cursor.execute(sql, ( account_id, ))

                post_account = cursor.fetchone() # Get A Post Account
        
        except Exception as e :
            print(f"[ ERROR ] Fail to Get Post Account : {e}")

            return jsonify({"result" : 0, "error" : "Fail to Get Post Account"})

        finally :
            connect_db.close()

        post_account_id = post_account['account_id']
        post_account_display_name = post_account['account_display_name'] # Not Use

        post_title = request.form.get('title')
        post_content = request.form.get('content')

         # Get - with "request.files.get()" : O / with "account_form_data.get()" : X
        post_file = request.files.get('file') or None
        post_password_raw = request.form.get('password') or None

        # Check : Require
        if (not post_title) or (not post_content) :
            return jsonify({"result" : 0, "error" : "Miss Require Fields"})
        
        post_edit_date = datetime.now().strftime("%Y%m%d_%H%M%S")

        post_file_file_path = ""

        # Save : Post File to Server
        if (post_file) and (post_file.filename != "") :
            post_file_file_name = f"post_{post_account_id}_{post_edit_date}_{post_file.filename}"

            post_file_directory_path = os.path.join("static", "image/image_post") # Get - Path : Directory

            os.makedirs(post_file_directory_path, exist_ok = True) # Check

            save_post_file_file_path = os.path.join(post_file_directory_path, post_file_file_name)
            
            post_file.save(save_post_file_file_path) # Save Post File to Server ( "save_post_file_file_path" )

            post_file_file_path = f"/static/image/image_post/{post_file_file_name}"
        
        post_password_hash = ""

        # Hash : Post Password
        if post_password_raw :
            post_password_hash = bcrypt.hashpw(post_password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')        
        
        # SQL Query : Insert to Post Table
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = """
                    UPDATE post
                    SET post_title = %s,
                        post_content = %s,

                        post_file = %s,
                        post_password = %s,

                        post_edit_date = %s
                    WHERE post_id = %s
                """

                cursor.execute(sql, (
                    post_title,
                    post_content,

                    post_file_file_path if post_file_file_path else None,
                    post_password_hash if post_password_hash else None,
                    
                    post_edit_date,

                    post_id
                ))  
            
                connect_db.commit()
            
            return jsonify({"result" : 1, "post_id" : post_id})

        except Exception as e :
            print(f"[ ERROR ] Fail to Edit Post : {e}")

            return jsonify({"result" : 0, "error" : "Fail to Edit Post"})
        
        finally :
            connect_db.close()
    
    # Authenticate - Fail => Can Not Access
    return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

# API - Post : Delete Post
@blueprint_api_post.route('/api/delete_post/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id) :
    authenticate_result = False

    authenticate_result = authenticate_session_account_post_account(post_id)

    # Authenticate - Success => Can Access
    if authenticate_result :
        try :
            connect_db = open_db()

            with connect_db.cursor() as cursor :
                sql = "DELETE FROM post WHERE post_id = %s"
                
                cursor.execute(sql, ( post_id ))

                connect_db.commit()

                return jsonify({"result" : 1})

        except Exception as e :
            print(f"[ ERROR ] Fail to Delete Post : {e}")

            return jsonify({"result" : 0, "error" : "Fail to Delete Post"})
        
        finally :
            connect_db.close()

    # Authenticate - Fail => Can Not Access
    else :
        return jsonify({"result" : 0, "error" : "Fail to Authenticate"})

########## ########## ########## ##########
# API - Post : Get All / Get A / Search
########## ########## ########## ##########

# API - Post : Get All Post
@blueprint_api_post.route('/api/get_all_post', methods = ['GET'])
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

# API - Post : Get A Post
@blueprint_api_post.route('/api/get_a_post', methods = ['GET'])
def get_a_post(post_id) :
    # SQL Query : Get A Post from Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "SELECT * FROM post WHERE post_id = %s"
            
            cursor.execute(sql, ( post_id, ))

            a_post = cursor.fetchone() # Get A Post

            if not a_post :
                return jsonify({"result" : 0, "error" : "Not Exist : A Post"})
        
        return jsonify({"result" : 1, "a_post" : a_post})

    except Exception as e :
        print(f"[ ERROR ] Fail to Get A Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Get A Post"})
    
    finally :
        connect_db.close()

# API - Post : Get A Secret Post ( Post Password )
@blueprint_api_post.route('/api/post_password/<int:post_id>', methods = ['POST'])
def get_a_secret_post(post_id) :
    data = request.get_json()

    input_password = data.get('postPassword')

    print(f"[ DEBUG ] Input Password : {input_password}", flush = True)

    if not input_password :
        return jsonify({"result": 0, "error": "Miss Require Fields"})
    
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            # SQL Query
            sql = "SELECT post_password FROM post WHERE post_id = %s"

            cursor.execute(sql, (post_id,))

            post = cursor.fetchone() # Get A Post

            # Case : Not Exist
            if not post :
                return jsonify({"result": 0, "error": "Not Exist"})

            post_password_hash = post.get('post_password')

            # Check
            check_result = bcrypt.checkpw(input_password.encode("utf-8"), post_password_hash.encode("utf-8"))
            
            # Check - Fail
            if not check_result :
                return jsonify({"result": 0, "error": "Fail to Check - Post Password"})

            # Create Session
            session[f"secret_post_{post_id}"] = True

            return jsonify({"result": 1, "post_id": post_id})

    except Exception as e :
        print(f"[ ERROR ] Fail to Check - Post Password : {e}")

        return jsonify({"result": 0, "error": "Fail to Check - Post Password"})

    finally :
        connect_db.close()

# API - Post : Search Post
@blueprint_api_post.route('/api/search_post', methods = ['GET'])
def search_post() :
    search_input = request.args.get("search_input")
    search_option = request.args.get("search_option")

    if not search_input :
        return jsonify({"result" : 0, "error" : "Miss Search Input"}) 
       
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            like_search_input = f"%{search_input}%"

            # Search By Title
            if search_option == "search_title" :
                sql = """
                    SELECT * FROM post
                    WHERE post_title LIKE %s
                    ORDER BY post_id DESC
                """

                cursor.execute(sql, ( like_search_input ))
    
            # Search By Content
            elif search_option == "search_content" :
                sql = """
                    SELECT * FROM post
                    WHERE post_content LIKE %s
                    ORDER BY post_id DESC
                """

                cursor.execute(sql, ( like_search_input ))
            
            # Search By Account => To Do

            # Search By All
            else :
                sql = """
                    SELECT * FROM post
                    WHERE post_title LIKE %s OR post_content LIKE %s
                    ORDER BY post_id DESC
                """
        
                cursor.execute(sql, ( like_search_input, like_search_input ))

            search_post = cursor.fetchall()

            if not search_post :
                return jsonify({"result" : 0, "error" : "Not Exist : Search Post"})

            return jsonify({"result" : 1, "search_post" : search_post})

    except Exception as e :
        print(f"[ ERROR ] Fail to Search Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Search Post"})
    
    finally :
        connect_db.close()
