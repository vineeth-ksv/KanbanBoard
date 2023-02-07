from flask import request, redirect, url_for, session
from flask import render_template
from flask import current_app as app
from flask import flash
import json
from application.models import *
from datetime import date
import datetime

def check_deadline(deadline_date, completed_status):
    if completed_status:
        return "finished"

    today = date.today()
    if(int((deadline_date - today).total_seconds()) <= 0):
        return "unfinished"

class NoCardsInListException(Exception):
    "raised when there are no cards in the list during transfering all cards operation"
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        session.pop('user', None)

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()
        
        if user == None:
            flash("Incorrect username or user doesn't exist..!", "warning")
            return redirect(url_for('index'))
        
        else:
            if user.password == password:
                session['user'] = username
                session['user_id'] = user.user_id
                return redirect(url_for('home'))
            else:
                flash("Invalid password..!", "danger")
                return redirect(url_for('index'))

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("index.html")
    
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
        
        except Exception as e:
            flash("Sorry. Couldn't register the user. Please try again later..", "warning")
            db.session.rollback()
            return redirect(url_for('register'))
        
        else:
            flash("Successfully registered. Welcome, {}".format(username), "success")
            user = User.query.filter_by(username = username).first()
            session['user'] = username
            session['user_id'] = user.user_id
            return redirect(url_for("home"))

@app.route("/home")
def home():
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    user = User.query.filter_by(user_id = session['user_id']).first()
    lists = user.lists
    list_ids = []
    card_ids = []
    deadline_color = {}
    cards_dict = {}
    card_flags = {}
    for list in lists:
        list_ids.append(list.list_id)
        cards = list.cards
        for card in cards:
            card_ids.append(card.card_id)
            deadline_color[card.card_id] = check_deadline(card.deadline, card.completed_status)

            if(card.completed_status):
                completed_Flag = True
            else:
                completed_Flag = False

            deadline_flag = False

            if not completed_Flag:
                if int((card.deadline - date.today()).total_seconds()) < 0:
                    deadline_flag = True
            card_flags[card.card_id] = { "completed_flag": completed_Flag, "deadline_flag": deadline_flag }
        if cards != []:
            cards_dict[list.list_id] = cards
    return render_template('home.html', lists = lists, cards_dict = cards_dict, list_ids = list_ids, 
                                        card_ids = card_ids, deadline_color = deadline_color, card_flags = card_flags, page='home')

@app.route('/add_list', methods=['POST'])
def add_list():
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        list_title = request.form['list_title']
        list_description = request.form['list_description']

        try:
            new_list = Lists(user_id = session['user_id'], list_title = list_title, list_description = list_description)
            db.session.add(new_list)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('List created successfully..', 'success')
        
        finally:
            return redirect(url_for('home'))

@app.route('/edit_list/<list_id>', methods=['POST'])
def edit_list(list_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        updated_list_title = request.form['list_title']
        updated_list_description = request.form['list_description']
        
        try:
            list = Lists.query.filter_by(list_id = list_id).first()
            if list is None:
                raise Exception("List Not Found...")
            list.list_title = updated_list_title
            list.list_description = updated_list_description
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('List updated successfully..', 'success')
        
        finally:
            return redirect(url_for('home'))

@app.route('/delete_list/<list_id>')
def delete_list(list_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    if request.method == "GET":
        try:
            list = Lists.query.filter_by(list_id = list_id).first()
            if list is None:
                raise Exception("List Not Found...")
            db.session.delete(list)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('List deleted successfully..', 'success')

        finally:
            return redirect(url_for('home'))

@app.route('/transfer_list_cards/<list_id>', methods=['POST'])
def transfer_list_cards(list_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        updated_list_id = request.form['list_id']
        try:
            cards = Cards.query.filter_by(list_id = list_id).all()
            if cards == []:
                raise NoCardsInListException
            for card in cards:
                card.list_id = updated_list_id
            
            db.session.commit()
        
        except NoCardsInListException as ncle:
            db.session.rollback()
            flash('There are no cards in the list to transfer...', 'warning')

        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('All Cards transfered to another list successfully..', 'success')
        
        finally:
            return redirect(url_for('home'))


@app.route('/add_card/<list_id>', methods=['POST'])
def add_card(list_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        card_title = request.form['card_title']
        card_content = request.form['card_content']
        input_deadline = request.form.get('deadline')
        deadline = (datetime.datetime.strptime(input_deadline, '%Y-%m-%d')).date()
        created_date = date.today()

        try:
            card = Cards(list_id = list_id, card_title = card_title, card_content = card_content, 
                            deadline = deadline, created_date = created_date, updated_date = created_date)
            db.session.add(card)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('Card created successfully..', 'success')

        finally:
            return redirect(url_for('home'))

@app.route('/edit_card/<list_id>/<card_id>', methods=['POST'])
def edit_card(list_id, card_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        try:
            user_card = Cards.query.filter_by(card_id = card_id).first()
            
            if user_card is None:
                raise Exception("Card Not Found...")

            user_card.list_id = request.form['list_id']
            user_card.card_title = request.form['card_title']
            user_card.card_content = request.form['card_content']
            input_deadline = request.form['deadline']
            user_card.deadline = (datetime.datetime.strptime(input_deadline, '%Y-%m-%d')).date()
            user_card.updated_date = date.today()
            if(request.form.get('completed_status')):
                user_card.completed_status = True
                user_card.completed_date = date.today()
            else:
                user_card.completed_status = False
            
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('Card updated successfully..', 'success')

        finally:
            return redirect(url_for('home'))

@app.route('/delete_card/<card_id>')
def delete_card(card_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))
    
    if request.method == "GET":
        try:
            card = Cards.query.filter_by(card_id = card_id).first()

            if card == None:
                raise Exception('Card Not Found...')
            db.session.delete(card)
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('Card deleted successfully..', 'success')

        finally:
            return redirect(url_for('home'))

@app.route('/transfer_card/<card_id>', methods=['POST'])
def transfer_card(card_id):
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return 'oops..! error occurred'
    
    elif request.method == 'POST':
        updated_list_id = request.form['list_id']
        try:
            card = Cards.query.filter_by(card_id = card_id).first()

            if card == None:
                raise Exception('Card Not Found')

            card.list_id = updated_list_id
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            flash('Oops..! Something went wrong.', 'danger')
        
        else:
            flash('Card transfered successfully..', 'success')

        finally:
            return redirect(url_for('home'))

@app.route('/summary')
def summary():
    if 'user' not in session:
        flash('Session expired. Please login again..', "warning")
        return redirect(url_for('login'))

    if request.method == 'GET':
        user = User.query.filter_by(user_id = session['user_id']).first()
        (labels, data1, data0) = ([], [], [])
        for list in user.lists:
            labels.append(list.list_title)
            temp1 = 0
            temp0 = 0
            for card in list.cards:
                if card.completed_status == True:
                    temp1 += 1
                else:
                    temp0 += 1
            data1.append(temp1)
            data0.append(temp0)
        return render_template('summary.html', user = user, labels = json.dumps(labels), data1 = json.dumps(data1), data0 = json.dumps(data0), page='summary')        

@app.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash("User logged out successfully..!", "success")
    return redirect(url_for("index")) 

@app.route("/error")
def error():
    return "Error Occurred...!"

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0"
    return response

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not logged in!'
 
@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    session.pop('user_id', None)
    return 'Dropped!'