from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from .interfaces import IPageRenderer
from .models import WikiPage, Session


@view_config(route_name="top")
@view_config(route_name="wiki")
def redirect_frontpage(request):
    location = request.route_url('wikipage',
                                 pagename=request.context.front_page_name)
    return HTTPFound(location=location)


@view_config(route_name="wikipage",
             renderer="templates/wikipage.html")
def page_view(request):
    pagename = request.matchdict["pagename"]
    page = WikiPage.query.filter(WikiPage.pagename == pagename).first()
    if page is None:
        location = request.route_url('wikipage.edit', pagename=pagename)
        return HTTPFound(location=location)
    return dict(page=request.find_service(IPageRenderer, context=page))


@view_config(route_name="wikipage.edit",
             renderer="templates/wikipage_edit.html")
def page_edit_view(request):
    pagename = request.matchdict["pagename"]
    page = WikiPage.query.filter(WikiPage.pagename == pagename).first()
    if page is None:
        page = WikiPage(pagename=pagename)
    if request.POST:
        page.contents = request.POST["contents"]
        location = request.route_url('wikipage', pagename=pagename)
        Session.add(page)
        Session.flush()
        return HTTPFound(location=location)

    return dict(page=page)
