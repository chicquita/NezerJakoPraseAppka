from flask import Flask, render_template, request
from models import db, uzivatel
from forms import SignupForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ada:To heslo ti nereknu!@da.stderr.cz/ada'
db.init_app(app)

app.secret_key = "development-key"


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def generic():
  return render_template("generic.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = uzivatel(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      return 'Success!'

  elif request.method == "GET":
    return render_template('signup.html', form=form)

if __name__ == "__main__":
  app.run(debug=True)