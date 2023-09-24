from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__ , static_url_path='/static')

# Set a secret key for securing your application
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random secret key

# Configure the database URI. Here, we're using SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Set up the LoginManager for handling user authentication
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Define the User model with id, username, and password columns
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


# User loader function for Flask-Login to get a user by their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home page route
@app.route('/')
def index():
    return redirect(url_for('login'))


# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Create a new user and add to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to login page after successful registration
        return redirect(url_for('login'))
    
    # Render the registration form template for GET request
    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)  # Log in the user
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
    
    # Render the login form template for GET request
    return render_template('login.html')


# Dashboard route (requires authentication)
@app.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username 
    return render_template('dashboard.html', username=username)


# Logout route (requires authentication)
@app.route('/logout')
@login_required
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('login'))  # Redirect to login page after logout


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
