#!/usr/bin/env python
# -*- coding: utf-8 -*-
from IPython.kernel import manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
import config
app.config.from_object(config)
db=SQLAlchemy(app)
# db.create_all()

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100),nullable=False)

class Article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('articles'))

db.create_all()




@app.route('/')
def index():
    # 增加
    # article=Article(title='数据增加',content='添加的第一条数据')
    # db.session.add(article)
    # #事务
    # db.session.commit()
    # 查
    # result=Article.query.filter(Article.title=='数据增加').all()
    # print("result是什么类型",type(result))
    # article1=result[0]
    # print(article1.title)
    # print(article1.content)
    # result=Article.query.filter(Article.title=='数据增加').first()
    # print("title=%s"%result.title)
    # print("content=%s"%result.content)
    # 改
    # 1、先把你要更改的数据查找出来
    # 2、修改数据
    # 3、做事务提交
    # result=Article.query.filter(Article.title=='数据增加').first()
    # result.title="修改测试"
    # db.session.commit()
    # 删除
    # 1 把需要删除的数据查找出来，然后做删除操作
    # Article.query.filter(Article.title=='修改测试').delete()
    # 2 删除后提交事务
    # db.session.commit()
    #想要添加一篇文章就必先添加一个用户，所以先增用户
    # user1=User(username='ziliao')
    # db.session.add(user1)
    # db.session.commit()
    # article=Article(title='python从入门到精通',content="课时160",author_id=1)
    # db.session.add(article)
    # db.session.commit()
    # 找文章标题为python从入门到精通的作者名称
    # article=Article.query.filter(Article.title=='python从入门到精通').first()
    # author_id=article.author_id
    # user = User.query.filter(User.id==author_id).first()
    # return "作者是%s"%user.username
    # article=Article(title='python入门',content="python学习手册",author_id=1)
    # db.session.add(article)
    # db.session.commit()
    # 找文章标题为python入门的这个作者
    # article = Article.query.filter(Article.title=="python入门").first()
    # print(article.author.username)
    # 找用户zhiliao写的所有的书
    # user = User.query.filter(User.username=="ziliao").first()
    # articles=user.articles
    # for item in articles:
    #     print("书名",item.title)
    #
    # return "添加成功"
    pass




if __name__ == '__main__':
    app.run()