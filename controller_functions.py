from flask import render_template, redirect, request, session, flash
from config import db, bcrypt
from models import User, Wish, GrantedWish
from sqlalchemy import desc

def index():
    return render_template("index.html")

def process_user():
    validation_check = User.validate_user(request.form)
    if not validation_check:
        return redirect("/")
    else:
        new_user = User.new_user(request.form)
        session['user_id'] = new_user.id
        session['first_name'] = new_user.first_name
    return redirect("/wishes")

def process_login():
    if len(request.form['password']) < 1:
        flash("Email or Password is Incorrect")
        return redirect("/")
    else:
        login_check = User.validate_login(request.form)
        if login_check == False:
            return redirect("/")
        else:
            session['user_id'] = login_check.id
            session['first_name'] = login_check.first_name
            return redirect("/wishes")

def wishes():
    if 'first_name' in session:
        wishes = Wish.query.filter_by(user_id=session['user_id']).order_by(desc(Wish.created_at)).all()
        granted_wishes = GrantedWish.query.order_by(desc(GrantedWish.granted_at)).all()
        users = User.query.all()
        return render_template("wishes.html", wishes=wishes, granted_wishes=granted_wishes, users=users)
    else:
        return redirect("/")

def make_wish():
    if 'first_name' in session:     
        return render_template("make_wish.html")
    else: 
        return redirect("/")

def make_new_wish():
    validation_check = Wish.validate_wish(request.form)
    if not validation_check:
        return redirect("/make_wish")
    else:
        new_wish = Wish.new_wish(request.form)
        return redirect("/wishes")

def edit_wish(id):
    if 'first_name' in session:
        return render_template("edit_wish.html", wish_id = id)
    else: 
        return redirect("/")

def process_edited_wish(id):
    validation_check = Wish.validate_wish(request.form)
    if not validation_check:
        return redirect("/edit_wish/" + id)
    else:
        edited_wish = Wish.edit_wish(request.form, id)
        return redirect("/wishes")

def delete_wish(id):
    Wish.delete_wish(id)
    return redirect("/wishes")

def grant_wish(id):
    GrantedWish.new_granted_wish(id)
    return redirect("/wishes")

def logout():
    session.clear()
    return redirect("/")