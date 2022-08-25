#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource, reqparse
import os, json, tempfile
import logging

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
app = Flask(__name__)


@app.route('/api/v1/storage/json/all', methods=['GET'])
def get_all_items():
	if os.path.isfile(storage_path):
		with open(str(storage_path), "r") as f:	
			items = json.load(f)
			if not items:
				return jsonify({'error': 'no existing data in storage'})
			return jsonify(items)	
	else:
		return jsonify({'error': 'no file created'})	



@app.route('/api/v1/storage/json/read', methods=['GET'])
def query_items():
	key = request.args.get('key')
	with open(storage_path, 'r+') as f:
		try:
			items = json.load(f)
		except:
			items = {}
			json.dump(items, f)	
		for k, val in items.items():
			if k == key:
				return jsonify({k: val})
		return jsonify({'error': 'data not found'})	



@app.route('/api/v1/storage/json/write', methods=['POST'])
def create_new_item():
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		data = json.loads(request.data)
		if os.path.isfile(storage_path):
			with open(str(storage_path), 'r') as f:
				file_data = json.load(f)
				for k, val in data.items():
					if k in file_data.keys():
						file_data[k] = file_data[k] + [val]
						res = {k: file_data[k]}
					else:
						file_data.update({k: [val]})
						res = {k: [val]}

			with open(str(storage_path), 'w') as f:
				f.write(json.dumps(file_data))

		else:
			with open(str(storage_path), "w") as f:
				for k, val in data.items:
					if val != "":
						json.dump({k: val}, f)
					else:
						return jsonify({"error": "value is empty"})	

		return jsonify(res), 201
	else:
		return jsonify({"error":'Content-Type not supported!'})



if __name__ == '__main__':
    app.run(debug=True)