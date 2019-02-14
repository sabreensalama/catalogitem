from flask import Flask, render_template, redirect,
from flask import url_for, request, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import base, Catalog, CatalogItem,  User
# 2 step in oauth google plus
from flask import session as login_session
# to create pseudo random string that wil identify each session
import random
import string
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# to make object from class Flask
app = Flask(__name__)
engine = create_engine("sqlite:///catalogitem.db")
base.metadata.create_all(engine)
DBsession = sessionmaker(bind=engine)
session = DBsession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ARAGEEK"


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token TO ENSURE tokens from server to client
    # is the same of client to server
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code that sent to the server
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade' /
                                            'the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # send get request with url
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    # authorization he have the right to make access
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # check to see if the user is connected to the system or not
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user ' /
                                            'is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session
    # for later use. if none of the if is true
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # to check if he exit or not if does'nt make new one
    user_id = getUerID(email=login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;""'
    output += ' "style="-webkit-border-radius: 150px;""'
    output += '" style="-moz-border-radius: 150px;">" '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
# make local permision system


def createUser(login_session):
    newuser = User(name=login_session['username'], email=login_session['emai'],
                   picture=login_session['picture'])
    session.add(newuser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUerID(email):
        try:
            user = session.query(User).filter_by(email=email).one()
            return user.id
        except:
            return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not ' /
                                            'connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token' /
                                            ' for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route("/catalog/Json")
def showCatalogjson():
    catalog = session.query(Catalog).all()
    items = session.query(CatalogItem).all()
    return jsonify(categories=[i.serialize for i in catalog],
                   items=[i.serialize for i in items])


@app.route("/")
def showCatalog():
        catalog = session.query(Catalog).all()
        if 'username' not in login_session:
            return render_template('publiccategory.html', catalog=catalog)
        else:
            return render_template('category.html', catalog=catalog)


@app.route("/catalog/new/category", methods=['GET', 'POST'])
def newCategory():
        if 'username' not in login_session:
            return redirect('/login')
        if request.method == 'POST':
            added = Catalog(name=request.form['name'],
                            user_id=login_session['user_id'])
            session.add(added)
            session.commit()
            flash("successful New category was Added")
            return redirect(url_for('showCatalog'))
        else:
            return render_template('addcategory.html')


@app.route("/catalog/<path:catalog_name>/edit/category",
           methods=['GET', 'POST'])
def editCatalog(catalog_name):
        if 'username' not in login_session:
            return redirect('/login')
        editeditem = session.query(Catalog).filter_by(name=catalog_name).one()
        if request.method == 'POST':
            editeditem.name = request.form['name']
            session.add(editeditem)
            session.commit()
            flash("successful !!!Item was edited")
            return redirect(url_for('showCatalog'))
        else:
            return render_template('editcategory.html',
                                   i=editeditem, catalog_name=catalog_name)


@app.route("/catalog/<path:catalog_name>/delete/category",
           methods=['GET', 'POST'])
def deleteCatalog(catalog_name):
    if 'username' not in login_session:
        return redirect('/login')
    deleteditem = session.query(Catalog).filter_by(name=catalog_name).first()
    if request.method == 'POST':
        session.delete(deleteditem)
        session.commit()
        flash("successful an category was deleted!!!!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deletecatalog.html',
                               catalog_name=catalog_name, i=deleteditem)


@app.route("/catalog/<path:catalog_name>/items")
def showItems(catalog_name):
    cata = session.query(Catalog).filter_by(name=catalog_name).one()
    creator = getUserInfo(cata.user_id)
    items = session.query(CatalogItem).filter_by(catalog_id=cata.id).all()
    if 'username' not in login_session or
    creator.id != login_session['user_id']:
            return render_template('publicitems.html', cata=cata, items=items,
                                   catalog_name=catalog_name, creator=creator)
    else:
            return render_template('items.html', cata=cata, items=items,
                                   catalog_name=catalog_name, creator=creator)


@app.route("/catalog/<path:catalog_name>/<path:item_title>/")
def showInfo(catalog_name, item_title):
    items = session.query(CatalogItem).filter_by(title=item_title).one()
    catalog = session.query(Catalog).order_by(Catalog.name)
    if 'username' not in login_session:
        return render_template('publicitem.html', items=items, catalog=catalog)
    else:
        return render_template('item.html', items=items, catalog=catalog)


@app.route("/catalog/<path:catalog_name>/new/item", methods=['GET', 'POST'])
def newItem(catalog_name):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    if request.method == 'POST':
        added = CatalogItem(title=request.form['title'],
                            description=request.form['description'],
                            catalog_id=catalog.id,
                            category=request.form['category'],
                            user_id=catalog.user_id)
        session.add(added)
        session.commit()
        flash("successful!!New Item was Added")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('additem.html', catalog_name=catalog_name,
                               catalog=catalog)


@app.route("/catalog/<path:item_title>/edit", methods=['GET', 'POST'])
def editItem(item_title):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).all()
    editeditem = session.query(CatalogItem).filter_by(title=item_title).one()
    if request.method == 'POST':
        editeditem.title = request.form['title']
        editeditem.description = request.form['description']
        editeditem.category = request.form['category']
        session.add(editeditem)
        session.commit()
        flash("successful !!!Item was edited")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('edititem.html', item_title=item_title,
                               i=editeditem, catalog=catalog)


@app.route("/catalog/<path:item_title>/delete", methods=['GET', 'POST'])
def deleteItem(item_title):
    if 'username' not in login_session:
        return redirect('/login')
    deleteditem = session.query(CatalogItem).filter_by(title=item_title).one()
    if request.method == 'POST':
        session.delete(deleteditem)
        session.commit()
        flash("successful an item was deleted!!!!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteitem.html',
                               item_title=item_title, i=deleteditem)


if __name__ == '__main__':
        app.secret_key = 'super_secret_key'
        app.debug = True
        app.run(host='0.0.0.0', port=8000)
