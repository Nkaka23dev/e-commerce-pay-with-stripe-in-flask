from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,TextAreaField
from wtforms.validators import DataRequired,ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from .models import Brand,Category

class BrandForm(FlaskForm):
    name=StringField('Addbrand',validators=[DataRequired()])
    submit=SubmitField('Add')
    def validate_name(self,name):
        name=Brand.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name exit in your database.')



class CategoryForm(FlaskForm):
    name=StringField('Addcat',validators=[DataRequired()])
    submit=SubmitField('Add')
    def validate_name(self,name):
        name=Category.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That name exit in your database.')
    

class ProductForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',validators=[DataRequired()])
    description=TextAreaField('Description',validators=[DataRequired()])
    color=TextAreaField('Colors',validators=[DataRequired()])
    picture_1=FileField('Image 1',
               validators=[FileRequired(),FileAllowed(['png','jpg','jpeg','gif'])])
    picture_2=FileField('Image 2',
               validators=[FileRequired(),FileAllowed(['png','jpg','jpeg','gif'])])
    picture_3=FileField('Image 3',
               validators=[FileRequired(),FileAllowed(['png','jpg','jpeg','gif'])]  )

    submit=SubmitField('Add Product')


class UpdateProductForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',validators=[DataRequired()])
    description=TextAreaField('Description',validators=[DataRequired()])
    color=TextAreaField('Colors',validators=[DataRequired()])
    picture_1=FileField('Image 1',
               validators=[FileAllowed(['png','jpg','jpeg','gif'])])
    picture_2=FileField('Image 2',
               validators=[FileAllowed(['png','jpg','jpeg','gif'])])
    picture_3=FileField('Image 3',
               validators=[FileAllowed(['png','jpg','jpeg','gif'])]  )

    submit=SubmitField('Update Product')
