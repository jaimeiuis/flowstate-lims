from collections import OrderedDict

from flowstate.extensions import db


class Sample(db.Model):
    TYPE = OrderedDict([
        ()
    ])

    TEST = OrderedDict([
        ()
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
    accession_date = db.Column()
    test_count = db.Column(db.Integer, nullable=False, default=0)
    report_date = db.Column()
