########## ########## ########## ##########

# Import : External
from flask import Blueprint, request, jsonify

# Import : File
from .db import open_db

########## ########## ########## ##########

blueprint_api = Blueprint('blueprint_api', __name__)

# API : Create Post
@blueprint_api.route('/api/create_post', methods = ['POST'])
def create_post() :
    post_data = request.get_json() # Get Post Data

    post_title = post_data.get('title')
    post_content = post_data.get('content')
    post_date = post_data.get('date')

    # Check : Require
    if (not post_title) or (not post_content) or (not post_data) :
        return jsonify({"error" : "Miss Require Fields"})
    
    # SQL Query : Insert to Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = "INSERT INTO post (post_title, post_content, post_date) VALUES (%s, %s, %s)"
            
            cursor.execute(sql, ( post_title, post_content, post_date ))

            connect_db.commit()

            post_id = cursor.lastrowid # Get Post ID : Last Post
        
        return jsonify({"result" : 1, "post_id" : post_id})

    except Exception as e :
        print(f"[ ERROR ] Fail to Create Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Create Post"})
    
    finally :
        connect_db.close()



# API : Get All Post
@blueprint_api.route('/api/get_all_post', methods = ['GET'])
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

# API : Get A Post
@blueprint_api.route('/api/get_a_post', methods = ['GET'])
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

# API : Search Post
@blueprint_api.route('/api/search_post', methods = ['GET'])
def search_post() :
    search_input = request.args.get("search_input")

    if not search_input :
        return jsonify({"result" : 0, "error" : "Miss Search Input"})
    
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = """
                SELECT * FROM post
                WHERE post_title LIKE %s OR post_content LIKE %s
                ORDER BY post_id DESC
            """
            
            like_search_input = f"%{search_input}%"

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

# API : Edit Post
@blueprint_api.route('/api/edit_post_post/<int:post_id>', methods = ['POST'])
def edit_post_post(post_id) :
    post_data = request.get_json() # Get Post Data

    post_title = post_data.get('title')
    post_content = post_data.get('content')
    post_date = post_data.get('date')

    # Check : Require
    if (not post_title) or (not post_content) or (not post_data) :
        return jsonify({"error" : "Miss Require Fields"})
    
    # SQL Query : Insert to Post Table
    try :
        connect_db = open_db()

        with connect_db.cursor() as cursor :
            sql = """
                UPDATE post
                SET post_title = %s,
                    post_content = %s,
                    post_date = %s
                WHERE post_id = %s
            """
            
            cursor.execute(sql, ( post_title, post_content, post_date, post_id ))

            connect_db.commit()
        
        return jsonify({"result" : 1, "post_id" : post_id})

    except Exception as e :
        print(f"[ ERROR ] Fail to Edit Post : {e}")

        return jsonify({"result" : 0, "error" : "Fail to Edit Post"})
    
    finally :
        connect_db.close()

# API : Delete Post
@blueprint_api.route('/api/delete_post/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id) :
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