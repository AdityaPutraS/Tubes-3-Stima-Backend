from flask import *
from app import app

@app.route('/')
def index():
	return Response(status=200)

@app.route('/test')
def test():
	return jsonify({'Test':2}), 200
	
