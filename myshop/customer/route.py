from myshop import app,bcrypt,db
from flask import render_template,flash,redirect,url_for,request,session,make_response
from .forms import CustomerRegister,CustomerLogin
from .models import Customer,Customer_order
from flask_login import login_user,logout_user,current_user,login_required
import secrets
import os
import pdfkit
import stripe

publishable_key='pk_test_51GqaJEER9nv2mwVYduduTD0asSJTH03J50ccb7JEShKXrn17IDjncPKVPbtmwPadT1cfk85UuqhNpqA7mkP9lC3H00x0LpH2SF'
stripe.api_key='sk_test_51GqaJEER9nv2mwVYhSDto7ZhPBC8yObZwwQjfZtE9ohtqAa9qTZ9lEEfcrw8DIzoDCyCLOpAOK9LKzrSZmZo7vfL00sIlX0isf'

@app.route('/payment',methods=['POST'])
@login_required
def payment():
    invoice=request.form.get('invoice')
    amount=request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Nkakashop',
        amount=amount,
        currency='usd',
    )
    orders=Customer_order.query.filter_by(customer_id=current_user.id,invoice=invoice).order_by(Customer_order.id.desc()).first()
    orders.status='Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('customer/thanks.html',title='Customer Thanks')


@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    if current_user.is_authenticated:
      return redirect(url_for('home'))
    form=CustomerRegister()
    if form.validate_on_submit():
       hash_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
       name=form.name.data
       username=form.username.data
       email=form.email.data
       country=form.country.data
       state=form.state.data
       city=form.city.data
       contact=form.contact.data
       address=form.address.data
       zip_code=form.zip_code.data
       customer=Customer(name=name,username=username,email=email,password=hash_password,
       country=country,state=state,city=city,contact=contact,address=address,zip_code=zip_code)
       db.session.add(customer)
       db.session.commit()
      #  flash('You have registerd!','success')
       return redirect(url_for('home'))  
    return render_template('customer/customer.html',title='Customer Register',form=form)

@app.route('/customer/login',methods=['GET','POST'])
def customer_login():
   if current_user.is_authenticated:
      return redirect(url_for('home'))
   form=CustomerLogin()
   if form.validate_on_submit():
      customer=Customer.query.filter_by(email=form.email.data).first()
      if customer and bcrypt.check_password_hash(customer.password,form.password.data):
         login_user(customer)
         next_page=request.args.get('next')
         return redirect(next_page) if next_page else redirect(url_for('home'))
      else:
         flash('Invalid email and password','danger')
   return render_template('customer/customer_login.html',title='Customer Login',form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

def updateshoppingcart():
   for _key,product in session['Shoppingcart'].items():
       session.modified=True
       del product['image']
       del product['colors']
   return updateshoppingcart
    
@app.route('/get_order')
@login_required
def get_order():
   if current_user.is_authenticated:
      customer_id=current_user.id
      invoice=secrets.token_hex(5)
      updateshoppingcart()
      try:
         order=Customer_order(invoice=invoice,customer_id=customer_id,orders=session
         ['Shoppingcart'])
         db.session.add(order)
         db.session.commit()
         session.pop('Shoppingcart')
         flash('Your order has been sent successfully','info')
         return redirect(url_for('get_orders',invoice=invoice))
      except Exception as e:
         print(e)
         flash('Something went wrong while getting order','danger')
         return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def get_orders(invoice):
   if current_user.is_authenticated:
      grandtotal=0
      subtotal=0
      customer_id=current_user.id
      customer=Customer.query.filter_by(id=customer_id).first()
      orders=Customer_order.query.filter_by(customer_id=customer_id,invoice=invoice).order_by(Customer_order.id.desc()).first()

      for key,product in orders.orders.items():
         discount=(product['discount']/100)* float(product['price'])
         subtotal+=float(product['price'])*int(product['quantity'])
         subtotal-=discount
         tax=("%.2f" % (.06*float(subtotal)))
         grandtotal=("%0.2f"%(1.06*float(subtotal)))
   else:
      return redirect(url_for('customer_login'))
   return render_template('customer/order.html',invoice=invoice,tax=tax,subtotal=subtotal,
   grandtotal=grandtotal,customer=customer,orders=orders)

@app.route('/get_pdf/<invoice>',methods=['POST'])
@login_required
def get_pdf(invoice):
   if current_user.is_authenticated:
      grandtotal=0
      subtotal=0
      customer_id=current_user.id
      if request.method=="POST":
         customer=Customer.query.filter_by(id=customer_id).first()
         orders=Customer_order.query.filter_by(customer_id=customer_id).order_by(Customer_order.id.desc()).first()
         for key,product in orders.orders.items():
            discount=(product['discount']/100)* float(product['price'])
            subtotal+=float(product['price'])*int(product['quantity'])
            subtotal-=discount
            tax=("%.2f" % (.06*float(subtotal)))
            grandtotal=float("%0.2f"%(1.06*subtotal))
         rendered=render_template('customer/pdf.html',invoice=invoice,tax=tax,subtotal=subtotal,
         grandtotal=grandtotal,customer=customer,orders=orders)
         pdf=pdfkit.from_string(rendered,False)
         response=make_response(pdf)
         response.headers['content-Type']='application/pdf'
         response.headers['content-Disposition']='atteched;filename='+invoice+'.pdf'
         return response
   return request(url_for('get_orders'))
   



      