import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# importing x-ray libaries
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

app = Flask(__name__)

# X-Ray Configuration
xray_recorder.configure(service='FlaskAppRunnerDemo')
patch_all()  
XRayMiddleware(app, xray_recorder)

# Database Configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', users=User.query.all())


@app.route('/user', methods=['POST'])
def user():
    u = User(request.form['name'], request.form['email'])
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

# Entry Point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
