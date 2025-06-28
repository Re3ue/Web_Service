########## ########## ########## ##########

# Import : Internal
import os

# Import : External
import pymysql

########## ########## ########## ##########

# Get DB Information from ".env" File
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_ID = os.getenv('MYSQL_ID')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# Open DB
def open_db() :
    return pymysql.connect(
        host = MYSQL_HOST,
        db = MYSQL_DB,
        user = MYSQL_ID,
        password = MYSQL_PASSWORD,
        cursorclass = pymysql.cursors.DictCursor, # Get Response with Dictionary
        autocommit = True, # Commit
    )

# Close DB
def close_db() :
    print()

# Initialize DB
def initialize_db() :
    connect_db = open_db()

    try :
        with connect_db.cursor() as cursor :
            # [ DB Schema ] Account Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS account (
                    account_id INT AUTO_INCREMENT PRIMARY KEY,
                    account_name TEXT NOT NULL,
                    account_pw TEXT NOT NULL,
                    account_create_date VARCHAR(20) NOT NULL,
                    account_edit_date VARCHAR(20) NOT NULL
                )
            """)

            print("[ OK ] Success to Create DB Table - Account")

            # [ DB Schema ] Post Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post (
                    post_id INT AUTO_INCREMENT PRIMARY KEY,
                    post_title VARCHAR(255) NOT NULL,
                    post_content TEXT NOT NULL,
                    post_create_date VARCHAR(20) NOT NULL,
                    post_edit_date VARCHAR(20) NOT NULL,
                    post_upvote INT DEFAULT 0
                )
            """)

            print("[ OK ] Success to Create DB Table - Post")
    
    except Exception as e :
        print(f"[ ERROR ] Fail to Create DB Table - Post : {e}")
    
    finally :
        connect_db.close()