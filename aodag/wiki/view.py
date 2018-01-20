from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from .models import WikiPage


@view_config(route_url="top")
@view_config(route_url="wiki")
def redirect_frontpage(request):
    location = request.route_url('wikipage', pagename="FrontPage")
    return HTTPFound(location=location)


@view_config(route_url="wikipage",
             renderer="templates/wikipage.html")
def page_view(request):
    pagename = request.matchdict["pagename"]
    page = WikiPage.query.filter(WikiPage.pagename == pagename).first()
    if page is None:
        location = request.route_url('wikipage.edit', pagename="FrontPage")
        return HTTPFound(location=location)
    return dict(page=page)


@view_config(route_url="wikipage.edit",
             renderer="templates/wikipage_edit.html")
def page_edit_view(request):
    pagename = request.matchdict["pagename"]
    page = WikiPage.query.filter(WikiPage.pagename == pagename).first()
    if page is None:
        page = WikiPage(pagename=pagename)
    if request.POST:
        page.content = request.POST["content"]
    return dict(page=page)
