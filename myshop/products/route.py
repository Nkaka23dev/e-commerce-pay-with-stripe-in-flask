import secrets
import os
from PIL import Image
from flask import render_template,flash,redirect,url_for,request,current_app,abort
from .forms import BrandForm,CategoryForm,ProductForm,UpdateProductForm
from myshop import app,db
from .models import Brand,Category,Product
from flask_login import login_required,current_user

def brands():
    brands=Brand.query.join(Product,(Brand.id==Product.brand_id)).order_by(Brand.id.desc()).all()
    return brands

def categories():
    categories=Category.query.join(Product,(Category.id==Product.category_id)).order_by(Category.id.desc()).all()
    return categories

@app.route('/home')
@app.route('/')
def home():
    page=request.args.get('page',1,type=int)
    products=Product.query.filter(Product.stock>0).paginate(page=page,per_page=8)
    return render_template('products/index.html',title='Home',products=products,brands=brands(),categories=categories())

@app.route('/product/<int:single_id>')
def single_page(single_id):
    product=Product.query.get_or_404(single_id)
    return render_template('products/single_page.html',title='Details',product=product,brands=brands(),categories=categories())


@app.route('/brand/<int:bra_id>',methods=['GET','POST'])
def get_brand(bra_id):
    page=request.args.get('page',1,type=int)
    get_bra=Brand.query.filter_by(id=bra_id).first_or_404()
    brand=Product.query.filter_by(brand=get_bra).paginate(page=page,per_page=8)
    return render_template('products/index.html',title='Brands',brand=brand,brands=brands(),categories=categories(),get_bra=get_bra)

@app.route('/category/<int:my_id>',methods=['GET','POST'])
def get_category(my_id):
    page=request.args.get('page',1,type=int)
    get_cat=Category.query.filter_by(id=my_id).first_or_404()
    category=Product.query.filter_by(category=get_cat).paginate(page=page,per_page=8)
    return render_template('products/index.html',title='Category',category=category,categories=categories(),brands=brands(),get_cat=get_cat)
   

@app.route('/brand',methods=['GET','POST'])
@login_required
def brand():
    if current_user.is_admin==False:
        return abort(404)
    form=BrandForm()
    if form.validate_on_submit():
        brand=Brand(name=form.name.data)
        db.session.add(brand)
        db.session.commit()
        flash(f'{form.name.data} brand was added to your database','info')
        return redirect(url_for('brands'))
    return render_template('products/brand.html',title='Add-Brand',form=form,
    legend='Add Brand')

@app.route('/brands/<int:brand_id>',methods=['GET','POST'])
@login_required
def update_brand(brand_id):
    if current_user.is_admin==False:
        return abort(404)
    brand=Brand.query.get_or_404(brand_id)
    form=BrandForm()
    if form.validate_on_submit():
        brand.name=form.name.data
        db.session.commit()
        flash(f'{brand.name} Brand has been updated','info')
        return redirect(url_for('brands'))
    elif request.method=='GET':
        form.name.data=brand.name
    return render_template('products/brand.html',title='Brand-update',form=form,
    legend='Update Brand')

@app.route('/deletebrand/<int:id>',methods=['POST'])
@login_required
def delete_brand(id):
    brand=Brand.query.get_or_404(id)
    # brandx=Product.query.filter_by(brand_id=id)
    if request.method=='POST':
        try:
           db.session.delete(brand)
           db.session.commit()
           flash(f'A brand {brand.name} was deleted from your database','success')
           return redirect(url_for('brands'))
        except Exception as e:
            flash("This brand can't be deleted! It contains some products","danger")
             
            return redirect(url_for('brands'))
                    
@app.route('/category',methods=['GET','POST'])
@login_required
def category():
    if current_user.is_admin==False:
        return abort(404)
    form=CategoryForm()
    if form.validate_on_submit():
        category=Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash(f'A {form.name.data} Category was added to your database','info')
        return redirect(url_for('categories'))
    return render_template('products/category.html',title='Category',form=form,
    legend='Add Category')

@app.route('/categories/<int:category_id>',methods=['GET','POST'])
@login_required
def update_category(category_id):
    if current_user.is_admin==False:
        return abort(404)
    category=Category.query.get_or_404(category_id)
    form=CategoryForm()
    if form.validate_on_submit():
        category.name=form.name.data
        db.session.commit()
        flash(f'A {category.name} Category has been updated','info')
        return redirect(url_for('categories'))
    elif request.method=='GET':
        form.name.data=category.name
    return render_template('products/category.html',title='Update-Category',form=form,
    legend='Update Category')

@app.route('/deletecategory/<int:id>',methods=['POST'])
@login_required
def delete_category(id):
    category=Category.query.get_or_404(id)
    # categoryx=Product.query.filter_by(category_id=id)
    if request.method=='POST':
        try:
           db.session.delete(category)
           db.session.commit()
           flash(f'A category {category.name} was deleted from your database','success')
           return redirect(url_for('admin'))
        except Exception as e:
            flash("This category can't be deleted! It contains some products","danger")
             
            return redirect(url_for('categories'))

def save_picture(form_pic):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_pic.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/photoes',picture_fn)
    # out_put=(125,125)
    # i=Image.open(form_pic)
    # i.thumbnail(out_put)
    form_pic.save(picture_path)
    return picture_fn

@app.route('/product',methods=['GET','POST'])
@login_required
def product():
    if current_user.is_admin==False:
        return abort(404)
    brands=Brand.query.all()
    categories=Category.query.all()
    form=ProductForm()
    if form.validate_on_submit():
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        desc=form.description.data
        colors=form.color.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        if form.picture_1.data and form.picture_2.data and form.picture_3.data:
           image_1=save_picture(form.picture_1.data)
           image_2=save_picture(form.picture_2.data)
           image_3=save_picture(form.picture_3.data)
        product=Product(name=name,price=price,discount=discount,stock=stock,desc=desc,colors=colors,
        brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(product)
        db.session.commit()
        flash(f'A product {form.name.data} is added to your database','info ')
        return redirect(url_for('admin'))
    return render_template('products/product.html',title='Add Product',form=form,
    brands=brands,categories=categories)

@app.route('/updateproduct/<int:product_id>',methods=['GET','POST'])
@login_required
def update_product(product_id):
    if current_user.is_admin==False:
        return abort(404)
    brands=Brand.query.all()
    categories=Category.query.all()
    product=Product.query.get_or_404(product_id)
    brand=request.form.get('brand')
    category=request.form.get('category')
    form=UpdateProductForm()
    if form.validate_on_submit():
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.stock=form.stock.data
        product.desc=form.description.data
        product.colors=form.color.data
        product.brand_id=brand
        product.category_id=category
        if form.picture_1.data:
            try:
                os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_1))
                product.image_1=save_picture(form.picture_1.data)
            except:
                product.image_1=save_picture(form.picture_1.data)
        
        if form.picture_2.data:
                
            try:
                os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_2))
                product.image_2=save_picture(form.picture_2.data)
            except:
                 product.image_2=save_picture(form.picture_2.data)

        if form.picture_3.data:
                
            try:
                os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_3))
                product.image_3=save_picture(form.picture_3.data)
            except:
                 product.image_3=save_picture(form.picture_3.data)
          
        db.session.commit()
        flash(f'{product.name} has been updated','success')
        return redirect(url_for('admin'))
    elif request.method=='GET':
         form.name.data=product.name
         form.price.data=product.price
         form.discount.data=product.discount
         form.stock.data=product.stock
         form.description.data=product.desc
         form.color.data=product.colors
    return render_template('products/updateproduct.html',title='Update Product',form=form,
    product=product,brands=brands,categories=categories)

@app.route('/deleteproduct/<int:prod_id>',methods=['POST'])
@login_required
def delete_product(prod_id):
    product=Product.query.get_or_404(prod_id)
    if request.method=='POST':
        try:
            os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_1))
            os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_2))
            os.unlink(os.path.join(current_app.root_path,'static/photoes/'+product.image_3))

        except Exception as e:
                print(e)

        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} is delete from your record.','success')
        return redirect(url_for('admin'))

    flash(f'{product.name} can not be delete.','danger')
    return redirect(url_for('admin'))


               
        
        
                 



                            
    
