from pyramid.config import Configurator


def includeme(config):
    config.add_route('top', '/')
    config.add_route('wiki', '/wiki')
    config.add_route('wikipage', '/wiki/{pagename}')
    config.add_route('wikipage.edit', '/wiki/{pagename}/edit')
    config.scan(".views")


def main(global_conf, **settings):
    config = Configurator(
        settings=settings,
        root_factory=".resources.WikiResource",
    )
    config.include("pyramid_jinja2")
    config.include("pyramid_tm")
    config.include("pyramid_sqlalchemy")
    config.include("pyramid_services")
    config.include(".wsgi")
    config.include(".wiki")
    config.add_jinja2_renderer(".html")
    return config.make_wsgi_app()
