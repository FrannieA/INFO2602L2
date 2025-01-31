import click, sys
from models import db, User
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  print(bob)
  db.session.add(bob)
  db.session.commit()
  print('database intialized')


@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)
  
@app.cli.command('add-user')
@click.argument('username')
@click.argument('email')
@click.argument('password')
def add_user(username, email, password):
  try:
    new_user = User(username, email, password)
    db.session.add(new_user)
    db.session.commit()
    print(f'{username} added!')
  except IntegrityError:
    db.session.rollback()
    print(f'Username {username} already exists')

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  user = User.query.filter_by(username=username).first()
  if not user:
      print(f'{username} not found!')
      return
  user.email = email
  db.session.add(user)
  db.session.commit()
  print(user)

@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  msg = ""
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    msg = "Username or email already taken!" #give the user a useful message
  else:
    msg = str(newuser) # print the newly created user
  finally:
    print(msg)