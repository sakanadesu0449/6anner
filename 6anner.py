import os
import json
import random
import requests

#from abc import ABC, abstractmethod

PARENT = 'json'
class BError(Exception):
	pass

class Robots():
	@classmethod
	def robot(cls, site: str, types: list[str]):

		SITES = {
			'hzmm': RobotHZZM
		}
		TYPES = ['ts', 'ss', 'sc']
		if site not in SITES:
			raise ValueError(f'unknown site: {site}')
		for _t in types:
			if _t not in TYPES:
				raise ValueError(f'unknown type: {_t}')

		return SITES[site](types)

	def __init__(self, types: list[str]):
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

		self.types = types
		self.headers = {
			'hzmm': {
			'authority': 'hzzm.xusenlin.com',
			'sec-ch-ua-platform': 'Windows',
			'Origin': 'https://hz.xusenlin.com',
			'User-Agent': self.user_agent
			}
		}

class RobotHZZM(Robots):
	def rand_page(self) -> str:
		paginates = {
			'ts': 5762,
			'ss': 25425,
			'sc': 2106
		}
		_type = random.choice(self.types)
		rand_p = random.randint(1, paginates[_type])
		return f'https://hzzm.xusenlin.com/v1/{_type}?pageNum={rand_p}&keyword='

	def get_rand_verse(self) -> str:
		url = self.rand_page()
		#print(url)
		page = requests.get(url, headers = self.headers['hzmm'])

		#print(page.status_code)
		_json = json.loads(page.text)
		_paragraph_list = _json['data']['list']
		rand_paragraph = random.choice(_paragraph_list)
		author = rand_paragraph['author']
		verse_list = rand_paragraph['paragraphs'].split('||')

		return random.choice(verse_list), author



def get_random_file(parent: str) -> str:

	_dir = os.path.dirname(__file__)
	json_parent_dir = os.path.join(_dir, parent)

	files = [os.path.join(json_parent_dir, _f) for _f in os.listdir(json_parent_dir)]
	return random.choice(files)

if __name__ == '__main__':

	r = Robots.robot('hzmm', ['ts', 'ss', 'sc'])
	verses = r.get_rand_verse()
	print(f'{verses[0]}\n              {verses[1]}')
'''
	except Exception as err:
		print(err)
'''




'''
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
'''


