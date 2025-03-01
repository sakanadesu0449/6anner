import os
import json
import random

PARENT = 'json'

def get_random_file(parent: str) -> str:

	_dir = os.path.dirname(__file__)
	json_parent_dir = os.path.join(_dir, parent)

	files = [os.path.join(json_parent_dir, _f) for _f in os.listdir(json_parent_dir)]
	return random.choice(files)

if __name__ == '__main__':
	file_path = get_random_file(PARENT)
	if 'song' in file_path:
		dynasty = '宋'
	else:
		dynasty = '唐'
	with open(file_path, 'r', encoding = 'utf-8') as _json:
		paragraphs_list = json.loads(_json.read())
		rand_paragraph = random.choice(paragraphs_list)
		rand_verse = random.choice(rand_paragraph['paragraphs'])
		rand_verse_poet = rand_paragraph['author']

		print(rand_verse)
		print(f'                {dynasty} - {rand_verse_poet}')
