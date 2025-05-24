from summary import get_summary


class Paper:
    def __init__(self, json_element: dict) -> None:
        self.title = json_element.get('title', {}).get('title', 'Untitled Paper')
        self.abstract = json_element.get('abstract', {}).get('summary', '')
        if not self.abstract:
            print(f"Warning: No abstract found for '{self.title}'.")
        self.url = None
        pdf_files = [file for file in json_element.get('files', []) if
                     file.get('eformat') and '.pdf' in file.get('eformat').lower()]
        if pdf_files:
            self.url = pdf_files[0].get('url')
        if len(pdf_files) > 1:
            print(f"Warning: {len(pdf_files)} PDF files found for '{self.title}'. Using first other are ignored!")

        self.summary = get_summary(self.abstract) if self.abstract else "No summary available."

    def __repr__(self) -> str:
        return (
            f"{{'title': '{self.title}', "
            f"'url': '{self.url}', "
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
