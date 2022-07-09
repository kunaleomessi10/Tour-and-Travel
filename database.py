import sqlite3
import datetime

mydb = sqlite3.connect('database.sqlite3', check_same_thread=False)
cursor = mydb.cursor()
datetime_format = '%Y-%m-%d'


def add_customer(**kwargs):
    try:
        query = 'INSERT INTO customer (name, phone, email, gender, dob, passport_no, postal_code, address, user_name, password) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?, ?)'
        cursor.execute(query, (
            kwargs.get('name'), int(kwargs.get('phone')), kwargs.get('email'), kwargs.get('gender'),
            datetime.datetime.strptime(kwargs.get('dob'), datetime_format),
            kwargs.get('passport_no'), kwargs.get('postal_code', 123), kwargs.get('address'), kwargs.get('user_name'),
            kwargs.get('password')))
        mydb.commit()
        msg = 'Successfully inserted customer'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting customer'
    return msg


def add_booking(**kwargs):
    try:
        query = "INSERT INTO booking (customer_id, booking_date, package_name,members, total_amount, booking_status ) VALUES (?, ?, ?,?, ?, ?)"
        cursor.execute(query, (
            int(kwargs.get('customer_id')), datetime.datetime.strptime(kwargs.get('booking_date'), datetime_format),
            kwargs.get('package_name'),
            int(kwargs.get('members')), int(kwargs.get('total_amount')), kwargs.get('booking_status')))
        mydb.commit()
        msg = 'Successfully inserted booking'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting booking'
    return msg


def add_package(**kwargs):
    try:
        query = 'INSERT INTO package (agency_id,travel_class_id, transportation_type_id, from_city, to_city, package_days,package_amount, description  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query, (
            int(kwargs.get('agency_id')), int(kwargs.get('travel_class_id')), int(kwargs.get('transportation_type_id')),
            kwargs.get('from_city'), kwargs.get('to_city'), int(kwargs.get('package_days')),
            int(kwargs.get('package_amount')), kwargs.get('description')))
        mydb.commit()
        msg = 'Successfully inserted package'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting package'
    return msg


def add_payment(**kwargs):
    try:
        query = "INSERT INTO payment (customer_id,booking_id, payment_date, payable_amount, payment_method, payment_status) VALUES (?, ?,?, ?, ?, ?)"
        cursor.execute(query, (
            int(kwargs.get('customer_id')), int(kwargs.get('booking_id')),
            datetime.datetime.strptime(kwargs.get('payment_date'), datetime_format),
            int(kwargs.get('payable_amount')),
            kwargs.get('payment_method'),
            kwargs.get('payment_status')))
        mydb.commit()
        msg = 'Successfully inserted payment'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting payment'
    return msg


def add_transportation(**kwargs):
    try:
        query = 'INSERT INTO transportation_type (transportation_type_name,description) VALUES (?, ?)'
        cursor.execute(query, (
            kwargs.get('transportation_type_name'), kwargs.get('description')))
        mydb.commit()
        msg = 'Successfully inserted transportation'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting transportation'
    return msg


def add_travel_agency(**kwargs):
    try:
        query = 'INSERT INTO travel_agency (agency_name,phone, email, city, country, address, postal_code) VALUES (?, ?,  ?, ?, ?, ?, ?)'
        cursor.execute(query, (
            kwargs.get('agency_name'), kwargs.get('phone'), kwargs.get('email'),
            kwargs.get('city'),
            kwargs.get('country'),
            kwargs.get('address'), kwargs.get('postal_code')))
        mydb.commit()
        msg = 'Successfully inserted travel agency'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting travel agency'
    return msg


def add_travel_class(**kwargs):
    try:
        query = 'INSERT INTO travel_class (class_name, description) VALUES (?, ?)'
        cursor.execute(query, (
            kwargs.get('class_name'), kwargs.get('description')))
        mydb.commit()
        msg = 'Successfully inserted travel class'
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while inserting travel class'
    return msg


def get_agency():
    try:
        query = "SELECT agency_name from travel_agency"
        cursor.execute(query)
        result = cursor.fetchall()
        output = []
        for single_res in result:
            output.append(single_res[0])
        return output
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return []


def get_transportation():
    try:
        query = "SELECT transportation_type_name from transportation_type"
        cursor.execute(query)
        result = cursor.fetchall()
        output = []
        for single_res in result:
            output.append(single_res[0])
        return output
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return []


def get_package():
    try:
        query = "SELECT package_id from package"
        cursor.execute(query)
        result = cursor.fetchall()
        output = []
        for single_res in result:
            output.append(single_res[0])
        return output
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return []


def get_travel_class():
    try:
        query = "SELECT class_name from travel_class"
        cursor.execute(query)
        result = cursor.fetchall()
        output = []
        for single_res in result:
            output.append(single_res[0])
        return output
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return []


def get_transportation_id(name):
    try:
        query = 'select transportation_type_id from transportation_type where transportation_type_name=?'
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result[0]
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return None


def get_class_id(name):
    try:
        query = 'select travel_class_id from travel_class where class_name=?'
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result[0]
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return None


def get_customer_id(name):
    try:
        query = 'select customer_id from customer where user_name=?'
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return None


def get_agency_id(name):
    try:
        query = 'select agency_id from travel_agency where agency_name=?'
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        return result[0]
    except Exception as ex:
        print(ex)
        mydb.rollback()
        return None

def get_all_booking():
    try:
        query = 'SELECT booking_id, customer_id, booking_date,package_name, members, total_amount,booking_status  FROM booking'
        cursor.execute(query)
        result = cursor.fetchall()
        msg = 'Fetched customer previous booking'
    except Exception as ex:
        print(ex)
        result = []
        mydb.rollback()
        msg = 'Error raises while fetching booking'
    return result

def get_past_booking(**kwargs):
    try:

        query = 'SELECT booking_id, customer_id, booking_date,package_name, members, total_amount,booking_status  FROM booking WHERE customer_id=?'
        cursor.execute(query, (int(kwargs.get('customer_id')),))
        result = cursor.fetchall()
        msg = 'Fetched customer previous booking'
    except Exception as ex:
        print(ex)
        result = []
        mydb.rollback()
        msg = 'Error raises while fetching booking'
    return result


def check_user(**kwargs):
    try:
        query = 'SELECT * FROM customer WHERE user_name=? and password=?'
        cursor.execute(query, (kwargs.get('user_name'), kwargs.get('password')))
        result = cursor.fetchall()
        # result = mydb.cursor(buffered=True)
        msg = 'Fetched customer'
        if len(result) > 0 and len(result[0]) > 0:
            return result[0], msg
        return [], msg
    except Exception as ex:
        print(ex)
        mydb.rollback()
        msg = 'Error raises while checking user'
    return [], msg

def change_booking_status(booking_id, new_status):
    try:
        query = f"UPDATE booking SET booking_status = '{new_status}' WHERE  booking_id= {booking_id}"
        cursor.execute(query)
        mydb.commit()
    except Exception as ex:
        mydb.rollback()
        raise ex
