from collections import OrderedDict

import datetime
import pytz
from lib.util_sqlalchemy import AwareDateTime

from flowstate.extensions import db


class Sample(db.Model):
    TYPE = OrderedDict([
        ('saliva', 'Saliva'),
        ('nasopharyngeal', 'Nasopharyngeal'),
    ])

    TEST = OrderedDict([
        ('covid19', 'COVID19'),
    ])

    RESULT = OrderedDict([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('retest', 'Retest')
    ])

    __tablename__ = 'samples'
    id = db.Column(db.Integer, primary_key=True)

    barcode = db.Column(db.String(24), unique=True, index=True)
    sample_type = db.Column(db.Enum(*TYPE, name='sample_types', native_enum=False),
                            index=True, nullable=False)
    valid = db.Column('is_valid', db.Boolean(), nullable=False,
                        server_default='1')
    test = db.Column(db.Enum(*TEST, name='test_types', native_enum=False),
                                index=True, nullable=False)
    result = db.Column(db.Enum(*RESULT, name='result_types', native_enum=False),
                                index=True, nullable=False)
    collection_date = db.Column(AwareDateTime(), default=datetime.datetime.now(pytz.utc))
    accession_date = db.Column(AwareDateTime())
    test_count = db.Column(db.Integer, nullable=False, default=0)
    report_date = db.Column(AwareDateTime())

    def __init__(self, **kwargs):
        """ Call Flask-SQLAlchemy's constructor. """
        super(User, self).__init__(**kwargs)

    @classmethod
    def find_by_barcode(cls, barcode):
        """ Find a sample via barcode. """
        return Sample.query.filter(
            (Sample.barcode == barcode)).first()

    @classmethod
    def type_to_test(cls, sample_type, test):
        """ Ensure that a sample type can only associated be certain tests. """
        pass

    def update_test_count(self):
        """ Increment the test count. """
        self.test_count += 1
        return self.save()

    def update_accession_date(self):
        """ Update the accession date. """
        self.accession_date = datetime.datetime.now(pytz.utc)
        return self.save()

    @classmethod
    def max_test_count(cls, sample):
        """ Only allow a max test count of 3. """
        if sample.test_count >= 3:
            sample.result = 'retest'
            sample.report_date = datetime.datetime.now(pytz.utc)

            return self.save()

    @classmethod
    def expiration(self):
        """
        Report a sample's result as Invalid if it is older than a certain threshold.
        """
        if self.accession_date - self.collection_date >= 3:
            self.valid = False
            self.report_date = datetime.datetime.now(pytz.utc)

        return self.save()

    def is_valid(self):
        """ Return whether a sample is valid. """
        return self.valid

    def result(sample, result):
        """ Set a sample's result and report_date. """
        self.result = result
        self.report_date = datetime.datetime.now(pytz.utc)

        return self.save()

    def save(self):
        """ Save a model instance. """
        db.session.add(self)
        db.session.commit()

        return self


class Dashboard(object):
    @classmethod
    def group_and_count_samples(cls):
        return Dashboard._group_and_count(Sample, Sample.test)

    @classmethod
    def _group_and_count(cls, model, field):
        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        results = {
            'query': query,
            'total': model.query.count()
        }

        return results


    
