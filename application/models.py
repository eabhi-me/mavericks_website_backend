from application import app, db
from application import bcrypt
from flask_bcrypt import generate_password_hash
# creating the user table
class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email_address = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable = False)

    # adding th eopt verificton model
    otp = db.Column(db.String(6), nullable=True)  # Store OTP
    is_verified = db.Column(db.Boolean, default=False)  # Verification status

    # adding the getter and setter for hased password
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
# creating the member table
class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batch = db.Column(db.String(20), nullable=True)
    photo = db.Column(db.String(200), nullable=True)  # URL or path to the photo
    branch = db.Column(db.String(50), nullable=True)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    linkedin_url = db.Column(db.String(200), nullable=True)
    email_address = db.Column(db.String(100), nullable=True)
    curr_status = db.Column(db.String(100), nullable=True)
# Insert dummy data into the database
with app.app_context():
    db.create_all()
    
    if not User.query.first():
        master_user = [
            User(username = 'admin', email_address = 'admin@gmail.com', password_hash = generate_password_hash('Master_User1_Password'), is_verified=True),
            User(username = 'inovaix', email_address = 'inovaix@gmail.com', password_hash = generate_password_hash('Master_User2_Password'), is_verified=True)
        ]
        db.session.bulk_save_objects(master_user)
        db.session.commit()

        db.session.close()