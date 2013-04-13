# -*- coding: utf-8 -*-
from cocoa.helpers.enum import Enum

Role = Enum('MEMBER', 'MODERATOR', 'ADMIN')

Gender = Enum('SECRET', 'MALE', 'FEMALE')
Gender.SECRET.set_text(u'保密')
Gender.MALE.set_text(u'男')
Gender.FEMALE.set_text(u'女')

Status = Enum('INACTIVE', 'ACTIVATED', 'DELETED')
