import webtest
import pytest


@pytest.fixture
def app(monkeypatch, sql_session):
    from aodag.wiki.wsgi import main
    monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)
    app = main({})
    return webtest.TestApp(app, extra_environ={'repoze.tm.active': True})


@pytest.fixture
def frontpage(app, sql_session):
    from aodag.wiki import models
    models.BaseObject.metadata.create_all()
    page = models.WikiPage.query.filter(
        models.WikiPage.pagename == 'FrontPage').first()
    if page is None:
        page = models.WikiPage(
            pagename='FrontPage',
            contents="#FrontPage",
        )
        models.Session.add(page)


def test_frontpage(app, frontpage):
    res = app.get("/")
    assert res.location == 'http://localhost/wiki/FrontPage'
    res = app.get(res.location)
    assert "<h1>FrontPage</h1>" in res, res.text


def test_edit(app):
    res = app.get("/wiki/TestPage")
    assert res.location == 'http://localhost/wiki/TestPage/edit'
    res = app.get(res.location)
    res.form["contents"] = "testing OK"
    res = res.form.submit()
    assert res.location == "http://localhost/wiki/TestPage"
    res = app.get(res.location)
    assert "testing OK" in res, res.text
