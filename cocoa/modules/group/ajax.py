# -*- coding: utf-8 -*-
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from .models import Group

class AjaxActions(object):

    @staticmethod
    @login_required
    def join(obj_response, group_id, intro):
        group = Group.query.get_or_404(group_id)
        group.applied(current_user, intro)

        return obj_response.alert(_(u'Your applicant has been sent.'))
