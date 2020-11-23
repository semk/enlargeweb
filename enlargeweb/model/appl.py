"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from enlargeweb.model.prop import ApplianceProperty
from sqlalchemy.types import *
from enlargeweb.lib.plugins import get_plugin_by_id

appliance_dependants_table = sa.Table('appliance_dependants', meta.metadata,
	sa.Column('appl_id', Integer, sa.ForeignKey('appliance.id')),
	sa.Column('depend_on_id', Integer, sa.ForeignKey('appliance.id'))
)

class Appliance(Base):
	"""
	Class represents deployable appliance
	"""
	__tablename__ = 'appliance'

	id = sa.Column(Integer, primary_key = True)
	name = sa.Column(Unicode(64))
	description = sa.Column(UnicodeText)
	arch = sa.Column(String(4))
	plugin_id = sa.Column(UnicodeText(32))
	icon = sa.Column(UnicodeText(128))
	properties = orm.relation(ApplianceProperty, backref = 'appliance', cascade = 'all')
	
	depends_on = orm.relation( 'Appliance', secondary = appliance_dependants_table,
		primaryjoin = id == appliance_dependants_table.c.appl_id,
		secondaryjoin = appliance_dependants_table.c.depend_on_id == id
		)
	
	def __init__(self, id, name, description, arch, plugin_id, icon):
		self.id = id
		self.name = name
		self.description = description
		self.arch = arch
		self.plugin_id = plugin_id
		self.icon = icon
		if not self.icon or len(self.icon) <= 0:
			#load default
			self.icon = '/images/default-appl.png'
		print '-------------- Appliance Icon: %s' % self.icon

	def get_prop_inst(self, name):
		for p in self.properties:
			if p.name == name:
				return p

	def get_prop(self, name):
		inst = self.get_prop_inst(name)
		if inst:
			return inst.value
		else:
			return None
        
	def get_plugin(self):
		return Appliance.get_plugin_for(self.plugin_id)		
		
	@classmethod
	def get_plugin_for(cls, id):
		plugin = get_plugin_by_id(id)
		if not plugin:
			return 'Failed to find plugin for appliance. Please recreate it.'
		return '%s (%s)' % (plugin.type_name, plugin.class_name)

	def __str__(self):
		if self.id:
			return '%s (%s)' % (self.name, self.arch)
		else:
			return 'New Appliance'

"""
class User(object):
    pass
class Keyword(object):
    pass
mapper(Keyword, keywords_table)
mapper(User, users_table, properties={
    'keywords': relation(Keyword, secondary=userkeywords_table,
        primaryjoin=users_table.c.user_id==userkeywords_table.c.user_id,
        secondaryjoin=userkeywords_table.c.keyword_id==keywords_table.c.keyword_id
        )
})"""
