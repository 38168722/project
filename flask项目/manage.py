#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager,Shell,Server
from flask_migrate import Migrate,MigrateCommand
from flask项目 import app
from exts import db
from models import User,Question,Answer

manager = Manager(app)

# 使用Migrate绑定app和db
migrate=Migrate(app,db,compare_type=True)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)
# manager.add_command('shell',Shell())
manager.add_command('runserver',Server())
if __name__ == '__main__':
    manager.run()


