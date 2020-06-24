from flask import render_template,flash,redirect,url_for,request,session
from myshop import app
from myshop.products.models import Product,Category,Brand
from myshop.products.route import brands,categories

def MergeDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+list(dict2.items()))
    else:
        return false

@app.route('/addcart',methods=['POST'])
def addcart():
    try:
       product_id=request.form.get('product_id')
       quantity=request.form.get('quantity')
       colors=request.form.get('colors')
       product=Product.query.filter_by(id=product_id).first()

       if product_id and quantity and colors and request.method=="POST":
          DictItems={product_id:{'name':product.name,'price':product.price,'discount':product.discount,
          'colors':colors,'quantity':quantity,'image':product.image_1}}
          if 'Shoppingcart' in session:
              print(session['Shoppingcart'])
              if product_id in session['Shoppingcart']:
                 for key,item in session['Shoppingcart'].items():
                     if float(key)==float(product_id):
                        session.modified=True
                        item['quantity']+=1
              else:
                   session['Shoppingcart']= MergeDicts(session['Shoppingcart'],DictItems)
                   return redirect(request.referrer) 
          else:
              session['Shoppingcart']=DictItems
              return redirect(request.referrer)

    except Exception as e:
      print(e)

    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))

    subtotal=0
    grandtotal=0
    for key,product in session['Shoppingcart'].items():
        discount=(product['discount']/100)* float(product['price'])
        subtotal+=float(product['price'])*int(product['quantity'])
        subtotal-=discount
        tax=("%.2f" % (.06*float(subtotal)))
        grandtotal=float("%0.2f"%(1.06*subtotal))
    return render_template('carts/carts.html',tax=tax,grandtotal=grandtotal,brands=brands(),categories=categories())

@app.route('/updatecart<int:item_id>',methods=['POST'])
def updatecart(item_id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    
    if request.method=='POST':
        quantity=request.form.get('quantity')
        try:
            session.modified=True
            for key,item in session['Shoppingcart'].items():
                if int(key)==item_id:
                    item['quantity']=quantity
                    flash('Item is successfullly updated!','primary')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deletecart<int:id>',methods=['GET'])
def deletecart(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))

    try:
        session.modified=True
        for key,item in session['Shoppingcart'].items():
            if int(key)==id:
                session['Shoppingcart'].pop(key,None)
                # flash('Item is updated!','info')
                return redirect(url_for('getCart'))
    
    except Exception as e:
        print(e)
        return redirect(url_for('getCard'))

@app.route('/empty')
def empty_cart():
    try:
        # session.clear()
        # using clear we make the userto clear the cart and logout,
        # which is not a good practice.
        session.pop('Shoppingcart',None)
        return redirect(url_for('home'))
    
    except Exception as e:
        print(e)
        return redirect(url_for('home'))