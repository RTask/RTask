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
from models.message import Message
from DTO.ticket_info_dto import TicketInfo
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
    userId = session['profile']['user_id'] # move this to ticket count func
    ticketCount = getTicketCount(userId)
    ticketInfoDto = TicketInfo(ticketCount)
    message_count = getNewMessageCount()
    
    return render_template('/dashboard/index.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'],indent=4),
                           ticketInfoDto=ticketInfoDto,
                           message_count=message_count)

@app.route('/logout', methods=['GET'])
def logout():
    # Clear flask session stored data
    session.clear()
    
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('hello', _external=True), 'client_id': 'Zt9tC9dhE4oGIqS5JDyUbbVg6ykZ0zVY'}
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

# begin messages endpoints
@app.route('/dashboard/messages')
@requires_auth
def messages():
    messages = getMessages()
    return render_template('/dashboard/messages/index.html', messages=messages)

@app.route('/dashboard/messages/new', methods=['GET', 'POST'])
@requires_auth
def message_new():
    if request.method == 'POST':
        message = getMessageFromForm(request)
        g.db.add(message)
        g.db.commit()
        flash('message sent')
    
    return render_template('/dashboard/messages/new.html')
    
# end messages endpoints

# begin endpoints for orders
def get_orders():
    return render_template('/dashbaord/orders/index.html')
# end enpoints for orders

# begin endpoints for tasks

# end endpoints for tasks

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
    return tickets

def getTicketCount(userId):
    count = g.db.query(Ticket).filter(Ticket.userId == userId).count()
    return count

def getMessages():
    userId = session['profile']['user_id']
    messages = g.db.query(Message).filter(Message.userId == userId)
    return messages
    
def getNewMessageCount():
    userId = session['profile']['user_id']
    count = g.db.query(Message).filter(Message.userId == userId).count()
    return count

def getMessageFromForm(request):
    title = request.form['title']
    description = request.form['description']
    sentBy = session['profile']['user_id'] # user who created message is the one sending
    sentTo = request.form['sendTo']
    userId = session['profile']['user_id']

    message = Message(title, description, userId, sentBy, sentTo)
    return message

if __name__ == '__main__':
    app.run(debug=True)