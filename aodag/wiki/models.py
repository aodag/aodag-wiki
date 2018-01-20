from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UnicodeText,
)
from pyramid_sqlalchemy import (
    BaseObject,
    Session,
)
from zope.interface import implementer
from .interfaces import IWikiPage


@implementer(IWikiPage)
class WikiPage(BaseObject):
    __tablename__ = "wikipages"
    query = Session.query_property()
    id = Column(Integer, primary_key=True)
    pagename = Column(Unicode(255))
    contents = Column(UnicodeText)
