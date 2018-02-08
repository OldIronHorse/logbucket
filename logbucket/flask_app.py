from flask import Flask, g, render_template, redirect
from pymongo import MongoClient
from logbucket import config

app = Flask(__name__)
app.config.from_object(__name__)

#TODO: common config scheme?
app.config.update(dict(
  SECRET_KEY='develeopment key',
  DB_CONNECTION_STRING=config.DATABASE['connection_string']))

def connect_db():
  db_client = MongoClient(app.config['DB_CONNECTION_STRING'])
  return db_client.logbucket

def get_db():
  if not hasattr(g, 'logbucket_db'):
    g.logbucket_db = connect_db()
  return g.logbucket_db

@app.route('/')
def root_page():
  return redirect('/domains')

@app.route('/domains')
def show_domains():
  return render_template('domains.html', domains=get_db().collection_names())

@app.route('/domains/<domain>')
def show_domain(domain):
  events = get_db()[domain].find()
  return render_template('domain.html', domain=domain, events=events)
