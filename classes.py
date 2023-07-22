
class Paper():
    def __init__(self, jsonelement) -> None:

        self.title = jsonelement['title']['title']
        self.abstract = jsonelement['abstract']['summary']
        files = jsonelement['files']
        for file in files:
            if file['full_name'].endswith('.pdf'):
                self.url = file['url']
    
    def __repr__(self) -> str:
        return f'Paper({self.title} at {self.url})'
    