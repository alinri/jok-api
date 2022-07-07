import os
import secrets
from urllib import parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, func, select
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+mysqldb://{os.getenv("FLASK_DB_USER")}:'\
    f'{parse.quote(os.getenv("FLASK_DB_PASSWORD"))}@'\
    f'{os.getenv("FLASK_DB_HOST")}/'\
    f'{os.getenv("FLASK_DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Post(db.Model):
    __tablename__ = 'post'

    post_id = Column(Integer, primary_key=True)
    post_content = Column(String(length=2000))
    four_joke_id = Column(String(length=32))
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship('Category', back_populates='posts')


class Category(db.Model):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(length=255))
    category_type = Column(String(length=16))
    posts = relationship('Post')


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_fk = True

    post_id = ma.auto_field()
    post_content = ma.auto_field()
    post_type = fields.String(attribute='category.category_type')
    category_id = ma.auto_field()


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@app.route('/random/')
def random_post():
    random_offset = db.session.query(
        func.floor(
            1 +
            func.rand() *
            (func.max(Post.post_id) - 1)
        )
    ).scalar()
    post = Post.query.filter(Post.post_id >= random_offset).limit(1).first()
    return post_schema.dump(post)
