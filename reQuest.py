'''
Created on 20.08.2013
@author: Phateon
'''

from flask import Flask
from request.view import qaBlue

app = Flask(__name__)
app.secret_key = 'lkshalufr8e4984anlap9e8rr87zfdvys'

app.register_blueprint(qaBlue)

if __name__ == "__main__":
	app.run()
