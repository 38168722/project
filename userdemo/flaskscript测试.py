#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_script import Manager

app = Flask(__name__,template_folder='templates',static_url_path='/static')
import config
app.config.from_object(config)


if __name__ == '__main__':
    app.run()