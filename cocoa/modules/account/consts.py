# -*- coding: utf-8 -*-
from flask.ext.babel import gettext as _

from cocoa.helpers.enum import Enum

Role = Enum('MEMBER', 'MODERATOR', 'ADMIN')

Gender = Enum('SECRET', 'MALE', 'FEMALE')
Gender.SECRET.set_text(_(u'Secret'))
Gender.MALE.set_text(_(u'Male'))
Gender.FEMALE.set_text(_(u'Female'))

Status = Enum('INACTIVE', 'ACTIVATED', 'DELETED')
