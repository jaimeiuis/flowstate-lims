from flowstate.extensions import db

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