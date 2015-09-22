import ConfigParser
import codecs

URL = 'url'
REGEX = 'regex'
CONDITION = 'condition'
QUERY = 'query'
MAIL_RECEIVER = 'mail_receiver'
MAIL_MSG = 'mail_msg'
INTERVAL_SECONDS = 'interval_seconds'
WATCH_WEBS = 'watchweb.ini'
MAIL_CONFIG = 'mailconfig.ini'

def get_watch_webs():
	config = ConfigParser.ConfigParser()
	config.readfp(codecs.open(WATCH_WEBS, "r", encoding='utf-8'))
	return [dict(config.items(section)) for section in config.sections()]

def get_mail_config():
	config = ConfigParser.ConfigParser()
	config.readfp(codecs.open(MAIL_CONFIG, "r", encoding='utf-8'))
	result = {}
	for option in config.options("mail"):
		result[option] = config.get("mail", option)
	return result

if __name__ == '__main__':
	get_watch_webs()
