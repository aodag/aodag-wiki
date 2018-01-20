class WikiResource:
    def __init__(self, request):
        self.request = request

    @property
    def front_page_name(self):
        reg = self.request.registry
        return reg.settings.get("aodag.wiki.frontpage_name", "FrontPage")
