# -*- coding: utf-8 -*-
#
# File: RDV_RendezVousView.py
#
# Copyright (c) 2008 by Ecreall
# Generator: ArchGenXML Version 2.2 (svn)
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Vincent Fretin <vincentfretin@ecreall.com>"""
__docformat__ = 'plaintext'

##code-section module-header #fill in your manual code here
from Products.rendezvous.browser.RDV_RendezVousUtility import RDV_RendezVousUtility
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
##/code-section module-header

from zope import interface
from zope import component
from Products.CMFPlone import utils
from Products.Five import BrowserView
from zope.interface import implements
from Products.rendezvous.content.RDV_RendezVous import RDV_RendezVous
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin


class RDV_RendezVousView(BrowserView):
    """
    """

    ##code-section class-header_RDV_RendezVousView #fill in your manual code here
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    ##/code-section class-header_RDV_RendezVousView

    @memoize
    def getPropositionsItemsByOrderedDates(self):
        context = self.context.aq_inner
        propositions_by_dates = context.getPropositionObjectsByDates()
        return [(date, propositions_by_dates[date]) for date in sorted(propositions_by_dates.keys())]

    def getParticipationClass(self, participant, proposition):
        prop_obj = getattr(self.context, proposition)
        if participant in prop_obj.getAvailable():
            return self.AVAILABLE
        if participant in prop_obj.getUnavailable():
            return self.UNAVAILABLE
        return self.UNKNOWN

    def addParticipation(self):
        context = self.context.aq_inner
        actor = self.request.AUTHENTICATED_USER
        participant = actor.getId()
        try:
            selected_propositions = self.request.form['propositions']
        except KeyError:
            selected_propositions = ()
        context.addParticipant(participant)
        for prop in self._getAllPropositionsIds():
            prop_obj = getattr(context, prop)
            checked = prop in selected_propositions
            prop_obj.manageParticipant(participant, checked)

        actor_fullname = actor.getProperty('fullname', participant)
        actor_email = actor.getProperty('email', None)
        encoding = getUtility(ISiteRoot).getProperty('email_charset')
        template = getattr(self.context, "rdv_participation_notification")
        owner = self.context.getOwner()
        owner_email = owner.getProperty('email', None)
        owner_name = owner.getProperty('fullname', owner.getId())
        if owner_email:
            message = template(self.context, self.request,
                                       actor_fullname=actor_fullname,
                                       actor_email=actor_email,
                                       receipt_to_email=owner_email,
                                       receipt_to_name=owner_name)
            self.context.MailHost.send(message.encode(encoding))

        self.request.response.redirect(self.context.absolute_url())

    def getFullname(self, member_id):
        portal_membership = getToolByName(self, "portal_membership")
        member = portal_membership.getMemberById(member_id)
        return member and member.getProperty("fullname") or member_id

    def getNbParticipantsForProposition(self, prop_id):
        return len(getattr(self.context, prop_id).getAvailable())

    def _getAllPropositionsIds(self):
        return [p[1] for date, propositions in self.getPropositionsItemsByOrderedDates()
                         for p in propositions]

##code-section module-footer #fill in your manual code here
##/code-section module-footer


