import csv

__author__ = 'Markus'

from request.config import db
from random import randint


def hits_from_csv(source):
	data = csv.DictReader(source, delimiter=',', quotechar="'")
	hits = [x for x in data]
	db.hits.insert_many(hits)


def write_csv(hits_per_task, error_message=None):
	ids = generate_tasks(hits_per_task)

	if error_message is None:
		error_message = 'Please retrieve the correct reply code from our website.\n'

	with open('ids.csv', 'w') as ids_csv:
		ids_csv.write('_task_id,reply_id_gold,reply_id_gold_reason'+'\n')
		for i in ids:
			ids_csv.write(str(i[0])+','+str(i[1])+','+error_message)


def generate_tasks(hits_per_task, random_from=1738295, random_to=9473682):
	tasks = []
	hit_list = db.hits.find()
	hit_ids = [[x['_id'], 0] for x in hit_list]

	while len(hit_ids) > hits_per_task:
		task_id = randint(random_from, random_to)
		reply_id = randint(random_from, random_to)
		task_hit_ids = []
		tmp_hit_ids = range(len(hit_ids))

		for _ in range(0, hits_per_task):
			r = randint(0, len(tmp_hit_ids)-1)
			ti = tmp_hit_ids.pop(r)
			id_el = hit_ids[ti]
			id_el[1] += 1
			task_hit_ids.append(id_el[0])

			if id_el[1] == hits_per_task:
				hit_ids.remove(id_el)
				tmp_hit_ids = range(len(hit_ids))

		hits = {str(e):{'solved': False,
						'response': '',
						'quality': 0.0} for e in task_hit_ids}

		task = {'task_id': task_id,
				'hits': hits,
				'reply': reply_id,
				'finished': False}

		db.tasks.save(task)
		tasks.append((task_id, reply_id))

	return tasks
