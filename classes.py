from summary import get_summary


class Paper:
    def __init__(self, json_element) -> None:

        self.title = json_element['title']['title']
        abstract = ""
        try:
            abstract = json_element['abstract']['summary']
        except Exception as e:
            print('No abstract for ' + self.title)
        self.abstract = abstract
        self.url = None
        self.summary = get_summary(self.abstract)
        files = json_element['files']
        for file in files:
            if file['full_name'].endswith('.pdf'):
                self.url = file['url']

    def __repr__(self) -> str:
        return f"{'title':'{self.title}',  'url':'{self.url}', 'summary':{self.summary}}"

class Video:
    def __init__(self, json_element) -> None:

        self.title = json_element['title']['title']
        # to fix abstract = none
        self.abstract = json_element['abstract']['summary']
        self.urls = []
        media = json_element['electronic_location']
        for file in media:
            try:
                if file['uri'].endswith('.mp4'):
                    self.urls.append(file['uri'])
            except KeyError:
                pass
        self.url = self.urls[0] if len(self.urls) > 0 else None

    def __repr__(self) -> str:
        return f"{'title':'{self.title}',  'url':'{self.url}'}"
