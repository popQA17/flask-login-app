

# // TO-DO \\





# 1. Make use of the text-captcha lib
# 2. Create docs on the github repo
# 3. 




# // CONFIG \\




sitename = "your site's name" # what your site's name is called
about_us = "your site's info" # what your site is about. Shows in /about
announcement = "your site's announcement" # the announcement posted on your site's homepage
discord = "your discord server invite" # WIP, is not implemented yet.
admin1 = "admin1's username" # Access to admin portal
admin2 = "admin2's username"
admin3 = "admin3's username"
maintainance_key = "p0pP147s" # Key required to lock the website while you maintain the website temporarily. Admins will still have access to the website.











# // SOURCE CODE \\
# Do not touch unless you know what you are doing!





















import os
from replit import db
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import requests
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
users = []
app = Flask('')
app.secret_key = 'AKEYTHAT0NLYISH0ULDKN0W'


@app.errorhandler(404)
def page_not_found(e):
  return render_template('erro404.html'), 404

        



@app.route('/profile' , methods=['GET','POST'])
def profile():
    userse = [x for x in users if x.username == session['username']][0]
    g.user = userse
    try:
          if request.method == "POST":
              password = request.form['password']
              db[g.user.username] = password
              users.append(User(username=g.user.username, password=password))
              return redirect(url_for("profile"))
          if g.user.username == admin1 or g.user.username==admin2 or g.user.username==admin3:
            isadmin = True
            print("is admin")
            return render_template('profile.html',isadmin=isadmin, passwordt=db[g.user.username], site=sitename, discord=discord)
          else:
            print("is not admin")
            isadmin = False
            return render_template("profile.html", passwordt=db[g.user.username], site=sitename, discord=discord)
    except:
        return render_template("profile.html")
@app.route('/', methods=['GET', 'POST'])
def home():
    g.user = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
          matches = db.prefix(username)
          value = db[username]
        except:
          return render_template('invaliduser.html', site=sitename)
        passwordval = db[username]
        if passwordval == password:
          if username == admin1 or username ==  admin2 or username==admin3:
            print("an admin logged onto our site!")
          else:
            print("a regular user is logged in")
          session['username'] = username
          users.append(User(username=username, password=passwordval))
          return redirect(url_for('profile'))
        else:
          return render_template('invaliduser.html', site=sitename, announce=announcement)
    try:
      userse = [x for x in users if x.username == session['username']][0]
      islogin = True
      return render_template("index.html", islogin=islogin, site=sitename, announce=announcement, discord=discord)
    except:
      islogin = False
      return render_template("index.html", islogin=islogin, site=sitename, announce=announcement, discord=discord)

@app.route('/applications')
def apps():
      try:
        userse = [x for x in users if x.username == session['username']][0]
        islogin = "Yes"
        g.user = userse
        try:
          if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3 :
            isadmin = True
            return render_template('applications.html', islogin=islogin,isadmin=isadmin, site=sitename)
          else:
            isadmin = False
            print("not an admin")
            return render_template("applications.html", islogin=islogin, isadmin=isadmin, site=sitename)
        except:
          return render_template("erro403.html", islogin=islogin, site = sitename)
      except:
        return render_template("erro403.html")
  
@app.route('/about')
def about():
      try:
        userse = [x for x in users if x.username == session['username']][0]
        islogin = True
        g.user = userse
        try:
          if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3:
            isadmin = True
            print("is an admin")
            return render_template('about.html', islogin=islogin,isadmin=isadmin, site=sitename, about=about_us)
          else:
            print("aren't an admin?")
            isadmin = False
            return render_template("about.html", islogin = islogin, isadmin=isadmin, site=sitename, about = about_us)
        except:
          return render_template("about.html", islogin=islogin, site=sitename, about=about_us)
      except:
        return render_template("about.html", site=sitename, about=about_us)
@app.route('/register', methods=['GET', 'POST'])
def reg():
 if request.method == 'POST':
  username = request.form['username']
  password = request.form['password']
  try:
    matches = db.prefix(username)
    value = db[username]
    return render_template("alruser.html", site=sitename)
  except:
    db[username] = password
    session["username"] = username
    users.append(User(username=username, password=password))
    return redirect(url_for("profile"))
 return render_template("register.html", site=sitename)
@app.route('/logout', methods=['GET', 'POST'])
def logout():
 session.pop('username',None)
 session.pop('admin',None)
 print("Logout successful.")
 return render_template("loggedout.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    g.user = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:

          matches = db.prefix(username)
          value = db[username]
        except:
          return render_template('invaliduser.html', site=sitename)
        passwordval = db[username]
        if passwordval == password:
          session['username'] = username
          if username == admin1 or username == admin2:
            session['admin'] = "Yes"
            print("an admin logged onto our site!")
          else:
            print("a regular user is logged in")
          users.append(User(username=username, password=passwordval))
          return redirect(url_for('profile'))
          return render_template('login.html', site=sitename)
        else:
          return render_template('invaliduser.html')
    return render_template('login.html')

@app.route("/deluseradmin", methods=['GET','POST'])
def admin():
 userse = [x for x in users if x.username == session['username']][0]
 g.user = userse
 try:
  if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3:
    keys = db.keys()
    if request.method == "POST":
      deluser = request.form["killusername"]
      try:
        value = db[deluser]
      except:
        return render_template('invaliduser.html')
      del db[deluser]
      return redirect(url_for('admin'))
  else:
    return render_template('erro403.html')
 except:
   return render_template('erro403.html')
 return render_template('deluser.html', keys=keys)

@app.route("/admin")
def adminpage():
 userse = [x for x in users if x.username == session['username']][0]
 g.user = userse
 try:
  if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3:
    return render_template("admin.html")
 except:
   return render_template('erro403.html')
 return render_template('admin.html')

@app.route("/admincheckpw", methods=['GET','POST'])
def checkpw():
 userse = [x for x in users if x.username == session['username']][0]
 g.user = userse
 try:
  if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3:
    keys = db.keys()
    if request.method == "POST":
      deluser = request.form["killusername"]
      try:
        value = db[deluser]
      except:
        return render_template('invaliduser.html')
      value = db[deluser]
      return render_template("checkedpw.html", pw=value, user=deluser)
  else:
    return render_template('erro403.html')
 except:
   return render_template('erro403.html')
 return render_template('checkpw.html', keys=keys)
@app.route("/adduseradmin", methods=['GET','POST'])
def addusr():
 userse = [x for x in users if x.username == session['username']][0]
 g.user = userse
 try:
  if g.user.username == admin1 or g.user.username == admin2 or g.user.username == admin3:
    keys = db.keys()
    if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      db[username] = password
      return redirect(url_for('addusr'))
  else:
    return render_template('erro403.html')
 except:
   return render_template('erro403.html')
 return render_template('adduser.html', keys=keys)
@app.route("/delacc")
def del_account():
 try:
  userse = [x for x in users if x.username == session['username']][0]
  g.user = userse
  del db[g.user.username]
  return redirect(url_for("logout"))
  
 except:
  return redirect(url_for("home"))
@app.route('/registered')
def registered():
  session['username'] = None
  return render_template("registered.html")

app.run(host="0.0.0.0")
