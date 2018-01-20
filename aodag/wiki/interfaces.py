from zope.interface import Interface, Attribute


class IWikiPage(Interface):
    pagename = Attribute("pagename")
    contents = Attribute("contents")


class IPageRenderer(Interface):
    page = Attribute("page")
    title = Attribute("title of page")
    contents = Attribute("html contents of page")
