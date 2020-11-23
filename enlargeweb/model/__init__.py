"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from enlargeweb.model import meta

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.engine = engine
