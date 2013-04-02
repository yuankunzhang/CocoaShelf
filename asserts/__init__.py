# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase as Base, Twill

from cocoa import create_app
from cocoa.config import TestConfig
from cocoa.extensions import db

class TestCase(Base):

    def create_app(self):
        app = create_app(TestConfig)
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
