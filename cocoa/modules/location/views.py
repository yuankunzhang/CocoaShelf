# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request

from .models import provinces, cities

mod = Blueprint('location', __name__)

@mod.route('/provinces/', methods=['POST'])
def provinces():

    return provinces()


@mod.route('/cities/', methods=['POST'])
def cities():

    province_id = request.form['province_id']
    return cities(province_id)
