# -*- coding: utf-8 -*-
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from .models import Group, GroupApplicant

class AjaxActions(object):

    @staticmethod
    @login_required
    def join(obj_response, group_id, intro):
        group = Group.query.get_or_404(group_id)
        group.applied(current_user, intro)

        return obj_response.alert(_(u'Your applicant has been sent.'))

    @staticmethod
    @login_required
    def accept_applicant(obj_response, applicant_id):
        applicant = GroupApplicant.query.get_or_404(applicant_id)
        applicant.accepted()

        obj_response.script('$(\'table tr[value="' + \
            str(applicant_id) + '"]\').remove();'
        )

    @staticmethod
    @login_required
    def decline_applicant(obj_response, applicant_id):
        applicant = GroupApplicant.query.get_or_404(applicant_id)
        applicant.declined()

        obj_response.script('$(\'table tr[value="' + \
            str(applicant_id) + '"]\').remove();'
        )
