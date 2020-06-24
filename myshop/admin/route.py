from flask import render_template,flash,redirect,url_for,request,abort
from .form import RegisterForm,LoginForm
from myshop import app,db,bcrypt
from myshop.customer.models import Customer
from flask_login import login_user,current_user,login_required,logout_user
from myshop.products.models import Product,Brand,Category

@app.route('/dashboard')
@login_required
def admin():
    if current_user.is_admin==False:
        return abort(404)
    products=Product.query.all()
    return render_template('admin/index.html',title='Admin',products=products)

@app.route('/brands')
@login_required
def brands():
    if current_user.is_admin==False:
        return abort(404)
    brands=Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brands.html',title='Admin-Brands',brands=brands)

@app.route('/categories')
@login_required
def categories():
    if current_user.is_admin==False:
        return abort(404)
    categories=Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brands.html',title='Admin-categories',categories=categories)

@app.route('/register',methods=['GET','POST'])
@login_required
def register():
    if current_user.is_admin==False:
         return redirect('home')
    form=RegisterForm()
    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer=Customer(name=form.name.data,username=form.username.data,email=form.email.data,
        password=hash_password,is_admin=True)
        db.session.add(customer)
        db.session.commit()
        flash(f'{form.name.data} Thank you for registering','success')
        return redirect(url_for('home'))
    return render_template('admin/register.html',title='Register Page',form=form)

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if current_user.is_authenticated:
#       return redirect(url_for('home'))
#     form=LoginForm()
#     if form.validate_on_submit():
#        user=User.query.filter_by(email=form.email.data).first()
#        if user and bcrypt.check_password_hash(user.password,form.password.data):
#         login_user(user)
#         next_page=request.args.get('next')
#         flash(f'{current_user.name} Welcome to the admin page','info')
#         return redirect(next_page) if next_page else redirect(url_for('admin'))
#        else:
#            flash('Check your email and password','danger')
#     return render_template('admin/login.html',title='Login page',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

