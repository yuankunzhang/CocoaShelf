# -*- coding: utf-8 -*-
from blinker import Namespace

signals = Namespace()

test = signals.signal('test')
