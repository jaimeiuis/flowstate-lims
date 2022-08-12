import datetime
import pytz

from sqlalchemy import DateTime

from flowstate.extensions import db


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.
    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime.datetime) and value.tzinfo is None:
            raise ValueError('{!r} must be TZ-aware'.format(value))
        return value

    def __repr__(self):
        return 'AwareDateTime()'


class ResourceMixin(object):
    def save(self):
        """ Save a model instance. """
        db.session.add(self)
        db.session.commit()

        return self

    def delete(self):
        """ Delete a model instance. """
        db.session.delete(self)
        return db.session.commit()