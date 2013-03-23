# -*- coding: utf-8 -*-
from flask.ext.principal import RoleNeed, Permission

admin = Permission(RoleNeed('admin'))
moderator = Permission(RoleNeed('moderator'))
member = Permission(RoleNeed('member'))

# this is assigned when you want to block a permission to all
# never assign this role to anyone !
null = Permission(RoleNeed('null'))
