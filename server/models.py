from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship('Signup', back_populates='activity')
    # Add serialization rules
    serialize_rules = ('-signups.activity', )

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship('Signup', back_populates='camper')
    # Add serialization rules
    serialize_rules = ('-signups.camper', )
    # Add validation
    @validates('age')
    def validate_age(self, key, value):
        if not (0 <= value <= 120):  # Example age validation, adjust as needed
            raise ValueError('Age must be between 0 and 120')
        return value
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)

    activity = db.relationship('Activity', back_populates='signups')
    camper = db.relationship('Camper', back_populates='signups')

    # Add relationships
    
    # Add serialization rules
    serialize_rules = ('-activity.signups', '-camper.signups', )
    # Add validation
    @validates('time')
    def validate_time(self, key, value):
        if not (0 <= value <= 24):  # Example time validation, adjust as needed
            raise ValueError('Time must be between 0 and 24')
        return value
    def __repr__(self):
        return '<Signup {}: Activity {} - Camper {}>'.format(self.id, self.activity_id, self.camper_id)


# add any models you may need.
