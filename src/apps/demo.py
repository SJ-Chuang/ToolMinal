from apps.base import AppBase

class DemoApp(AppBase):
    def __init__(self):
        super().__init__("Demo App", "Hello world", "app/demo")
        self.create_route("", methods=["GET"], view_func=self.print_demo)
    
    def print_demo(self):
        return "Hello World"