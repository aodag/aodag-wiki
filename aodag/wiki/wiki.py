import CommonMark
from zope.interface import implementer
from .interfaces import IPageRenderer


def includeme(config):
    config.register_service_factory(
        CommonmarkPageRendererFactory(),
        IPageRenderer)


class CommonmarkPageRendererFactory:
    def __init__(self):
        self.parser = CommonMark.Parser()
        self.renderer = CommonMark.HtmlRenderer()

    def __call__(self, context, request):
        return CommonmarkPageRenderer(context, self.parser, self.renderer)


@implementer(IPageRenderer)
class CommonmarkPageRenderer:
    def __init__(self, wikipage, parser, renderer):
        self.wikipage = wikipage
        self.parser = parser
        self.renderer = renderer

    @property
    def title(self):
        return self.wikipage.pagename

    @property
    def contents(self):
        ast = self.parser.parse(self.wikipage.contents)
        return self.renderer.render(ast)
