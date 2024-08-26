# import arrow
from app import db, cache
from datetime import datetime, UTC
from app.users import User


# association object
class Assistants(db.Model):
    __tablename__ = 'assistants'

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), primary_key=True)

    employee: db.Mapped["Employee"] = db.relationship(
        # back_populates='assigned_ta'
    )
    workshop: db.Mapped["Workshop"] = db.relationship(
        # back_populates='assistants'
    )

    def __repr__(self):
        return '{}'.format(self.employee.name)


# possible workaround pattern for bidirectional reference of User <-> Employee
# class UserModel(User):
#     # employee_email = db.relationship(
#     #     'Employee', backref=db.backref('signin_email')
#     # )
#     pass


class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      db.ForeignKey('user.email')
                      )
    name = db.Column(db.String(64), unique=True)
    join_date = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True, nullable=False)
    degree = db.Column(db.String(32))
    university = db.Column(db.String(64))

    # Note: change this to use association object Assistants instead of table
    # if flask-admin > 1.6.1 does not show strange behavior with association objects
    assigned_ta: db.Mapped[list["Workshop"]] = db.relationship(
        secondary='assistants',
        back_populates='assistants',
        overlaps='workshop,employee',
    )

    assigned_instructor = db.relationship(
        'Workshop',
        backref=db.backref('instructor'))

    def __repr__(self):
        return '{}'.format(self.name)


class Workshop(db.Model):
    __tablename__ = 'workshop'

    id = db.Column(db.Integer, primary_key=True)
    workshop_name = db.Column(db.String(64))
    workshop_category = db.Column(db.Enum(
        "Academy", "DSS", "Corporate", "Weekend", "Others",
        name="workshop_category"), nullable=False)
    workshop_instructor = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    workshop_start = db.Column(db.DateTime, default=datetime.now(UTC), nullable=False)
    workshop_hours = db.Column(db.Integer, nullable=False)
    workshop_venue = db.Column(db.String(64), nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    responses = db.relationship('Response', backref='workshop', lazy='dynamic')

    # Note: change this to use association object Assistants instead of table
    # if flask-admin > 1.6.1 does not show strange behavior with association objects
    assistants: db.Mapped[list["Employee"]] = db.relationship(
        secondary='assistants',
        back_populates='assigned_ta',
        overlaps='workshop,employee',
    )

    def __repr__(self):
        # past = arrow.get(self.workshop_start).humanize()
        # return '{}, {}'.format(self.workshop_name, past)
        return '{}, on {}'.format(self.workshop_name, self.workshop_start.strftime("%B %d, %Y"))

    @cache.memoize(50)
    def printtime(self):
        # time = arrow.get(self.workshop_start).humanize()
        time = self.workshop_start.strftime("%B %d, %Y")
        return time


class Response(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), nullable=False)
    difficulty = db.Column(db.Integer)
    assistants_score = db.Column(db.Integer)
    knowledge = db.Column(db.Integer)
    objectives = db.Column(db.Integer)
    timeliness = db.Column(db.Integer)
    venue_score = db.Column(db.Integer)
    satisfaction_score = db.Column(db.Integer)
    comments = db.Column(db.Text)
