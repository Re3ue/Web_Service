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

        return jsonify({"error" : "Fail to Create Post"})
    
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
                return "Not Exist : All Post"
        
        return jsonify({"result" : 1, "all_post" : all_post})

    except Exception as e :
        print(f"[ ERROR ] Fail to Get All Post : {e}")

        return jsonify({"error" : "Fail to Get All Post"})
    
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
                return "Not Exist : A Post"
        
        return jsonify({"result" : 1, "a_post" : a_post})

    except Exception as e :
        print(f"[ ERROR ] Fail to Get A Post : {e}")

        return jsonify({"error" : "Fail to Get A Post"})
    
    finally :
        connect_db.close()
