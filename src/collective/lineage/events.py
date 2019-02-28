# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer

@implementer
class ChildSiteWillBeCreatedEvent(ObjectEvent):

@implementer
class ChildSiteCreatedEvent(ObjectEvent):

@implementer
class ChildSiteWillBeRemovedEvent(ObjectEvent): 

@implementer
class ChildSiteRemovedEvent(ObjectEvent):
 
