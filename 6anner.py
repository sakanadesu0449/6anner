import os
import json
import random
import requests

PARENT = 'json'
OS_SEP = os.sep
USER = '.6anner'
USER_PROFILE = 'user_profile.json'

DEFAULT_USER_PROFILE_SETTIGS = {
	'online_mode': True,
	'online_mode_settings': {
		'timeout': 3,
		'site': 'hzzm',
		'type': ['ts', 'sc', 'ss'],
		'cache': False
	}
}

class BError(Exception):
	pass

class Robots():
	@classmethod
	def robot(cls, site: str, timeout: bool, types: list[str]):
		SITES = {
			'hzzm': RobotHZZM
		}
		if site not in SITES:
			raise ValueError(f'unknown site: {site}')

		return SITES[site](timeout, types)

	def __init__(self, timeout, types: list[str]):
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'

		self.types = types
		self.dynastys = {
			'ts': '唐',
			'ss': '宋',
			'sc': '宋'
		}
		self.headers = {
			'hzmm': {
				'authority': 'hzzm.xusenlin.com',
				'sec-ch-ua-platform': 'Windows',
				'Origin': 'https://hz.xusenlin.com',
				'User-Agent': self.user_agent
			}
		}

class RobotHZZM(Robots):
	def rand_page(self, type: str) -> str:
		paginates = {
			'ts': 5762,
			'ss': 25425,
			'sc': 2106
		}

		rand_p = random.randint(1, paginates[type])
		return f'https://hzzm.xusenlin.com/v1/{type}?pageNum={rand_p}&keyword='

	def get_rand_verse(self) -> tuple:
		_type = random.choice(self.types)
		url = self.rand_page(_type)
		page = requests.get(url, headers = self.headers['hzmm'])

		_json = json.loads(page.text)
		_paragraph_list = _json['data']['list']
		rand_paragraph = random.choice(_paragraph_list)
		author = rand_paragraph['author']
		verse_list = rand_paragraph['paragraphs'].split('||')

		return random.choice(verse_list), self.dynastys[_type], author

	def run(self) -> tuple:
		TYPES = ['ts', 'ss', 'sc']
		for _type in self.types:
			if _type not in TYPES:
				raise ValueError(f'unknown type: {_type}')

		verse = self.get_rand_verse()
		return verse


def user_profile() -> dict:
	USER_PROFILE_PATH = f'{USER}{OS_SEP}{USER_PROFILE}'

	if not os.path.exists(USER):
		os.mkdir(USER)
	with open(USER_PROFILE_PATH, 'r+', encoding = 'utf-8') as _user_profile_f:
		try:
			user_profile = json.loads(_user_profile_f.read())

		except json.JSONDecodeError as _e:
			json.dump(DEFAULT_USER_PROFILE_SETTIGS, _user_profile_f, indent = 4)
			return DEFAULT_USER_PROFILE_SETTIGS

	return user_profile



def main() -> None:
	_user_profile = user_profile()
	if _user_profile['online_mode'] is True:
		r = Robots.robot(
			_user_profile['online_mode_settings']['site'],
			_user_profile['online_mode_settings']['timeout'],
			_user_profile['online_mode_settings']['type']
		)
		verses = r.run()

	print(f'{verses[0]}\n              {verses[1]} - {verses[2]}')



if __name__ == '__main__':
	main()