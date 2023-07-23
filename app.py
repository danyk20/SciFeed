import requests
from flask import Flask, request, render_template

from answers import qa_model
from chatboot import read_pdf_from_url, download_pdf_from_link
from classes import Paper

app = Flask(__name__)
# pdf_url = "https://cds.cern.ch/record/2863895/files/2307.01612.pdf"  # Replace with the actual URL of the PDF



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textbox']
        paper_urls = query_to_url(user_input)
        return render_template('feed.html', value=paper_urls)
    return render_template('index.html')

@app.route('/ask')
def ask():
    return render_template('ask.html')


@app.route('/moodBoard', methods=['GET', 'POST'])
def mood():
    return render_template('mood_board.html')

@app.route('/chat', methods=['POST'])
def chat():
    paper_text = read_pdf_from_url(request.form['paper_url'])
    user_input = request.form['user_input']
    if user_input.lower() == "exit":
        response = "Chatbot: Goodbye!"
    else:
        answers = qa_model(question=user_input, context=paper_text)
        response = "Chatbot answer: " + answers['answer']
        response += " - I am " + str(round(answers['score'] * 100, 2)) + '% confident with that answer'
    return render_template('chat.html', response=response)

def get_html():
    file_path = "templates/index.html"

    try:
        with open(file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading the file '{file_path}'.")
    return content


def query_cds(query, videos=False):
    """query the Cern Document Server using an HTTP request. Can be toggled to request videos or papers."""
    params = {"p": query, "of": "recjson"}
    if videos:
        params["c"] = "Presentations & Talks"

    response = requests.get('https://cds.cern.ch//search', params=params)

    # never got a different response code but it is probably good to test for it anyways
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def get_pdfs_from_json(jsonfile, number_of_files=5):
    """get the first n pdf urls from the search response"""
    papers = []
    for entry in jsonfile:
        try:
            paper = Paper(entry)
            if paper.url:
                papers.append(paper)
            if len(papers) == number_of_files:
                break
        except KeyError:
            pass
        
    return papers


def get_videos_from_json(jsonfile, number_of_files=5, ):
    """get the first n video urls from the search response"""
    urls = [''] * number_of_files
    i = 0
    for entry in jsonfile:
        try:
            if 'video' in entry['medium']['material']:
                urls[i] = entry['electronic_location'][1]['uri']
                i += 1
        except KeyError:
            pass
        if i == number_of_files:
            break
    return urls


def query_to_url(query, videos=False, number_of_results=5):
    """returns the file urls of the first 'number_of_results' results, should be <=10
    Can be toggled to either return pdfs or video urls"""
    jsonfile = query_cds(query, videos=videos)
    if videos:
        return get_videos_from_json(jsonfile, number_of_files=number_of_results)
    else:
        return get_pdfs_from_json(jsonfile, number_of_files=number_of_results)


app.run()
