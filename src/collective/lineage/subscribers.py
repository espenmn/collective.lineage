from zope.component.interfaces import ISite
from zope.component import adapter
import zope.event

from Products.CMFCore.utils import getToolByName
from Products.Five.component import disableSite
from five.localsitemanager import make_objectmanager_site

from p4a.subtyper.interfaces import ISubtypeAddedEvent
from p4a.subtyper.interfaces import ISubtypeRemovedEvent

from collective.lineage.interfaces import IChildSite
from collective.lineage.events import ChildSiteWillBeCreatedEvent
from collective.lineage.events import ChildSiteCreatedEvent
from collective.lineage.events import ChildSiteWillBeRemovedEvent
from collective.lineage.events import ChildSiteRemovedEvent


def reindexObjectProvides(folder):
    pc = getToolByName(folder, 'portal_catalog')
    pc.reindexObject(
        folder,
        idxs=['object_provides']
    )


def enableFolder(folder):
    zope.event.notify(ChildSiteWillBeCreatedEvent(folder))
    if not ISite.providedBy(folder):
        make_objectmanager_site(folder)
    # reindex so that the object_provides index is aware of our
    # new interface
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteCreatedEvent(folder))


def disableFolder(folder):
    zope.event.notify(ChildSiteWillBeRemovedEvent(folder))
    # remove local site components
    disableSite(folder)

    # reindex the object so that the object_provides index is
    # aware that we've removed it
    reindexObjectProvides(folder)
    zope.event.notify(ChildSiteRemovedEvent(folder))


@adapter(ISubtypeAddedEvent)
def enableChildSite(event):
    """When a lineage folder is created, turn it into a component site
    """
    if not IChildSite.providedBy(event.object):
        return
    folder = event.object
    enableFolder(folder)


@adapter(ISubtypeRemovedEvent)
def disableChildSite(event):
    """When a child site is turned off, remove the local components
    """
    subtype = event.subtype
    if subtype is not None and subtype.type_interface == IChildSite:
        folder = event.object
        disableFolder(folder)

def addURLOverrides(event):
    """When Plone starts up, add our overrides for
        - ZPublisher.HTTPRequest.HTTPRequest.physicalPathToURL
    """
    from ZPublisher.HTTPRequest import HTTPRequest
    from collective.lineage.absoluteurl import physicalPathToURL

    HTTPRequest._physicalPathToURL = HTTPRequest.physicalPathToURL
    HTTPRequest.physicalPathToURL = physicalPathToURL

    # Ideally, we could use `useBrains`,
    # But ZCatalog forces AbstractCatalogBrain first in the MRO.
    #from zope.app.appsetup.bootstrap import getInformationFromEvent
    #from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
    #from collective.lineage.brains import VHMAwareBrain
    #db, connection, root, root_folder = getInformationFromEvent(event)

    #for obj_id, obj in root_folder.items():
    #    if IPloneSiteRoot.providedBy(obj):
    #        catalog = getToolByName(obj, 'portal_catalog')
    #        catalog._catalog.useBrains(VHMAwareBrain)
