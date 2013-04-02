# -*- coding: utf-8 -*-
from asserts import TestCase

class TestFrontend(TestCase):

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200
