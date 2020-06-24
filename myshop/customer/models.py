from myshop import db
from datetime import datetime
from myshop import login_manager
from flask_login import UserMixin,current_user
import json




@login_manager.user_loader
def load_user(user_id):
  return Customer.query.get(int(user_id))

class Customer(db.Model,UserMixin):
  id=db.Column(db.Integer,primary_key=True)
  name=db.Column(db.String(100),unique=False)
  # l_name=db.Column(db.String(100),unique=False)
  username=db.Column(db.String(100),unique=True)
  email=db.Column(db.String(120),unique=True)
  password=db.Column(db.String(200),unique=False)
  country=db.Column(db.String(100),unique=False)
  state=db.Column(db.String(100),unique=False)
  city=db.Column(db.String(100),unique=False)
  contact=db.Column(db.String(100),unique=False)
  address=db.Column(db.String(100),unique=False)
  zip_code=db.Column(db.String(100),unique=False)
  profile=db.Column(db.String(200),unique=False,default='default.jpg')
  created_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  is_admin=db.Column(db.Boolean,default=False)
  def __repr__(self):
      return f"Customer('{self.id}','{self.username}','{self.email}')"

class JsonEcodedDict(db.TypeDecorator):
  impl=db.Text
  def process_bind_param(self,value,dialect):
    if value is None:
      return '{}'
    else:
      return json.dumps(value)

  def process_result_value(self,value,dialect):
    if value is None:
      return {}
    else:
      return json.loads(value)


class Customer_order(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  invoice=db.Column(db.String(20),unique=True,nullable=False)
  status=db.Column(db.String(20),default='Pending',nullable=False)
  customer_id=db.Column(db.Integer,unique=False,nullable=False)
  date_created=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
  orders=db.Column(JsonEcodedDict)

  def __repr__(self):
    return f"Customer_order('{self.customer_id}','{self.orders}'{self.invoice}')"



db.create_all()


 