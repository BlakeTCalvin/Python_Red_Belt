from flask import flash, session
from sqlalchemy.sql import func
from config import db, EMAIL_REGEX, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if len(user_data['first_name']) < 1:
            is_valid = False
            flash("Please provide a first name!")
        if len(user_data['last_name']) < 1:
            is_valid = False
            flash("Please provide a last name!")
        if not EMAIL_REGEX.match(user_data['email']):
            is_valid = False
            flash("Please provide a valid email address!")
        if len(user_data['password']) < 5:
            is_valid = False
            flash("Password must be at least 5 characters!")
        if user_data['password'] != user_data['cpassword']:
            is_valid = False
            flash("Passwords do not match!")
        return is_valid

    @classmethod
    def validate_login(cls, user_data):
        is_valid = True
        hash_password = bcrypt.generate_password_hash(user_data['password'])
        get_user = User.query.filter_by(email=user_data['email']).first()
        if get_user:
            if bcrypt.check_password_hash(get_user.password, user_data['password']):
                return get_user
            else:
                is_valid = False
                flash("Email or Password is Incorrect")
                return is_valid
        else: 
            is_valid = False
            flash("Email or Password is Incorrect")
            return is_valid
    
    @classmethod
    def new_user(cls, user_data):
        hashed_password = bcrypt.generate_password_hash(user_data['password'])
        user_to_add = cls(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'], password=hashed_password)
        db.session.add(user_to_add)
        db.session.commit()
        return user_to_add

class Wish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish = db.Column(db.String(45))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def validate_wish(cls, user_data):
        is_valid = True
        if len(user_data['wish']) < 3:
            is_valid = False
            flash("A wish must consist of at least 3 characters!")
        if len(user_data['description']) < 3:
            is_valid = False
            flash("A description must be provided!")
        return is_valid

    @classmethod
    def new_wish(cls, user_data):
        wish_to_add = cls(wish=user_data['wish'], description=user_data['description'], user_id=session['user_id'])
        db.session.add(wish_to_add)
        db.session.commit()
        return wish_to_add

    @classmethod
    def edit_wish(cls, user_data, wish_id):
        get_wish = Wish.query.get(wish_id)
        get_wish.wish = user_data['wish']
        get_wish.description = user_data['description']
        db.session.commit()
        return get_wish
    
    @classmethod
    def delete_wish(cls, wish_id):
        get_wish = Wish.query.get(wish_id)
        db.session.delete(get_wish)
        db.session.commit()

class GrantedWish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish = db.Column(db.String(45))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())
    granted_at = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def new_granted_wish(cls, wish_id):
        get_old_wish = Wish.query.get(wish_id)
        wish_to_add = cls(wish=get_old_wish.wish, description=get_old_wish.description, user_id=get_old_wish.user_id, created_at=get_old_wish.created_at, updated_at = get_old_wish.updated_at)
        db.session.add(wish_to_add)
        db.session.commit()
        db.session.delete(get_old_wish)
        db.session.commit()
        return wish_to_add
