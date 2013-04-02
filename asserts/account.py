# -*- coding: utf-8 -*-
from flask.ext.login import current_user

from asserts import TestCase

from cocoa.extensions import db
from cocoa.modules.account.models import User
from cocoa.modules.location.models import City, Province

class TestAccount(TestCase):

    def test_save(self):
        """
            1.一个邮箱只能注册一次
            2.初始化用户名
        """

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
        """
            1.邮箱格式正确
            2.密码与确认密码一致
            (3).密码长度限制
        """

        # 有效注册
        self.client.post('/u/signup/', data=dict(
            email='abc@gmail.com',
            password='1',
            confirm='1',
        ), follow_redirects=True)
        assert User.get_by_email('abc@gmail.com') is not None

        # 密码不一致
        self.client.post('/u/signup/', data=dict(
            email='abcd@gmail.com',
            password='1',
            confirm='2',
        ), follow_redirects=True)
        assert User.get_by_email('abcd@gmail.com') is None

        # 邮箱格式不正确
        self.client.post('/u/signup/', data=dict(
            email='abcd.com',
            password='1',
            confirm='1',
        ), follow_redirects=True)
        assert User.get_by_email('abcd.com') is None

    def test_update(self):
        u1 = User(u'feber@gmail.com', u'1')
        u1.save()

        # 北京市 110100
        u1.update(u'Alice', u'Much a do than nothing.', 0, u'110100')
        assert u1.penname == 'Alice'
        assert u1.intro == 'Much a do than nothing.'
        assert u1.gender == 0
        assert u1.city_id == '110100'

    def test_update_password(self):
        u1 = User(u'feber@gmail.com', u'1')
        u1.save()

        u1.update_password(u'1', u'2')
        assert u1.check_password(u'2')

    def test_get_display_name(self):
        u1 = User(u'feber@gmail.com', u'1')
        u1.save()
        assert u1.get_display_name() == u'feber'

        u1.update(u'Alice', None, None, None)
        assert u1.get_display_name() == u'Alice'

    def test_get_location(self):
        """
            User.get_location()
            User.location
        """

        u1 = User(u'feber@gmail.com', u'1')
        u1.save()

        city = City()
        city.city_id = u'110100'
        city.name = u'北京市'
        city.province_id = u'110000'
        db.session.add(city)
        db.session.commit()

        province = Province()
        province.province_id = u'110000'
        province.name = u'北京市'
        db.session.add(province)
        db.session.commit()

        u1.update(None, None, None, u'110100')
        assert u1.get_location()['city_id'] == u'110100'
        assert u1.get_location()['province_id'] == u'110000'
        assert u1.get_location()['text'] == u'北京 北京市'
        assert u1.location == u'北京 北京市'
