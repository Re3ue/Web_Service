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
                           
                    account_name VARCHAR(20) NOT NULL,
                    account_password VARCHAR(20) NOT NULL,
                    account_create_date VARCHAR(20) NOT NULL,
                    account_edit_date VARCHAR(20) NOT NULL
                )
            """)

            # Check - Empty : Account Table
            cursor.execute("SELECT COUNT(*) AS account_count FROM account")

            account_count = cursor.fetchone()['account_count']

            # Create Admin Account : "admin_1" ~ "admin_9"
            if (account_count == 0) :
                for i in range(1, 10, 1):
                    sql = "INSERT INTO account (account_name, account_password, account_create_date, account_edit_date) VALUES (%s, %s, %s, %s)"
                    
                    cursor.execute(sql, (f"admin_{i}", f"admin_{i}", "", ""))

                print("[ Table : Account ] Not Exist : Admin Accounts => Create : admin_0 ~ admin_9")
            
            else :
                print("[ Table : Account ] Exist : Admin Account => Not Create : Admin Account")

            print("[ OK ] Success to Create DB Table - Account")

            # [ DB Schema ] Post Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post (
                    post_account_id INT NOT NULL,
                    post_account_name VARCHAR(20) NOT NULL,
                           
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