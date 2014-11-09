import re

from .base_item import BaseItem
import datetime


class VideoItem(BaseItem):
    INFO_GENRE = 'genre'  # (string)
    INFO_AIRED = 'aired'  # (string)
    INFO_DURATION = 'duration'  # (int) seconds
    INFO_DIRECTOR = 'director'  # (string)
    INFO_PREMIERED = 'premiered'  # (string) iso 8601
    INFO_EPISODE = 'episode'  # (int)
    INFO_SEASON = 'season'  # (int)
    INFO_YEAR = 'year'  # (int)
    INFO_PLOT = 'plot'  # (string)
    INFO_TITLE = 'title'  # (string)
    INFO_IMDB_ID = 'imdb_id'  # (string)
    INFO_CAST = 'cast'  # (list of string)
    INFO_RATING = 'rating'  # float
    INFO_DATE_ADDED = 'date_added'  # string

    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        self._genre = None
        self._aired = None
        self._duration = None
        self._director = None
        self._premiered = None
        self._episode = None
        self._season = None
        self._year = None
        self._plot = None
        self._title = None
        self._imdb_id = None
        self._cast = None
        self._rating = None
        self._track_number = None
        pass

    def set_title(self, title):
        self._title = unicode(title)
        pass

    def get_title(self):
        return self._title

    def set_track_number(self, track_number):
        self._track_number = track_number
        pass

    def get_track_number(self):
        return self._track_number

    def set_year(self, year):
        self._year = int(year)
        pass

    def get_year(self):
        return self._year

    def set_premiered(self, year, month, day):
        date = datetime.date(year, month, day)
        self._premiered =date.isoformat()
        pass

    def get_premiered(self):
        return self._premiered

    def set_plot(self, plot):
        self._plot = unicode(plot)
        pass

    def get_plot(self):
        return self._plot

    def set_rating(self, rating):
        self._rating = float(rating)
        pass

    def get_rating(self):
        return self._rating

    def set_director(self, director_name):
        self._director = unicode(director_name)
        pass

    def get_director(self):
        return self._director

    def add_cast(self, cast):
        if self._cast is None:
            self._cast = []
            pass
        self._cast.append(cast)
        pass

    def get_cast(self):
        return self._cast

    def set_imdb_id(self, url_or_id):
        re_match = re.match('(http\:\/\/)?www.imdb.(com|de)\/title\/(?P<imdbid>[t0-9]+)(\/)?', url_or_id)
        if re_match:
            self._imdb_id = re_match.group('imdbid')
        else:
            self._imdb_id = url_or_id
        pass

    def get_imdb_id(self):
        return self._imdb_id

    def set_episode(self, episode):
        self._episode = int(episode)
        pass

    def get_episode(self):
        return self._episode

    def set_season(self, season):
        self._season = int(season)
        pass

    def get_season(self):
        return self._season

    def set_duration(self, hours, minutes, seconds=0):
        _seconds = seconds
        _seconds += minutes * 60
        _seconds += hours * 60 * 60
        self.set_duration_from_seconds(_seconds)
        pass

    def set_duration_from_minutes(self, minutes):
        self.set_duration_from_seconds(int(minutes) * 60)
        pass

    def set_duration_from_seconds(self, seconds):
        self._duration = int(seconds)
        pass

    def get_duration(self):
        return self._duration

    def set_aired(self, year, month, day):
        date = datetime.date(year, month, day)
        self._aired = date.isoformat()
        pass

    def get_aired(self):
        return self._aired

    def set_genre(self, genre):
        self._genre = unicode(genre)
        pass

    def get_genre(self):
        return self._genre

    pass