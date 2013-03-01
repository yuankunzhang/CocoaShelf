# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~~~

    运行应用实例
    2013.03.01
"""
from cocoa import create_app

app = create_app()
app.run(debug=True)
