from functools import wraps
import json
import config
from os import environ as environ
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request
from flask import flash
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from models.ticket import Ticket
from forms.ticket_form import TicketForm
from flask import g
import os.path
from os import path
from db import db_session, init_db
from models.ticket import Ticket

app = Flask(__name__)
app.secret_key = 'SlumDog'
oauth = OAuth(app)

# move to config file
auth0 = oauth.register(
    'auth0',
    client_id=config.clientId,
    client_secret= config.secret,
    api_base_url='https://rtask.auth0.com',
    access_token_url='https://rtask.auth0.com/oauth/token',
    authorize_url='https://rtask.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# check if database/tables exist
init_db()

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/profile')
@requires_auth
def profile():
    return render_template('/dashboard/profile/index.html', userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@app.route('/setup')
def setup():
    return render_template('/setup/index.html')

@app.route('/')
def hello():
    name = 'michael'
    return render_template('home.html', name=name)

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('/dashboard/index.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@app.route('/logout')
def logout():
    # Clear session stored data
    db_session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'Zt9tC9dhE4oGIqS5JDyUbbVg6ykZ0zVY'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/dashboard/tickets/new', methods=['GET', 'POST'])
@requires_auth
def ticket():

    ticket = Ticket()
    success = False
    form = TicketForm(request.form, obj=ticket)

    if request.method == 'GET':
        form = TicketForm(obj=ticket)
        return render_template('/dashboard/tickets/new.html', form=form, success=success)
    
    ticket.title = request.form['title']
    ticket.description = request.form['description']
    ticket.userId = session['profile']['user_id']
    
    g.db.add(ticket)
    g.db.commit()
    success = True

    flash('ticket created successfully!')
    return redirect(url_for('ticket_list'))

@app.route('/dashboard/tickets', methods=['GET'])
@requires_auth
def ticket_list():
    # bind to userid to get unique tickets
    userId = session['profile']['user_id']

    # get list of tickets
    tickets = getTickets(userId)
    return render_template('/dashboard/tickets/index.html', tickets=tickets)

@app.route('/dashboard/tickets/<int:ticket_id>', methods=['GET'])  
def get_ticket(ticket_id):
    ticket = g.db.query(Ticket).get(ticket_id)
    return render_template('/dashboard/tickets/view.html', ticket=ticket)

@app.route('/dashboard/tickets/edit/<int:ticket_id>', methods=['POST'])
@requires_auth
def update_ticket(ticket_id):
    ticket = g.db.query(Ticket).get(ticket_id)
    
    # get username and assign on ticket
    userId = session['profile']['user_id']
    
    if ticket:
        ticket.title = request.form['title']
        ticket.description = request.form['description']
        ticket.userId = userId
        g.db.commit()
        success = True
        flash('ticket updated successfully!')
    else:
        flash('error updating ticket')

    return render_template('/dashboard/tickets/edit.html', ticket=ticket)

@app.route('/dashboard/tickets/edit/<int:ticket_id>', methods=['GET'])  
def edit_ticket(ticket_id):
    ticket = g.db.query(Ticket).get(ticket_id)
    return render_template('/dashboard/tickets/edit.html', ticket=ticket)

@app.before_request
def before_req():
    g.db = db_session()

@app.after_request
def after_req(resp):
    try:
        g.db.close()
    except Exception:
        pass
    return resp

def getTickets(userId):
    tickets = g.db.query(Ticket).filter(Ticket.userId == userId)
    for ticket in tickets:
        print(ticket.description)
    return tickets

    
if __name__ == '__main__':
    app.run(debug=True)