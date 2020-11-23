"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy.types import *

class UserAttribute(Base):
	"""
	Class represents internal user attributes
	"""
	__tablename__ = 'user_attributes'
	id = sa.Column(Integer, primary_key = True)
	user_id = sa.Column(Integer, sa.ForeignKey('user.id'))
	name = sa.Column(String(64))
	value = sa.Column(String(64))

class User(Base):
	"""
	Class represents user
	"""
	__tablename__ = 'user'

	id = sa.Column(Integer, primary_key = True)
	login = sa.Column(String(64))
	password = sa.Column(String(256))
	first_name = sa.Column(String(64))
	second_name = sa.Column(String(64))
	department = sa.Column(Unicode(64))
	attributes = orm.relation(UserAttribute, cascade='all')

	def __init__(self, id, login, first_name, second_name, department):
		self.id = id
		self.login = login
		self.first_name = first_name
		self.second_name = second_name
		self.department = department

	def get_attr(self, name):
		for attr in self.attributes:
			if attr.name == name:
				return attr
		return None
		
	def __str__(self):
		return '%s %s - %s' % (self.first_name, self.second_name, self.department)
