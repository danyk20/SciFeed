import requests
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textbox']
        print(query_to_url(user_input))
        print("->" + user_input[0] + "<-")
        return render_template('feed.html', value=user_input[0])
    return render_template('index.html')


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
    urls = [''] * number_of_files
    i = 0
    for entry in jsonfile:
        for file in entry['files']:
            if file['full_name'].endswith('.pdf'):
                urls[i] = file['url']
                i += 1
        if i >= number_of_files:
            break
    return urls


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
