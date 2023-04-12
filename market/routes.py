from market import app
from flask import render_template,url_for,redirect,flash,request
from market.models import Itm,User
from market.forms import Registerform,loginform,PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user
from flask import Flask, request
import pandas as pd
import keras
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences




#Decorators
@app.route('/')

@app.route('/home')
def home_page():
    return render_template("home.html")





@app.route('/market', methods=['GET', 'POST'])

@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #purchase item form
        purchased_item = request.form.get('purchased_item')
        p_item_object = Itm.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
       
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Itm.query.filter_by(owner=None)
        owned_items = Itm.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)


@app.route('/register',methods=['GET','POST'])
def Register_page():
#now will create instance from registerform class
    form=Registerform()
    if form.validate_on_submit():
        #this username =form.username which is recive vlaue from user field
        user_to_create=User(username=form.username.data,
                            email=form.email.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg}',category='danger')

    return render_template('register.html',form=form)

@app.route('/logot')
def logout_page():
    logout_user()
    flash('you have been logged out',category='info')
    return redirect (url_for('home_page'))


@app.route('/login',methods=['GET','POST'])
def login_page():
    form=loginform()
    if form.validate_on_submit():
        attemped_user=User.query.filter_by(username=form.username.data).first()
        if attemped_user and attemped_user.check_password_correction(attemped_password=form.password.data):
            login_user(attemped_user)
            flash(f'Success! you are logged in as:{attemped_user.username}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash("username and password are not match!please try again",category='danger')


    return render_template('login.html',form=form)



    
    

tweet= pd.read_csv('C:\\Users\\KIIT\\Desktop\\FlaskMarket\\market\\Clean_data.csv')
model = keras.models.load_model('C:\\Users\\KIIT\\Desktop\\FlaskMarket\\market\\Disasater predictor.h5')

tokenizer = Tokenizer(num_words=5000, lower=True)
tokenizer.fit_on_texts(tweet['text'])
dict_size = len(tokenizer.word_index) + 1

@app.route('/predict', methods=['POST'])
def predict_disaster():
    tweet = request.form['tweet']
    sequence = tokenizer.texts_to_sequences([tweet])
    pad_seq = pad_sequences(sequence, maxlen=200, padding='pre')
    output = model.predict(pad_seq)[0][0]
    if output > 0.5:
        result = "True, it's a true news after disaster"
    else:
        result = "This is a False news"
    return render_template('predict_result.html', result=result)



@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')



