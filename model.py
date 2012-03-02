import datetime
import sqlalchemy as sa
from sqlalchemy.types import *

from metamodel import *
import hashlib

@Model
class User(object):
	id = PrimaryKey(Integer)
	enabled = Boolean
	admin = Boolean
	username = Unicode(255)
	password = String(40)

	@staticmethod
	def hash(password):
		for i in range(1000):
			password = hashlib.sha1(password).hexdigest()
		return password

	@staticmethod
	def add(username, password, admin):
		User.create(
			enabled=True, 
			username=username, 
			password=User.hash(password), 
			admin=admin
		)
		session.commit()
	
	@staticmethod
	def find(username, password=None):
		try:
			if password != None:
				return session.query(User).filter(sa.and_(User.enabled == True, User.username == username, User.password == User.hash(password))).one()
			else:
				return session.query(User).filter(sa.and_(User.enabled == True, User.username == username)).one()
		except:
			return False
	
	def change(self, username, password, admin):
		if password == None:
			password = self.password
		else:
			password = User.hash(password)
		self.update(username=username, admin=admin, password=password)
		session.commit()

@Model
class Config(object):
	id = PrimaryKey(Integer)
	name = String(20)
	value = Unicode(255)

	@staticmethod
	def get(name):
		try:
			return session.query(Config).filter(Config.name == unicode(name)).one().value
		except:
			return None

	@staticmethod
	def getString(name):
		data = Config.get(name)
		if data == None:
			return None
		else:
			return str(data)

	@staticmethod
	def set(name, value):
		name, value = unicode(name), unicode(value)
		try:
			row = session.query(Config).filter(Config.name == name).one()
			row.update(value=value)
		except:
			Config.create(
				name=name,
				value=value
			)

		session.commit()

setup()
