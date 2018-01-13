from flask import Flask,render_template,session

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)

@app.route('/article/<id>')
def article(id):
    session["key"]="aaa"
    return "您请求的参数是%s"%id


if __name__ == '__main__':
    app.run()
    app.__call__()
