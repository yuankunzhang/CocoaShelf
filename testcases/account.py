# -*- coding: utf-8 -*-
from testcases import TestCase

from cocoa.extensions import db
from cocoa.modules.account.models import User

class TestAccount(TestCase):

    def test_save(self):
        u1 = User(u'feber@gmail.com', u'1')
        u1.save()
        assert User.query.count() == 1
        assert u1 in db.session
        assert u1.username == u'feber'

        u2 = User(u'feber@126.com', u'1')
        u2.save()
        assert User.query.count() == 2
        assert u2 in db.session
        assert u2.username == u'feber2'

        u3 = User(u'feber@hotmail.com', u'1')
        u3.save()
        assert User.query.count() == 3
        assert u3 in db.session
        assert u3.username == u'feber3'

        u4 = User(u'feber@gmail.com', u'1')
        self.assertRaises(ValueError, u4.save)

    def test_signup(self):
        self.client.post('/u/signup/', data=dict(
            email='abc@gmail.com',
            password='1',
            confirm='1',
        ), follow_redirects=True)
        assert User.get_by_email('abc@gmail.com') is not None

        self.client.post('/u/signup/', data=dict(
            email='abcd@gmail.com',
            password='1',
            confirm='2',
        ), follow_redirects=True)
        assert User.get_by_email('abcd@gmail.com') is None

        self.client.post('/u/signup/', data=dict(
            email='abcd.com',
            password='1',
            confirm='1',
        ), follow_redirects=True)
        assert User.get_by_email('abcd.com') is None
