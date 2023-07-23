from summary import get_summary


class Paper():
    def __init__(self, jsonelement) -> None:

        self.title = jsonelement['title']['title']
        abstract = self.title
        try:
            abstract = jsonelement['abstract']['summary']
        except Exception as e:
            print('No abstract')
        self.abstract = abstract
        self.url = None
        self.summary = get_summary(self.abstract)
        files = jsonelement['files']
        for file in files:
            if file['full_name'].endswith('.pdf'):
                self.url = file['url']

    def __repr__(self) -> str:
        return f"\{'title':'{self.title}',  'url':'{self.url}', 'summary':{self.summary}\}"

class Video():
    def __init__(self, jsonelement) -> None:

        self.title = jsonelement['title']['title']
        # to fix abstract = none
        self.abstract = jsonelement['abstract']['summary']
        self.urls = []
        media = jsonelement['electronic_location']
        for file in media:
            try:
                if file['uri'].endswith('.mp4'):
                    self.urls.append(file['uri'])
            except KeyError:
                pass
        self.url = self.urls[0] if len(self.urls) > 0 else None

    def __repr__(self) -> str:
        return f"\{'title':'{self.title}',  'url':'{self.url}'\}"
