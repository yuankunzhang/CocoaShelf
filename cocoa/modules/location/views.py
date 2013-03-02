# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request

from .models import provinces, cities

mod = Blueprint('location', __name__)

@mod.route('/provinces/', methods=['POST'])
def get_province_list():

    return provinces()


@mod.route('/cities/', methods=['POST'])
def get_city_list():

    province_id = request.form['province_id']
    return cities(province_id)
