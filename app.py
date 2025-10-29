from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key_here"
db = SQLAlchemy(app)

# Database models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    rate = db.Column(db.Integer, nullable=False, default=2500)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        # Example check
        user_exists = False  # Replace this with your real database query
        if not user_exists:
            return redirect(url_for('no_users'))

        return "Logged in successfully!"  # replace with dashboard or similar

    return render_template('login.html', current_year=2025)

@app.route('/no_users')
def no_users():
    return render_template('no_users.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(phone=phone).first():
            return "Phone number already registered!"
        new_user = User(phone=phone, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return redirect(url_for('welcome'))
    return render_template('register.html')


@app.route('/welcome')
def welcome():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html')


@app.route('/cars')
def show_cars():
    all_cars = Car.query.all()
    return render_template('cars.html', cars=all_cars)



@app.route('/selectcar/<int:car_id>', methods=['GET', 'POST'])
def selectcar(car_id):
    car = Car.query.get(car_id)
    if not car:
        return "Car not found", 404
    if request.method == 'POST':
        duration = int(request.form.get('duration', 1))
        payment_method = request.form.get('payment_method')
        total = car.rate * duration
        return render_template('payment.html', car=car, total=total, method=payment_method)
    return render_template('selectcar.html', car=car)

@app.route('/pay/<int:car_id>/<int:total>', methods=['POST'])
def pay(car_id, total):
    if "user_id" not in session:
        return redirect(url_for('login'))

    car = Car.query.get(car_id)
    if not car:
        return "Car not found", 404

    # Simulate payment success (you can integrate Mpesa later)
    receipt = {
        'car_name': car.name,
        'amount': total,
        'status': 'Paid',
    }

    # Get logged-in user's phone number
    user = User.query.get(session['user_id'])
    phone = user.phone

    return render_template('receipt.html', receipt=receipt, phone=phone)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
