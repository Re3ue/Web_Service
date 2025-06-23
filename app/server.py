########## ########## ########## ##########

# Import : Internal
import os
import time

# Import : External
from flask import Flask
import pymysql

# Import : File
from server.route import blueprint_route

########## ########## ########## ##########

# Create Flask Instance
server = Flask(__name__)

# Route ( Blueprint )
server.register_blueprint(blueprint_route)

# Run Flask Server
if __name__ == '__main__' :
    server.run(debug = True)
