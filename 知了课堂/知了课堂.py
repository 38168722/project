from flask import Flask, request, redirect, url_for,render_template

app = Flask(__name__)
app.config['templates_auto_loads']=True

# @app.route('/')
# def hello_world():
#     a=2/0
#     return 'Hello World!'

# @app.route('/<any(article,blog):url_path>/<id>/')
# def item(url_path,id):
#   parm=request.args.get('name')
#   print("姓名是什么==%s"%parm)
#   return url_path
@app.route('/list/<int:page>/')
def ceshi(page):
    books=[
        {
            "name":"三国演义",
            'author':"罗贯中"
        },
        {
            "name": "红楼梦",
            'author': "曹雪芹"
        },
        {
            "name": "西游记",
            'author': "吴承恩"
        },
        {
            "name": "水浒传",
            'author': "施耐庵"
        }
    ]

    return render_template("index.html",books=books)

@app.route('/')
def index():
    return render_template('son.html')

if __name__ == '__main__':
    app.run(debug=True)
