# -*- coding: utf-8 -*-
from collective.lineage.interfaces import IChildSiteCreatedEvent
from collective.lineage.interfaces import IChildSiteRemovedEvent
from collective.lineage.interfaces import IChildSiteWillBeCreatedEvent
from collective.lineage.interfaces import IChildSiteWillBeRemovedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer

@implementer
class ChildSiteWillBeCreatedEvent(ObjectEvent):
    """PASS"""
    
@implementer
class ChildSiteCreatedEvent(ObjectEvent):
    """PASS"""
    
@implementer
class ChildSiteWillBeRemovedEvent(ObjectEvent): 
    """PASS"""
    
@implementer
class ChildSiteRemovedEvent(ObjectEvent):
    """PASS"""
