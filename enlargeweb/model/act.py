"""The application's model objects"""
import os, signal
import sqlalchemy as sa
import datetime
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy.types import *

class LogItem(Base):
	"""class represents log entry written by activity"""
	__tablename__ = 'activity_log'
	id = sa.Column(Integer, primary_key = True)
	activity_id = sa.Column('activity_id', Integer, sa.ForeignKey('activity.id'))
	message = sa.Column('message', UnicodeText)
	timestamp = sa.Column('timestamp', TIMESTAMP)

	def __init__(self, activity_id, message, timestamp):
		self.activity_id = activity_id
		self.message = message
		self.timestamp = timestamp

class Activity(Base):
	"""class represents information about activity in system"""

	__tablename__ = 'activity'

	id = sa.Column(Integer, primary_key = True)
	parent_id = sa.Column( Integer, sa.ForeignKey('activity.id'))

	description = sa.Column(UnicodeText)
	status = sa.Column(Integer)
	start_time  = sa.Column(TIMESTAMP)
	end_time = sa.Column(TIMESTAMP)
	proc_id = sa.Column(Integer)
	proc_exit_code = sa.Column(Integer)
	owner = sa.Column(Unicode(64))

	children = orm.relation("Activity", backref=orm.backref('parent_activity', remote_side='Activity.id'))
	logs = orm.relation(LogItem, backref=orm.backref('activity'))
	
	def put_log(self, msg):
		log = LogItem(self.id, msg, datetime.datetime.now())
		meta.Session.add(log)
		meta.Session.commit()
		
	def get_status(self):
		if self.status == 0:
			return 'Canceled'
		elif self.status == 1:
			return 'In Progress'
		elif self.status == 2:
			return 'Finished'
		elif self.status == 3:
			return 'Error'
		else:
			raise Exception()
			
	def get_status_color(self):
		if self.status == 0:
			return 'orange';
		elif self.status == 1:
			return 'LightGreen'
		elif self.status == 2:
			return 'DarkGreen'
		elif self.status == 3:
			return 'red'
		else:
			raise Exception()
	
	def __stop_activity(self, status, user, message, code, kill_proc):
		self.status = status
		self.end_time = datetime.datetime.now()
		self.proc_exit_code = code
		self.put_log('%s(%s) : %s' % ( self.get_status(), user, message))
		if kill_proc:
			try:
				self.put_log('Killing process %s' % self.proc_id)
				os.kill(int(self.proc_id), signal.SIGKILL)
			except OSError, oserr:
				self.put_log('Cannot kill process: %s' % str(oserr))
	
	def finish(self, user, message, code, kill_proc = True):
		self.__stop_activity(2, user, message, code, kill_proc)
		
	def cancel(self, user, message, code, kill_proc = True):
		self.__stop_activity(0, user, message, code, kill_proc)
		
	def error(self, user, message, code, kill_proc = True):
		self.__stop_activity(3, user, message, code, kill_proc)
		
	def get_start_time(self):
		delta = datetime.datetime.now() - self.start_time
		if delta.days > 24:
			return 'Too long ago'
		elif delta.days > 0:
			if delta.days == 1:
				return '%s day ago on %s' % ( delta.days, Activity.format_datetime(self.start_time) )
			else:
				return '%s days ago on %s' % ( delta.days, Activity.format_datetime(self.start_time) )
		elif (delta.seconds  < 3600):
			if (delta.seconds / 60) > 1:
				return '%s minutes ago' % (delta.seconds / 60)
			else:
				return '%s minute ago' % (delta.seconds / 60)
		else:
			return 'at %s ' % Activity.format_datetime(self.start_time)

	def get_end_time(self):
		if self.end_time:
			return self.format_datetime(self.end_time)
		else:
			return 'Running'
	
	@classmethod
	def format_datetime(cls, date):
		return date.strftime("%A, %d. %B %Y %I:%M%p")

	def __init__(self, parent_id, description, start_time, proc_id, owner):
		self.parent_id = parent_id
		self.description = description
		self.status = 1
		self.start_time = start_time
		self.proc_id = proc_id
		self.owner = owner

	def __str__(self):
		return '%s (%s)' % (self.description, self.status)

