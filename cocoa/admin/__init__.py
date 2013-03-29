# -*- coding: utf-8 -*-
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView

from cocoa.extensions import db
from cocoa.permissions import admin as role_admin
from cocoa.modules.location.models import City
from cocoa.modules.account.models import User
from cocoa.modules.tag.models import Tag

__all__ = ['admin']

class PermissionCheck(AdminIndexView):
    def is_accessible(self):
        return role_admin.can()


admin = Admin(name='Cocoa', index_view=PermissionCheck())

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tag, db.session))
