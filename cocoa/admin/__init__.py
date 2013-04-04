# -*- coding: utf-8 -*-
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView

from cocoa.extensions import db
from cocoa.permissions import admin as role_admin
from cocoa.modules.location.models import City
from cocoa.modules.account.models import User
from cocoa.modules.book.models import Book
from cocoa.modules.blog.models import Post
from cocoa.modules.tag.models import Tag
from cocoa.modules.bookstore.models import Bookstore

__all__ = ['admin']

class PermissionCheck(AdminIndexView):
    def is_accessible(self):
        return role_admin.can()


admin = Admin(name='Cocoa', index_view=PermissionCheck())

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(Bookstore, db.session))
