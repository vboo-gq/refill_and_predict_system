"""Database models"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Region(Base):
    """Model for region"""
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gold_limit = Column(SmallInteger)
    oil_limit = Column(SmallInteger)
    ore_limit = Column(SmallInteger)
    uranium_limit = Column(SmallInteger)
    diamond_limit = Column(SmallInteger)


class DeepExploration(Base):
    """Model for deep exploration"""
    __tablename__ = 'deep_exploration'
    id = Column(Integer, primary_key=True)
    date_time_end = Column(DateTime)
    region_id = Column(Integer)
    resource_type = Column(SmallInteger)
    region_id = Column(Integer, ForeignKey('region.id'))
    region_track = relationship(
        "Region",
        backref=backref("deep_explorations", lazy="dynamic")
    )


class ResourceTrack(Base):
    """Model for resource track"""
    __tablename__ = 'resource_track'
    id = Column(Integer, primary_key=True)
    resource_type = Column(SmallInteger)
    date_time = Column(DateTime, default=datetime.datetime.now)
    state_id = Column(Integer, ForeignKey('state.id'))
    resource_track = relationship(
        "State",
        backref=backref("resource_tracks", lazy="dynamic")
    )


class ResourceStat(Base):
    """Model for resource stat"""
    __tablename__ = 'resource_stat'
    id = Column(Integer, primary_key=True)
    explored = Column(SmallInteger)
    deep_exploration = Column(SmallInteger)
    limit_left = Column(SmallInteger)

    resource_track_id = Column(Integer, ForeignKey('resource_track.id'))
    resource_track = relationship(
        "ResourceTrack",
        backref=backref("resource_stats", lazy="dynamic")
    )

    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(
        "Region",
        backref=backref("resource_stats", lazy="dynamic")
    )

    def total(self):
        """total left"""
        return self.limit_left + self.explored


class State(Base):
    """Model for state"""
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)
