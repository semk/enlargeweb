"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy.types import *

class Vendor(Base):
	"""
	Class represents device vendor
	"""

	__tablename__ = 'vendor'

	id = sa.Column(Integer, primary_key = True)
	name = sa.Column(Unicode(64))

	def __init__(self, id, name):
		self.id = id
		self.name = name

class Device(Base):
	"""
	Class represents device
	"""
	__tablename__ = 'device'

	id = sa.Column(Integer, primary_key = True)
	vendor_id = sa.Column(Integer, sa.ForeignKey('vendor.id'))
	device_id = sa.Column(Integer)
	name = sa.Column(Unicode(64))

	vendor = orm.relation(Vendor)

	def __init__(self, id, name, vendor_id, device_id):
		self.id = id
		self.name = name
		self.type = type
		self.property_group = property_group

