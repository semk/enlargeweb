"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy.types import *

class Property(Base):
	"""
	Class represents custom property
	"""
	__tablename__ = 'property'

	id = sa.Column(Integer, primary_key = True)
	name = sa.Column(String(32))
	type = sa.Column(String(16))
	property_group = sa.Column(String(16))

	def __init__(self, id, name, type, property_group):
		self.id = id
		self.name = name
		self.type = type
		self.property_group = property_group

class ApplianceProperty(Base):
	"""
	Class represents appliance property
	"""
	__tablename__ = 'appliance_property'

	id = sa.Column(Integer, primary_key = True)
	appliance_id = sa.Column(Integer, sa.ForeignKey('appliance.id'))
	name = sa.Column(String(64))
	prop_name = sa.Column(Unicode(32))
	value = sa.Column(UnicodeText)

	def __init__(self, appliance_id, name, prop_name, value):
		self.appliance_id = appliance_id
		self.name = name
		self.prop_name = prop_name
		self.value = value

	def __str__(self):
		return 'appl:%s, %s(%s) = %s' % (self.appliance_id, self.name, self.prop_name, self.value)
