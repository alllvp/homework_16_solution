import datetime
import json

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from lib import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


@app.route("/users", methods=['GET', 'POST'])
def get_all_users():
    """
    all users
    """
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    if request.method == 'POST':
        user = json.loads(request.data)
        db.session.add(User(id=user['id'],
                            first_name=user['first_name'],
                            last_name=user['last_name'],
                            age=user['age'],
                            email=user['email'],
                            role=user['role'],
                            phone=user['phone']
                            )
                       )
        db.session.commit()
        return "All is OK", 200


@app.route("/users/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_user(gid):
    """
    one user by pk
    """
    if request.method == 'GET':
        user = User.query.get(gid)
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        user = db.session.query(User).get(gid)
        user_data = json.loads(request.data)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        return 'All is OK', 200
    if request.method == 'DELETE':
        user = db.session.query(User).get(gid)
        db.session.delete(user)
        db.session.commit()
        return 'All is OK', 200


@app.route("/orders", methods=['GET', 'POST'])
def get_all_orders():
    """
    all orders
    """
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])
    if request.method == 'POST':
        order = json.loads(request.data)
        start_month, start_day, start_year = order['start_date'].split('/')
        end_month, end_day, end_year = order['end_date'].split('/')
        db.session.add(Order(id=order['id'],
                             name=order['name'],
                             description=order['description'],
                             start_date=datetime.date(month=int(start_month), day=int(start_day), year=int(start_year)),
                             end_date=datetime.date(month=int(end_month), day=int(end_day), year=int(end_year)),
                             address=order['address'],
                             price=order['price'],
                             customer_id=order['customer_id'],
                             executor_id=order['executor_id']
                             )
                       )
        db.session.commit()
        return "All is OK", 200


@app.route("/orders/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_order(gid):
    """
    one order by pk
    """
    if request.method == 'GET':
        order = Order.query.get(gid)
        return jsonify(order.to_dict())
    if request.method == 'PUT':
        order = db.session.query(Order).get(gid)
        order_data = json.loads(request.data)
        start_month, start_day, start_year = order_data['start_date'].split('/')
        end_month, end_day, end_year = order_data['end_date'].split('/')
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = datetime.date(month=int(start_month), day=int(start_day), year=int(start_year))
        order.end_date = datetime.date(month=int(end_month), day=int(end_day), year=int(end_year))
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        db.session.add(order)
        db.session.commit()
        return 'All is OK', 200
    if request.method == 'DELETE':
        order = db.session.query(Order).get(gid)
        db.session.delete(order)
        db.session.commit()
        return 'All is OK', 200


@app.route("/offers", methods=['GET', 'POST'])
def get_all_offers():
    """
    all offers
    """
    if request.method == 'GET':
        offers = Offer.query.all()
        return jsonify([offer.to_dict() for offer in offers])
    if request.method == 'POST':
        offer = json.loads(request.data)
        db.session.add(Offer(id=offer['id'],
                             order_id=offer['order_id'],
                             executor_id=offer['executor_id'],
                             )
                       )
        db.session.commit()
        return "All is OK", 200


@app.route("/offers/<int:gid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_offer(gid):
    """
    one offer by pk
    """
    if request.method == 'GET':
        offer = Offer.query.get(gid)
        return jsonify(offer.to_dict())
    if request.method == 'PUT':
        offer = db.session.query(Offer).get(gid)
        offer_data = json.loads(request.data)
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        return 'All is OK', 200
    if request.method == 'DELETE':
        offer = db.session.query(Offer).get(gid)
        db.session.delete(offer)
        db.session.commit()
        return 'All is OK', 200


if __name__ == "__main__":
    app.run()
