# -*- coding: utf-8 -*-
from flask import current_app
from flask.ext.script import Manager, prompt_bool

from cocoa import create_app
from cocoa.extensions import db
from cocoa.modules.location.models import IpSection, City, Province
from cocoa.modules.account.models import User
from cocoa.modules.book.models import Book, Category, BookCategory, \
    Tag, BookTags, BookExtra
from cocoa.modules.library.models import ShelfHave, ShelfRead, \
    ShelfReading, ShelfWish, ShelfLike, Library

manager = Manager(create_app())

@manager.command
def db_create_all():
    """创建数据表"""

    db.create_all()


@manager.command
def db_drop_all():
    """移除所有数据表"""

    if prompt_book("Are you sure? You will lose all your data!"):
        db.drop_all()


@manager.shell
def make_shell_context():
    return dict(app=current_app,
                db=db,)

if __name__ == '__main__':
    manager.run()
