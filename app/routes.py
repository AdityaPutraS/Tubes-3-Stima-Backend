from flask import *
from app import app
from app.stringMatching import getJawaban

@app.route('/')
def index():
	return Response(status=200)

@app.route('/test')
def test():
	return jsonify({'Test':2}), 200

@app.route('/query/<pertanyaan>', methods=['GET','POST'])
def query(pertanyaan):
	jawaban = getJawaban(pertanyaan)
	return jsonify({'respon' : jawaban}), 200
	
