from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User looking to seek healthcare"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)   
    password = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    market = db.Column(db.String(15), nullable=False)
    # state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)


    def __repr__(self):

        return f"<User user_id={self.user_id} email={self.email}>"
                                                

class Carrier(db.Model):
    """Types of health insurance carriers"""

    __tablename__ = "carriers"

    carrier_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(25), nullable=False)


    def __repr__(self):

        return f"<Carrier carrier_id={self.carrier_id} name={self.name}>"
                                

class Plan(db.Model):
    """User's choice of plan(s)"""

    __tablename__ = "plans"

    plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    plan_org = db.Column(db.String(10), nullable = True)
    name = db.Column(db.String(100), nullable=False)
    vericred_id = db.Column(db.Integer, nullable=True)
    plan_type = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)
    carrier_id = db.Column(db.Integer,
                           db.ForeignKey('carriers.carrier_id'), index=True)


    # Define relationship to carrier
    carrier = db.relationship("Carrier",
                              backref=db.backref("plans", order_by=plan_id))

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("plans", order_by=plan_id))                              


    def __repr__(self):

        return f"<Plan plan_id={self.plan_id} name={self.name}"
                    

class PlanType(db.Model):
    """Type of Plan""" 

    __tablename__ = "plan_types"

    plan_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name_type = db.Column(db.String(10), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.plan_id'), index=True)

    # Define relationship to plan
    plan = db.relationship("Plan", 
                           backref=db.backref("plan_types", 
                           order_by=plan_type_id))


def connect_to_db(app):

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///healthcare'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Work directly with database when running module interactively
     
    from server import app

    connect_to_db(app)
    print("Connected to DB.")
