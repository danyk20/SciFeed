from typing import List

from flask import Flask, request, render_template

from chatboot import read_pdf_from_url, read_pdf_from_file, qa_model
from classes import Paper, Video
from config import NUMBER_OF_PAPERS, NUMBER_OF_VIDEOS
from utils import query_to_url

app = Flask(__name__)


# pdf_url = "https://cds.cern.ch/record/2863895/files/2307.01612.pdf"  # Replace with the actual URL of the PDF


@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    if request.method == 'POST':
        user_input: str = request.form['textbox']
        paper_urls: List[Paper] = query_to_url(user_input, NUMBER_OF_PAPERS)
        video_urls: List[Video] = query_to_url(user_input, NUMBER_OF_VIDEOS, videos=True)
        return render_template('feed.html', papers=paper_urls, videos=video_urls)
    return render_template('index.html')


@app.route('/ask')
def ask() -> str:
    return render_template('ask.html')


@app.route('/moodBoard', methods=['GET', 'POST'])
def mood() -> str:
    return render_template('mood_board.html')


@app.route('/chat', methods=['POST'])
def chat() -> str:
    paper_input_type = request.form['paper_input_type']
    if paper_input_type == "url":
        paper_text = read_pdf_from_url(request.form['paper_url'])
    elif paper_input_type == 'file':
        path = request.files['paper_file']
        paper_text = read_pdf_from_file(path)
    else:
        print("Unsupported input type.")
        paper_text = ""
    user_input = request.form['user_input']
    if user_input.lower() == "exit":
        response = "Chatbot: Goodbye!"
    else:
        answers = qa_model(question=user_input, context=paper_text)
        response = user_input + " -> Chatbot answer: " + answers['answer']
        response += " [" + str(round(answers['score'] * 100, 2)) + '% confidence]'
    return render_template('chat.html', response=response)


app.run()
