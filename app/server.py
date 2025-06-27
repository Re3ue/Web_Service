########## ########## ########## ##########

# Import : Internal
import os
import time

# Import : External
from flask import Flask
import pymysql

# Import : File
from server.db import initialize_db
from server.route import blueprint_route
from server.api import blueprint_api

# Import : File - Admin
from server.admin import blueprint_admin

########## ########## ########## ##########

# Create Flask Instance
server = Flask(__name__)

# Route ( Blueprint )
server.register_blueprint(blueprint_route)
server.register_blueprint(blueprint_api)

# Route - Admin ( Blueprint )
server.register_blueprint(blueprint_admin)

# Run Flask Server
if __name__ == '__main__' :
    try_count = 0

    while try_count < 10 :
        try : 
            with server.app_context() :
                # Initialize DB
                initialize_db()
            
            print("[ OK ] Success to Connect DB")

            break
        
        except Exception as e :
            try_count += 1

            print(f"[ ERROR ] Fail to Connect DB ( Try Count : {try_count}) : {e}")

            time.sleep(2)

    else :
        print("[ ERROR ] Fail to Connect DB")

        exit(1)

    server.run(host = '0.0.0.0', debug = True)
