from market import app,db
from flask import render_template, redirect, url_for,flash,get_flashed_messages,request
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market.models import Item,User
from flask_login import login_user, logout_user, login_required,current_user
@app.route('/')
@app.route('/home') 
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    if request.method=="POST":
        purchased_item= request.form.get('purchased_item')
        p_item_object=Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.check_budget(p_item_object):
                p_item_object.buy(current_user)
            else:
                flash(f'Unfortunately you dont have balance for {p_item_object.name}', category='danger')
                return redirect(url_for('market_page'))

        else:
            flash("item doesnt exist")
        return redirect(url_for('market_page'))
    if request.method=="GET":
        items = Item.query.filter(Item.owner.is_(None)).all()
        return render_template('market.html', items=items, purchase_form=purchase_form)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form =RegisterForm()
    if form.validate_on_submit():
            createduser= User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
            db.session.add(createduser)
            db.session.commit()

            login_user(createduser)
            flash(f'Creared Account ! you are signed in as {createduser.username}',category='success' )
            

            return redirect(url_for('market_page'))
    if form.errors!={}:
         for err_msg in form.errors.values():
              flash(f'There was an error: {err_msg}',category='danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success ! you are signed in as {attempted_user.username}',category='success' )
            return  redirect(url_for('market_page'))

        else:
            flash('Please check your username or Password', category='danger')
    return render_template('login.html', form=form)
    


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out !', category='info')
    return redirect(url_for('home_page'))