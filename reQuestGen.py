'''
Created on Mar 10, 2014

@author: Markus
'''
from request.config import db
from request.generator import write_csv, hits_from_csv

if __name__ == '__main__':
	if db.hits.find().count() == 0:
		with open('hits.csv') as source:
			hits_from_csv(source)

	write_csv(5)
