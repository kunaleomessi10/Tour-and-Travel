from flask import Flask, render_template, request, redirect, url_for, session, abort
from functools import wraps
from database import *

app = Flask(__name__)

app.secret_key = 'your secret key'

# error
app.config['MYSQL_HOST'] = 'localhost'

app.config["SESSION_PERMANENT"] = False
app.static_folder = 'static'


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is not None and session.get('is_admin') == True:
            return f(*args, **kwargs)
        else:
            return abort(404, 'Only Allowed to admin')

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def not_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is not None:
            return redirect(url_for('logout', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/register', methods=['GET', 'POST'])
@not_login_required
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            phone = request.form['phone']
            gender = request.form['gender']
            dob = request.form['dob']
            passport_no = request.form['passport_no']
            address = request.form['address']
            user_name = request.form['username']
            password = request.form['password']
            email = request.form['email']
            postal_code = request.form['postal_code']
            msg = add_customer(name=name, phone=phone, gender=gender, dob=dob, passport_no=passport_no,
                               address=address, user_name=user_name, password=password, email=email,
                               postal_code=postal_code)
            return redirect(url_for('login'))
        except:
            msg = 'Invalid value in form, Please check again'
        return render_template('customer.html', msg=msg)
    else:
        msg = 'Please Fill the form'
    return render_template('customer.html', msg=msg)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_name = request.form['username']
        password = request.form['password']
        result, msg = check_user(user_name=user_name, password=password)
        if result:
            session['loggedin'] = True
            session['id'] = result[0]
            session['username'] = result[-2]
            session['email'] = result[4]
            if result[-2] == 'admin':
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            return redirect(url_for('booking'))
        else:
            msg = 'Incorrect username / password !'
    else:
        msg = 'Please Fill the form'
    return render_template('login.html', msg=msg, session=session)


@app.route('/logout')
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session['is_admin'] = False
    session['id'] = None
    return redirect(url_for('login'))


@app.route('/booking', methods=['POST', 'GET'])
@login_required
def booking():
    header = f"Hi {session['username']}"
    package_list = get_package()
    if request.method == 'POST':
        booking_date = request.form['booking_date']
        package_name = request.form['package_name']
        members = request.form['members']
        total_amount = request.form['total_amount']
        booking_status = request.form.get('booking_status', False)
        if booking_status:
            booking_status = 'Booked'
        else:
            booking_status = 'Pending'
        msg = add_booking(customer_id=session['id'], booking_date=booking_date, package_name=package_name,
                          booking_status=booking_status, total_amount=total_amount, members=members)
        return render_template('Payment.html', header=header, len_=len(package_list), package_list=package_list,
                               msg=msg,
                               session=session)
    else:
        msg = 'Fill the below form'
    return render_template('Booking.html', header=header, msg=msg, len_=len(package_list),
                           package_list=package_list, session=session)


@app.route('/package', methods=['POST', 'GET'])
@is_admin
def package():
    header = f"Hi {session['username']}"
    agency_list = get_agency()
    transportation_list = get_transportation()
    class_list = get_travel_class()
    if request.method == 'POST':
        agency_id = get_agency_id(request.form['agency_id'])
        travel_class_id = get_class_id(request.form['travel_class_id'])
        transportation_type_id = get_transportation_id(request.form['transportation_type_id'])
        from_city = request.form['from_city']
        to_city = request.form['to_city']
        package_days = request.form['package_days']
        package_amount = request.form['package_amount']
        description = request.form['description']
        msg = add_package(agency_id=agency_id, travel_class_id=travel_class_id,
                          transportation_type_id=transportation_type_id,
                          from_city=from_city,
                          to_city=to_city, package_days=package_days, package_amount=package_amount,
                          description=description)
    else:
        msg = 'Fill the below form'
    return render_template('Package.html', header=header, msg=msg, len_=len(agency_list), agency_list=agency_list,
                           transport_len=len(transportation_list), transportation_list=transportation_list,
                           class_len=len(class_list), class_list=class_list, session=session)


@app.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    header = f"Hi {session['username']}"
    package_list = get_package()
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_id = get_customer_id(customer_name)
        if customer_id is None or len(customer_id) == 0:
            msg = f'Customer with {customer_name} is not rpresent'
        else:
            customer_id = customer_id[0]
            booking_id = request.form['booking_id']
            payment_date = request.form['payment_date']
            payable_amount = request.form['payable_amount']
            payment_method = request.form['payment_method']
            payment_status = request.form['payment_status']
            change_booking_status(int(booking_id),payment_status)
            msg = add_payment(customer_id=customer_id, booking_id=booking_id,
                              payment_date=payment_date,
                              payable_amount=payable_amount,
                              payment_method=payment_method, payment_status=payment_status)
    else:
        msg = 'Fill the below form'
    return render_template('Payment.html', header=header, len_=len(package_list), package_list=package_list, msg=msg,
                           session=session)


@app.route('/transportation', methods=['POST', 'GET'])
@is_admin
def transportation():
    header = f"Hi {session['username']}"
    if request.method == 'POST':
        transportation_type_name = request.form['transportation_type_name']
        description = request.form['description']
        msg = add_transportation(transportation_type_name=transportation_type_name, description=description)
    else:
        msg = 'Fill the below form'
    return render_template('Transportation.html', header=header, msg=msg, session=session)


@app.route('/travel_agency', methods=['POST', 'GET'])
@is_admin
def travel_agency():
    header = f"Hi {session['username']}"
    if request.method == 'POST':
        agency_name = request.form['agency_name']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']
        address = request.form['address']
        postal_code = request.form['postal_code']
        msg = add_travel_agency(customer_id=session['id'], agency_name=agency_name, phone=mobile_no,
                                email=email,
                                city=city,
                                country=country, address=address, postal_code=postal_code)
    else:
        msg = 'Please Fill the form'
    return render_template('TravelAgency.html', header=header, msg=msg, session=session)


@app.route('/travel_class', methods=['POST', 'GET'])
@is_admin
def travel_class():
    header = f"Hi {session['username']}"
    if request.method == 'POST':
        class_name = request.form['class_name']
        description = request.form['description']
        msg = add_travel_class(class_name=class_name, description=description)
    else:
        msg = 'Please Fill the form'
    return render_template('TravelClass.html', header=header, msg=msg, session=session)


@app.route('/past_booking', methods=['GET', 'POST'])
@login_required
def past_booking():
    if request.method == 'POST':
        if request.form.get("accept"):
            change_booking_status(int(request.form.get("accept")), 'Booked')
        if request.form.get('reject'):
            change_booking_status(int(request.form.get("reject")), 'Rejected')
    header = f"Hi {session['username']}, Below is your previous booking"
    if session['username'] == 'admin':
        items = get_all_booking()
    else:
        items = get_past_booking(customer_id=session['id'])
    for i in range(len(items)):
        items[i] = list(items[i])
        items[i][3] = str(items[i][3])

    table_header = ['Index', "booking_id", "customer_id", "booking_date", "package_name", "members", "total_amount",
                    "booking_status"]
    return render_template('bookinghistory.html', header=header,
                           table_header=table_header, table_header_len_=len(table_header),
                           items_len_=len(items), items=items, session=session)


if __name__ == "__main__":
    app.run(debug=True)
