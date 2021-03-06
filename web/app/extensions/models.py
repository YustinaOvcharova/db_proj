from . import db
from hashlib import sha512


class User(db.Model):
    """
    model which declares table of accounts which may work with a service
    user_id - key
    login - username to authenticate
    password - sha512 hash of user's password
    role_id - foreign key which points to roles.role_id
    """
    __tablename__ = 'users'

    user_id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.ForeignKey('roles.role_id'))
    role = db.relationship('Role')

    def set_password(self, new_pass: str):
        """
        set new password on user object
        requires db.session.commit() to apply changes to the database
        :param new_pass: password to set
        :return: None
        """
        self.password = sha512(new_pass.encode()).hexdigest()

    def check_password(self, password):
        """
        Compare given password hashes with existing
        :param password: password to compare with original
        :return: boolean result of hash comparsion
        """
        return self.password == sha512(password.encode()).hexdigest()


class PersonalDataObject(db.Model):
    """
    model which declared personal data structure
    """
    __tablename__ = 'personal_data'

    pd_id = db.Column(db.Integer(), primary_key=True)
    person_name = db.Column(db.String(20), nullable=False)
    person_surname = db.Column(db.String(20), nullable=False)
    person_patronymic = db.Column(db.String(20), nullable=False)
    person_date_of_birth = db.Column(db.DateTime(), nullable=False)
    person_photo = db.Column(db.LargeBinary())
    person_json = db.Column(db.JSON())

    @property
    def full_name(self):
        """
        property to get full name
        :return: full name in format <Surname> <Name> <Patronymic>  
        """
        return ' '.join([self.person_surname, self.person_name, self.person_patronymic])


class Role(db.Model):
    """
    model which declares roles and their rights
    """
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(20), unique=True, nullable=False)
    role_right_1 = db.Column(db.Boolean())
    role_right_2 = db.Column(db.Boolean())


class ExtensionType(db.Model):
    __tablename__ = 'extensionsTypes'
    type_id = db.Column(db.Integer(), primary_key=True)
    type_name = db.Column(db.String(40), nullable=False)
    type_shortened = db.Column(db.String(5), nullable=False, unique=True)
    type_description = db.Column(db.String(100), nullable=False)


class PersonalDataExtension(db.Model):
    __tablename__ = 'extensionSchema'
    extension_id = db.Column(db.Integer(), primary_key=True)
    extension_type_id = db.Column(db.ForeignKey('extensionsTypes.type_id'), nullable=False)
    extensions_name = db.Column(db.String(40), unique=True, nullable=False)
