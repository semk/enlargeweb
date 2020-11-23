import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.types import *
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from enlargeweb.model.act import Activity
from sqlalchemy.orm.collections import collection
import operator

def srvact_collection(child_attr):
    """
    Factory returning a SrvActCollection with proxy to
    attribute ServerActivity.child_attr.
    """
    return lambda: SrvActCollection(child_attr)


class ServerActivity(Base):
    """
    Class represents Node/Activity association
    """
    __tablename__ = 'node_activity'

    node_id = sa.Column(Integer, sa.ForeignKey('node.id'), primary_key = True)
    activity_id = sa.Column(Integer, sa.ForeignKey('activity.id'), primary_key = True)
    master = sa.Column(Boolean)

    activity_info = orm.relation(
        Activity,
        backref = orm.backref(
            'servers',
            collection_class = srvact_collection('server_info')
        )
    )

class SrvActCollection(object):
    key_mapping = {
        'master': True,
        'slaves': False
    }

    def __init__(self, child_attr):
        self._data = {
            True: [],
            False: []
        }
        self._child_attr = child_attr

    @collection.appender
    def _sa_append(self, srv_act):
        """
        Method is invoked by SQLAlchemy to
        populate the collection from DB
        """
        self._data[srv_act.master].append(srv_act)

    @collection.adds(1)
    def _add_new(self, srv_act):
        self._data[srv_act.master].append(srv_act)

    @collection.remover
    def remove(self, item):
        raise Exception('Not implemented')

    def __getitem__(self, i):
        """
        Allow to call us a dictionary.
        We also proxy the call to _data[i], attribute named self._child_attr.
        """
        key = SrvActCollection.key_mapping[i]
        if len(self._data[key]) > 0:
            return [getattr(x, self._child_attr) for x in self._data[key]]
        return []

    @collection.iterator
    def __iter__(self):
        for k,v in self._data.iteritems():
            for t in v:
                yield t

    def add_new(self, id, is_master):
        """
        Add new object
        Server->Activity.servers or Activity->Server.activites
        """
        srv_act = ServerActivity()
        srv_act.node_id = id
        srv_act.master = is_master
        self._add_new(srv_act)
