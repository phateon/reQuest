'''
Created on Mar 10, 2014

@author: Markus
'''
from request.config import db

if __name__ == '__main__':

	data = db.tasks.find()

	myFile = open('eval.csv', 'w')
	myFile.write('response,estimated_quality'+'\n')
	for d in data:
		hits = d['hits']
		for h in hits:
			if hits[h]['solved']:
				myFile.write(str(hits[h]['response']).rstrip('\r\n')+','+str(hits[h]['quality'])+'\n')
		
	myFile.close()
