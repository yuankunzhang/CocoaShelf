# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

Role = Enum('MEMBER', 'MODERATOR', 'ADMIN')
Gender = Enum('SECRET', 'MALE', 'FEMALE')
