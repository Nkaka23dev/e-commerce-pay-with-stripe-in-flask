from myshop import db
from datetime import datetime

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),nullable=False)
    price= db.Column(db.Integer, nullable=False)
    discount=db.Column(db.Integer, nullable=False,default=0)
    stock= db.Column(db.Integer, nullable=False)
    desc= db.Column(db.Text, nullable=False)
    colors= db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    brand_id=db.Column(db.Integer,db.ForeignKey('brand.id'),nullable=False)
    brand=db.relationship('Brand',backref=db.backref('brand',lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('category',lazy=True))

    image_1=db.Column(db.String(120),nullable=False,default='default.jpg')
    image_2=db.Column(db.String(120),nullable=False,default='default.jpg')
    image_3=db.Column(db.String(120),nullable=False,default='default.jpg')
    
    
     
    def __repr__(self):
        return f"Product('{self.id}','{self.name}')"

class Brand(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=True)

    def __repr__(self):
        return f"Brand('{self.id}','{self.name}')"

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=True)
   

    def __repr__(self):
        return f"Category('{self.id}','{self.name}')"

db.create_all()
