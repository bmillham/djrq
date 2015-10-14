from paste.registry import StackedObjectProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, ForeignKey, func
from sqlalchemy import Boolean, Text, DateTime, Enum, or_, Interval
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
session = StackedObjectProxy()
prefixes = ['the']

from .song import Song
from .history import Played
from .requestlist import RequestList

def get_new_pending_requests_info():
    return session.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

def get_all_requests_info():
    return session.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)

def get_top_10(catalogs=[]):
    return session.query(func.count(Song.artist_name).label('artist_count'),\
                         Song.artist_fullname,\
                         Song.artist_name).\
                         filter(Song.catalog.in_(catalogs)).\
                         group_by(Song.artist_name, Song.artist_fullname).\
                         order_by(func.count(Song.artist_name).desc()).limit(10)

def get_top_played_by_all(catalogs):
    return session.query(func.count(Played.track_id).label('played_count'),\
                         func.max(Song.title).label('title'),\
                         func.max(Song.artist_fullname).label('artist_fullname'),\
                         func.max(Song.album_fullname).label('album_fullname'),
                         func.max(Played.date_played).label('last_play')).\
                    join(Song).\
                    filter(Song.catalog.in_(catalogs)).\
                    group_by(Played.track_id).\
                    order_by(func.count(Played.track_id).desc()).limit(10)

def get_artist_by_letter(catalogs, letter):
    return session.query(Song.artist_name,\
                         Song.artist_prefix,\
                         Song.artist_fullname,\
                         func.count(Song.title).label('song_count')).\
           filter(func.lower(Song.artist_name).startswith(letter.lower()),\
                  Song.catalog.in_(catalogs)).\
           order_by(Song.artist_name).group_by(Song.artist_fullname)

def get_new_counts(catalogs, start_time):
    return session.query(func.count(Song.id).label('total_count'),\
                         func.sum(Song.time).label('total_time'),\
                         func.sum(Song.size).label('total_size')).\
                        filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).one()

def get_new_artists(catalogs, start_time):
    return session.query(func.count(Song.artist_fullname).label('artist_count'),
                         func.sum(Song.time).label('artist_time'),
                         func.sum(Song.size).label('artist_size'),
                         func.max(Song.addition_time).label('m_addition_time'),
                         func.max(Song.artist_fullname).label('artist_fullname')
                         ).\
                        filter(Song.addition_time >= start_time,\
                               Song.catalog.in_(catalogs)).\
                        group_by(func.lower(Song.artist_fullname)).\
                        order_by(func.max(Song.addition_time).desc())

def get_album_by_letter(catalogs,  letter):
    return session.query(Song.album_name,\
                         Song.album_prefix,\
                         Song.album_fullname,\
                         func.count(Song.title).label('song_count')).\
                         filter(func.lower(Song.album_name).startswith(letter.lower()),\
                                Song.catalog.in_(catalogs)).\
           order_by(Song.album_name).group_by(Song.album_fullname)

def get_last_played(catalogs=[], limit=50):
    return session.query(func.count(Played.date_played),  Played).join(Song).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(Played.date_played, Played.id).\
        order_by(Played.date_played.desc()).limit(limit)

def get_multi_albums(artist_name, song_title):
    return session.query(Song).filter(func.lower(Song.artist_fullname) == func.lower(artist_name),\
                                      func.lower(Song.title) == func.lower(song_title))

def get_artist_letters_counts(catalogs=[]):
    return session.query(func.left(Song.artist_name, 1), func.count(Song.artist_name.distinct())).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(func.left(Song.artist_name, 1))

def get_album_letters_counts(catalogs=[]):
    return session.query(func.left(Song.album_name, 1), func.count(Song.album_name.distinct())).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(func.left(Song.album_name, 1))

def full_text_search(phrase, catalogs=[]):
    return session.query(Song).filter(
                (Song.title.match(phrase) |\
                 Song.artist_fullname.match(phrase) |\
                 Song.album_fullname.match(phrase)), Song.catalog.in_(catalogs))

def advanced_search(search_for, phrase, catalogs=[]):
    if search_for == 'title':
        search = Song.title
    elif search_for == 'artist':
        search = Song.artist_name
    elif search_for == 'album':
        search = Song.album_name
    p = r'%'+phrase+r'%'
    return session.query(Song).filter(search.ilike(p), Song.catalog.in_(catalogs))