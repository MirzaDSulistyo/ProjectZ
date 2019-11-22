from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev' :
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/chatbot'
else :
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(200), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(200))

	def __init__(self, name, email, phone):
		self.name = name
		self.email = email

	def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email
        }
		

@app.route("/")
def hello():
    res = jsonify({
        'hello'  : 'world',
        'number' : 3,
        'status' : 200
    })
    res.status_code = 200

    return res

@app.route('/user', methods=['POST'])
def createUser():
	name = request.form['name']
	email = request.form["email"]

	data = User(name,email)
	db.session.add(data)
	db.session.commit()

	return "User : {}, email: {}, phone: {}".format(name,email,phone)

if __name__ == "__main__":
    app.run()