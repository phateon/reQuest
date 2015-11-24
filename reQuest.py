'''
Created on 20.08.2013
@author: Phateon
'''

from flask import Flask
from request.view import qaBlue

app = Flask(__name__)
app.secret_key = 'your super secret app key'

app.register_blueprint(qaBlue)

if __name__ == "__main__":
	app.run()
