import pytest
from pyramid import testing
import pyramid.request

@pytest.fixture
def config():
    c = testing.setUp()
    try:
        yield c
    finally:
        testing.tearDown()


def test_page_renderer(config):
    from aodag.wiki.interfaces import IPageRenderer
    from aodag.wiki.wiki import CommonmarkPageRendererFactory
    config.include('pyramid_services')
    config.include('aodag.wiki.wiki')
    request = testing.DummyRequest()
    pyramid.request.apply_request_extensions(request)
    renderer = request.find_service_factory(IPageRenderer)
    assert renderer
    assert isinstance(renderer, CommonmarkPageRendererFactory)
    page = testing.DummyResource(contents="""\
# this is page

ok page
    """)
    page_renderer = request.find_service(IPageRenderer, context=page)
    assert page_renderer.contents == "<h1>this is page</h1>\n<p>ok page</p>\n"
