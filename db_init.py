import data
import datetime
from lib import *

db.drop_all()

db.create_all()

db.session.add_all([User(
               id=user['id'],
               first_name=user['first_name'],
               last_name=user['last_name'],
               age=user['age'],
               email=user['email'],
               role=user['role'],
               phone=user['phone']
               ) for user in data.Users])

db.session.add_all([Offer(
               id=offer['id'],
               order_id=offer['order_id'],
               executor_id=offer['executor_id'],
               ) for offer in data.Offers])

for order in data.Orders:
    start_month, start_day, start_year = order['start_date'].split('/')
    end_month, end_day, end_year = order['end_date'].split('/')
    db.session.add(Order(
                   id=order['id'],
                   name=order['name'],
                   description=order['description'],
                   start_date=datetime.date(month=int(start_month), day=int(start_day), year=int(start_year)),
                   end_date=datetime.date(month=int(end_month), day=int(end_day), year=int(end_year)),
                   address=order['address'],
                   price=order['price'],
                   customer_id=order['customer_id'],
                   executor_id=order['executor_id']
                   ))

db.session.commit()
