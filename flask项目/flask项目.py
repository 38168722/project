from flask import Flask,render_template,redirect,request,url_for,session
import config
from models import User,Question,Answer
from exts import db
from decorations import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
@login_required
def index():
    context={
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('password')
        user = User.query.filter(User.username==username,User.password==password).first()
        if user:
            session['user_id']=user.id
            #如果想在31天内都不需要登录
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return u'帐号或密码错误'

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #手机号码验证，如果注册过就不能再注册了。
        user = User.query.filter(User.telephone==telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码!'
        else:
            if password1!=password2:
                return u'两次密码不相等，请核对后再填写!'
            else:
                user = User(telephone=telephone,username=username,password=password2)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/question',methods=['GET','POST'])
@login_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        question=Question(title=title,content=content)
        user_id=session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model=Question.query.filter(Question.id==question_id).first()
    answers=Answer.query.filter(Answer.question_id==question_id).order_by('-create_time').all()
    return render_template('detail.html',question=question_model,answers=answers)

@app.route('/add_answer',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id=session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    print("user_id=%s"%user.id)
    answer.author = user
    question = Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))



if __name__ == '__main__':
    app.run()
