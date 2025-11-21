from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your_secret_key_here"
db = SQLAlchemy(app)

@app.route("/")
def index():
    # Optional: redirect to login or welcome page
    return redirect(url_for("login"))


# -----------------------------
# DATABASE MODELS
# -----------------------------
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

# -----------------------------
# SIGNUP ROUTE
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        if User.query.filter_by(phone=phone).first():
            return render_template(
                "nousers.html",
                message="This phone number is already registered.",
                redirect_url=url_for("login")
            )

        hashed_password = generate_password_hash(password)
        new_user = User(phone=phone, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect(url_for("welcome"))

    return render_template("signup.html")

# -----------------------------
# LOGIN ROUTE (includes Admin)
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        # Admin login
        if phone == "Admin" and password == "Admin@123":
            session['is_admin'] = True
            return redirect(url_for("admin_dashboard"))

        # Normal user login
        user = User.query.filter_by(phone=phone).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for("welcome"))
        else:
            return render_template(
                "nousers.html",
                message="Phone number not registered.",
                redirect_url=url_for("signup")
            )

    return render_template("login.html")

# -----------------------------
# WELCOME ROUTE
# -----------------------------
@app.route('/welcome')
def welcome():
    if "user_id" not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('welcome.html', phone=user.phone)

# -----------------------------
# CARS ROUTE
# -----------------------------
@app.route('/cars')
def show_cars():
    available_cars = Car.query.filter_by(available=True).all()
    return render_template('cars.html', cars=available_cars)

# -----------------------------
# SELECT CAR ROUTE
# -----------------------------
@app.route('/selectcar/<int:car_id>', methods=['GET', 'POST'])
def selectcar(car_id):
    car = Car.query.get(car_id)
    if not car:
        return "Car not found", 404

    if request.method == 'POST':
        duration = int(request.form.get('duration', 1))
        payment_method = request.form.get('payment_method')
        total = car.rate * duration
        user_phone = None
        if "user_id" in session:
            user = User.query.get(session['user_id'])
            user_phone = user.phone if user else None
        return render_template(
            'payment.html',
            car=car,
            total=total,
            duration=duration,
            method=payment_method,
            phone=user_phone
        )

    return render_template('selectcar.html', car=car)

# -----------------------------
# PAYMENT ROUTE
# -----------------------------
@app.route('/pay/<int:car_id>/<int:total>', methods=['POST'])
def pay(car_id, total):
    car = Car.query.get(car_id)
    if not car:
        return "Car not found", 404

    # Mark car as rented
    car.available = False
    db.session.commit()

    # Use phone from form if exists (payment.html)
    phone = request.form.get('phone')
    duration = request.form.get('duration', 'N/A')

    return render_template(
        'receipt.html',
        car=car,
        total=total,
        phone=phone or "Unknown",
        duration=duration
    )

# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    all_cars = Car.query.all()
    return render_template('admin.html', cars=all_cars)

# -----------------------------
# ADMIN LOGOUT
# -----------------------------
@app.route('/logout_admin')
def logout_admin():
    session.pop('is_admin', None)
    return redirect(url_for('login'))

# -----------------------------
# ADD CAR ROUTE (ADMIN ONLY)
# -----------------------------
@app.route('/add_car', methods=['POST'])
def add_car():
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    name = request.form.get('name')
    rate = request.form.get('rate')
    available = request.form.get('available') == "True"
    image = request.files.get('image')

    # Save image to static/images
    if image:
        os.makedirs('static/images', exist_ok=True)
        image_filename = image.filename
        image.save(os.path.join('static/images', image_filename))
    else:
        image_filename = 'default_car.jpg'

    new_car = Car(name=name, rate=rate, image=image_filename, available=available)
    db.session.add(new_car)
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

# -----------------------------
# DELETE CAR (ADMIN ONLY)
# -----------------------------
@app.route('/delete_car/<int:car_id>')
def delete_car(car_id):
    if not session.get('is_admin'):
        return redirect(url_for('login'))

    car = Car.query.get(car_id)
    if car:
        db.session.delete(car)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
