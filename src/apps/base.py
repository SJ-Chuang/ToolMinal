from flask import Blueprint

class AppBase:
    """
    A app base for building a new application

    Args:
        title (str): name of the app
        description (str): some information about the app
        url_prefix (str): the url prefix of this app

    Example:
        import random

        class MyApp(AppBase):
            def __init__(self):
                super().__init__("Demo App", "Print Hello world on the screen", "apps/demo")
                self.create_route("", methods=["GET"], self.index)
                self.create_route("random", methods["GET"], self.random_float)
            
            def index(self):
                return "[DEMO APP] Hello World [DEMO APP]"
            
            def random_float(self):
                return str(random.random())
    """
    def __init__(self, title: str, description: str, url_prefix: str):
        self.title = title
        self.description = description
        self.url_prefix = url_prefix.strip("/")
        self.blueprint = Blueprint(self.title, __name__, url_prefix="/" + self.url_prefix)
    
    def create_route(self, route, methods=["GET"], view_func=None):
        endpoint = route if route else "index"
        rule = "/" + route.strip("/") if route else "/"
        self.blueprint.add_url_rule(rule, endpoint=endpoint, view_func=view_func, methods=methods)
    
    
    