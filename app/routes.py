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
	#Buat dict nya
	hasil = {}
	for j in jawaban:
		hasil[j[1]] = j[0]
	return jsonify(hasil), 200
	
