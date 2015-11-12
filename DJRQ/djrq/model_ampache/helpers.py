""" Helpers for complex queryies """

from . import session
from requestlist import RequestList
from played import Played
from song import Song
from artist import Artist
from album import Album
from sqlalchemy.sql import func, or_

def get_played_by_me(catalogs=[]):
    return session.query(func.count(Played.track_id.distinct()).label('total')).\
        join(Song).filter(Song.catalog.in_(catalogs), Played.played_by_me == 1).one()

def get_song_stats(catalogs=[]):
    return session.query(func.sum(Song.size).label('song_size'),
                              func.count(Song.id).label('total_songs'),
                              func.avg(Song.size).label('avg_song_size'),
                              func.sum(Song.time).label('song_time'),
                              func.avg(Song.time).label('avg_song_time')).filter(Song.catalog.in_(catalogs)).one()

def get_total_artists(catalogs):
    return session.query(func.count(Artist.fullname.distinct()).label('total')).join(Song).filter(Song.catalog.in_(catalogs)).one()

def get_total_albums(catalogs):
    return session.query(func.count(Album.id.distinct()).label('total')).join(Song).filter(Song.catalog.in_(catalogs)).one()

def get_new_pending_requests_info():
    return session.query(func.count(RequestList.id).label('request_count'),
                  func.sum(Song.time).label('request_length')).\
                  join(Song).filter(or_(RequestList.status=="new", RequestList.status=='pending')).one()

def get_all_requests_info():
    return session.query(func.count(RequestList.status).label('request_count'),
                         RequestList.status,
                         func.sum(Song.time).label('request_length')).\
                         join(Song).group_by(RequestList.status)

def get_last_played(catalogs, limit=50):
    return session.query(func.count(Played.date_played), func.avg(Song.time), Played).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.date_played).order_by(Played.date_played.desc()).limit(limit)

def get_multi_ablums(artist_name, song_title):
    return session.query(Song).join(Album).join(Artist).filter(Artist.fullname == artist_name, Song.title == song_title)

def get_artist_letters_counts(catalogs):
    return session.query(func.left(Artist.name, 1), func.count(Artist.id.distinct())).join(Song).filter(Song.catalog.in_(catalogs)).group_by(func.left(Artist.name, 1))

def get_album_letters_counts(catalogs):
    return session.query(func.left(Album.name, 1), func.count(Album.id.distinct())).join(Song).filter(Song.catalog.in_(catalogs)).group_by(func.left(Album.name, 1))

def get_new_artists(catalogs, start_time):
    return session.query(func.count(Song.artist_id), func.sum(Song.time), func.sum(Song.size), Song).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).order_by(Song.addition_time.desc()).group_by(Song.artist_id)

def get_new_counts(catalogs, start_time):
    return session.query(func.count(Song.id), func.sum(Song.time), func.sum(Song.size)).filter(Song.addition_time >= start_time, Song.catalog.in_(catalogs)).one()

def get_artist_by_letter(catalogs, letter):
    return session.query(Artist).join(Song).filter(Artist.name.startswith(letter), Song.catalog.in_(catalogs)).order_by(Artist.name).group_by(Artist.id)

def get_album_by_letter(catalogs, letter):
    return session.query(Album).join(Song).filter(Album.name.startswith(letter), Song.catalog.in_(catalogs)).order_by(Album.name).group_by(Album.id)

def get_top_10(catalogs):
    return session.query(func.count(Song.artist_id).label('artist_count'),
                         Song.artist_id,
                         Artist.fullname.label('artist_fullname')).join(Artist).filter(Song.catalog.in_(catalogs)).group_by(Song.artist_id).order_by(func.count(Song.artist_id).desc()).limit(10)

def get_top_played_by_me(catalogs):
    return  session.query(Played,
                          func.count(Played.track_id).label('played_count'),
                          func.max(Played.date_played).label('date_played')).join(Song).filter(Song.catalog.in_(catalogs), Played.played_by_me == 1).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)

def get_top_played_by_all(catalogs):
    return session.query(func.count(Played.track_id), Song, func.max(Played.date_played)).join(Song).filter(Song.catalog.in_(catalogs)).group_by(Played.track_id).order_by(func.count(Played.track_id).desc()).limit(10)
    
def get_top_requested(catalogs):
    return session.query(Song).\
                         join(RequestList).\
                         filter(Song.catalog.in_(catalogs), RequestList.status == 'played').\
                         group_by(RequestList.song_id).\
                         order_by(func.count(RequestList.song_id).desc()).limit(10)

def get_top_requestors(catalogs):
    return session.query(func.count(RequestList.name).label('request_count'),
                         RequestList.name.label('requestor'),
                         func.max(RequestList.t_stamp).label('last_request')).join(Song).filter(Song.catalog.in_(catalogs)).group_by(RequestList.name).order_by(func.count(RequestList.name).desc()).limit(10)

def full_text_search(catalogs, phrase):
    return session.query(Song).join(Artist).join(Album).filter(((Song.title.match(phrase)) | (Artist.name.match(phrase)) | (Album.name.match(phrase))), Song.catalog.in_(catalogs))

def advanced_search(catalogs, search_for, phrase):
    if search_for == 'title':
        search = Song.title
    elif search_for == 'artist':
        search = Artist.name
    elif search_for == 'album':
        search = Album.name
    return session.query(Song).join(Artist).join(Album).filter(search.like(phrase), Song.catalog.in_(catalogs))

def get_current_requests():
    return session.query(RequestList).\
                       filter((RequestList.status == 'new') | (RequestList.status == 'pending')).order_by(RequestList.id)
