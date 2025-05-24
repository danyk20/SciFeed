from summary import get_summary


class Paper:
    def __init__(self, json_element: dict) -> None:
        self.title: str = json_element.get('title', {}).get('title', 'Untitled Paper')
        abstracts: list[dict] | dict = json_element.get('abstract', {})
        if isinstance(abstracts, list):
            if abstracts:
                for abstract in abstracts:
                    self.abstract: str = abstract.get("summary", "")
                    if self.abstract:
                        break
            else:
                self.abstract: str = ""
        else:
            self.abstract: str = abstracts.get('summary', '')
        if not self.abstract:
            print(f"Warning: No abstract found for '{self.title}'.")
        self.urls: list[str] = []
        pdf_files: list = [file for file in json_element.get('files', []) if
                           file.get('eformat') and '.pdf' in file.get('eformat').lower()]
        for pdf_file in pdf_files:
            self.urls.append(pdf_file.get('url'))
        self.summary: str = get_summary(self.abstract) if self.abstract else "No summary available."

    def __repr__(self) -> str:
        return (
            f"{{'title': '{self.title}', "
            f"'url': '{self.urls}', "
            f"'summary': '{self.summary}'}}"
        )


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
