""" Helpers for complex queryies """
#from . import Song
from . import session
from requestlist import RequestList
from played import Played, PlayedShow
from song import Song
from sqlalchemy.sql import func, or_

def get_total_artists(catalogs):
    return session.query(func.count(Song.artist_fullname.distinct()).label('total')).filter(Song.catalog.in_(catalogs)).one()

def get_total_albums(catalogs):
    return session.query(func.count(Song.album_fullname.distinct()).label('total')).filter(Song.catalog.in_(catalogs)).one()

def get_top_10(catalogs=[]):
    return session.query(func.count(Song.artist_name).label('artist_count'),\
                         Song.artist_fullname.label('artist_id'),\
                         Song.artist_fullname.label('artist_fullname')).\
                         filter(Song.catalog.in_(catalogs)).\
                         group_by(Song.artist_name, Song.artist_fullname).\
                         order_by(func.count(Song.artist_name).desc()).limit(10)

def get_top_played_by_all(catalogs):
    for tid, tid_count, title, art, alb, date_played in session.query(Played.track_id.label('track_id'),\
                         func.count(Played.track_id).label('played_count'),\
                         func.max(Song.title).label('title'),\
                         func.max(Song.artist_fullname).label('artist_fullname'),\
                         func.max(Song.album_fullname).label('album_fullname'),
                         func.max(Played.date_played).label('last_play')).\
                    join(Song).\
                    filter(Song.catalog.in_(catalogs)).\
                    group_by(Played.track_id).\
                    order_by(func.count(Played.track_id).desc()).limit(10):
        played = session.query(Played).filter(Played.track_id==tid, Played.date_played==date_played).one()
        yield played, tid_count, date_played

def get_top_played_by_me(catalogs):
    return get_top_played_by_all(catalogs)

def get_top_requested(catalogs):
    for sid, rid, cnt in session.query(RequestList.song_id,\
                                       func.max(RequestList.id),\
                                       func.count(RequestList.song_id)).\
                                 join(Song).\
                                 filter(Song.catalog.in_(catalogs), RequestList.status=='played').\
                                 group_by(RequestList.song_id).limit(10):
        r = session.query(RequestList).join(Song).filter(RequestList.id==rid, Song.catalog.in_(catalogs)).one()
        yield r.song

def get_top_requestors(catalogs):
    return session.query(func.count(RequestList.name).label('request_count'),
                         RequestList.name.label('requestor'),
                         func.max(RequestList.t_stamp).label('last_request')).join(Song).filter(Song.catalog.in_(catalogs)).group_by(RequestList.name).order_by(func.count(RequestList.name).desc()).limit(10)

def get_artist_by_letter(catalogs, letter):
    artists = []
    for s in session.query(Song.artist_name,\
                         Song.artist_prefix,\
                         Song.artist_fullname.label('artist_fullname'),\
                         func.count(Song.title).label('song_count')).\
           filter(func.lower(Song.artist_name).startswith(letter.lower()),\
                  Song.catalog.in_(catalogs)).\
           order_by(Song.artist_name).group_by(Song.artist_fullname):
        a = session.query(Song).filter(Song.artist_fullname==s.artist_fullname).first()
        artists.append(a.artist)
    return artists

def get_artist_letters_counts(catalogs=[]):
    return session.query(func.upper(func.left(Song.artist_name, 1)), func.count(Song.artist_name.distinct())).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(func.upper(func.left(Song.artist_name, 1)))

def get_album_letters_counts(catalogs=[]):
    return session.query(func.upper(func.left(Song.album_name, 1)), func.count(Song.album_name.distinct())).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(func.upper(func.left(Song.album_name, 1)))

def get_album_by_letter(catalogs,  letter):
    albums = []
    for s in session.query(Song.album_name,\
                         Song.album_prefix,\
                         Song.album_fullname,\
                         func.count(Song.title).label('song_count')).\
                         filter(func.lower(Song.album_name).startswith(letter.lower()),\
                                Song.catalog.in_(catalogs)).\
                                order_by(Song.album_name).group_by(Song.album_fullname):
        a = session.query(Song).filter(Song.album_fullname==s.album_fullname).first()
        albums.append(a.album)
    return albums

def get_new_pending_requests_info():
    return session.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

def get_current_requests():
    return session.query(RequestList).\
                       filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)

def get_all_requests_info():
    return session.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)


def get_new_counts(catalogs, start_time):
    return session.query(func.count(Song.id).label('total_count'),\
                         func.sum(Song.time).label('total_time'),\
                         func.sum(Song.size).label('total_size')).\
                        filter(func.extract("EPOCH", Song.addition_time) >= start_time, Song.catalog.in_(catalogs)).one()

def get_new_artists(catalogs, start_time):
    for count, total_time, total_size, addition_time, art_name in session.query(func.count(Song.artist_fullname).label('artist_count'),
                         func.sum(Song.time).label('artist_time'),
                         func.sum(Song.size).label('artist_size'),
                         func.max(Song.addition_time).label('m_addition_time'),
                         func.max(Song.artist_fullname).label('artist_fullname')
                         ).\
                        filter(func.extract("EPOCH", Song.addition_time) >= start_time,\
                               Song.catalog.in_(catalogs)).\
                        group_by(func.lower(Song.artist_fullname)).\
                        order_by(func.max(Song.addition_time).desc()):
        song = session.query(Song).filter(Song.artist_fullname==art_name,\
                                          func.extract("EPOCH", Song.addition_time) >= start_time,\
                                          Song.catalog.in_(catalogs)).first()
        yield count, total_time, total_size, song


def get_last_played(catalogs=[], limit=50):
    return session.query(func.count(Played.date_played), '0',  Played).join(Song).\
        filter(Song.catalog.in_(catalogs)).\
        group_by(Played.date_played, Played.id).\
        order_by(Played.date_played.desc()).limit(limit)

def get_multi_albums(artist_name, song_title):
    return session.query(Song).filter(func.lower(Song.artist_fullname) == func.lower(artist_name),\
                                      func.lower(Song.title) == func.lower(song_title))

def full_text_search(catalogs, phrase):
    return session.query(Song).filter(
                (Song.title.match(phrase) |\
                 Song.artist_fullname.match(phrase) |\
                 Song.album_fullname.match(phrase)), Song.catalog.in_(catalogs))

def advanced_search(catalogs, search_for, phrase):
    if search_for == 'title':
        search = Song.title
    elif search_for == 'artist':
        search = Song.artist_name
    elif search_for == 'album':
        search = Song.album_name
    p = r'%'+phrase+r'%'
    return session.query(Song).filter(search.ilike(p), Song.catalog.in_(catalogs))