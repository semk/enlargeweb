"""The application's model objects"""
import sqlalchemy as sa
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy import orm
from sqlalchemy.types import *

# FIXME: possibly it would be better to implement a single-table inheritance
#        by configuring a polymorphic mapper, however implementation below
#        still looks good, as DnsRecord always has all necessary information

class DnsRecord(Base):
    """
    Class represents DNS record for BIND server DLZ Driver
    """

    __tablename__ = 'dns_records'

    id = sa.Column(Integer, primary_key = True)
    zone = sa.Column(Text)
    host = sa.Column(Text)
    data = sa.Column(Text)
    type = sa.Column(Text)
    resp_person = sa.Column(Text)
    serial = sa.Column(Integer)

    # all parameters below are non-important
    # but should be present for correct Bind DLZ working

    # time-to-live of record in cache of secondary DNS servers
    ttl = sa.Column(Integer)
    # how often secondary DNS servers should query us for zone updates
    refresh = sa.Column(Integer)
    # how long to wait between update queries
    retry = sa.Column(Integer)
    # when the record expires if no updates available
    expire = sa.Column(Integer)
    # time-to-live in secondary DNS servers cache of negative responses
    minimum = sa.Column(Integer)
    # mail server priority
    mx_priority = sa.Column(Integer)

    def __init__(self, id, zone, host, type, data, resp_person, \
              serial, ttl = 3600, refresh = 1800, retry = 1800, \
                 expire = 3600, minimum = 10, mx_priority = 20):
        self.id = id
        self.zone = zone
        self.host = host
        self.ttl = ttl
        self.type = type
        self.data = data
        self.resp_person = resp_person
        self.serial = serial
        self.refresh = refresh
        self.retry = retry
        self.expire = expire
        self.minimum = minimum
        self.mx_priority = mx_priority

def init_tables():
    zone = DnsRecord(
        None,
        'deploy',
        '@',
        'soa',
        'deploy',
        'nickv@parallels.com',
        2008122601,
        3600,
        1800,
        1800,
        3600,
        10,
        20
    )
    meta.Session.add(zone)
    meta.Session.commit()
