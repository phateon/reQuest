'''
Created on 29.08.2013

@author: Phateon
'''
from bson.objectid import ObjectId
from flask import json
from flask.blueprints import Blueprint
from flask.globals import request
from flask.templating import render_template
from HTMLParser import HTMLParser
from request.config import db

qaBlue = Blueprint('index', __name__)

##################################################
@qaBlue.route("/<int:task_id>")
def qa_request(task_id=None):
	
	if task_id is None:
		return render_template('qa.html', request_obj=None)

	task = db.tasks.find_one({'task_id': int(task_id)})
	
	if task is None:
		return render_template('qa.html', request_obj=None)

	html_parser = HTMLParser()
	hits = task['hits']	
	requests = []
	for hit_id in hits.keys():
		hit = db.hits.find_one(ObjectId(hit_id))
		unescaped = html_parser.unescape(hit['html'])
		data = {'fragment': unescaped,
				'index': hit_id,
				'solved': hits[hit_id]['solved'],
				'quality': hits[hit_id]['quality'],
				'response': hits[hit_id]['response'],
				'task_id': task_id}
		requests.append(data)
	
	request_obj = {	'finished': task['finished'],
					'reply':task['reply'] if task['finished'] else '',
					'requests': requests}
	
	return render_template('qa.html', request_obj = request_obj)


##################################################
@qaBlue.route('/response', methods=['POST', 'GET'])
def qa_response():
	jsn = request.data
	data = json.loads(jsn)

	task = db.tasks.find_one({'task_id': int(data['task_id'])})
	
	if task is None:
		return {'error': 'Task not in database.'}
	
	q, feedback = quality(data['response'])
	hit = task['hits'][str(data['index'])]
	hit['quality'] = q
	hit['feedback'] = feedback
	hit['response'] = data['response']
	hit['solved'] = True
	hit['index'] = data['index']
	
	finished = True
	for h in task['hits']:
		if not task['hits'][h]['solved']:
			finished = False
	
	if finished:
		hit['finished'] = finished
		hit['reply'] = task['reply']
		
	task['finished'] = finished
	
	db.tasks.save(task)
	result = json.dumps(hit)
	
	return result


##################################################
# estimating response quality
##################################################
def quality(response):
	#TODO implement your quality metric here
	#TODO provide feedback as required

	q = 1.0 #Quality ranging from 0.0-1.0

	#possible feedback to your contributors depending on your quality metric
	feedback = 'Your answers is fine.' if q == 1.0 else 'Please make sure that you write a valid question that is related to the news article!'

	return q, feedback