from handler import handler

@handler(unicode)
def echo(string):
	return unicode(string)

@handler(unicode)
def reverse(string):
	string = list(string)
	string.reverse()
	return ''.join(string)

greetings = dict(
	en='Hello, %s!', 
	de='Guten tag, %s!'
)

@handler(unicode, unicode)
def hello(lang, name):
	return greetings[lang] % name
