import os
from typing import List, Dict, Any

import requests

from classes import Paper, Video
from config import NUMBER_OF_PAPERS, NUMBER_OF_VIDEOS, CERN_DOCUMENT_SERVER_URL, REQUESTED_RESULTS, TMP_FOLDER


def get_html() -> str:
    file_path = "templates/index.html"

    try:
        with open(file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading the file '{file_path}'.")
    return content


def query_cds(query: str, videos: bool = False) -> List[Dict[str, Any]]:
    """
    Queries the CERN Document Server (CDS) for research papers or videos.

    This function sends an HTTP GET request to the CDS search API.
    It can be configured to search specifically for videos (presentations and talks)
    or for general documents (papers).

    :param query: The search string to be used for the query (e.g., "Higgs boson").
    :param videos: If set to `True`, the query will be restricted to "Presentations & Talks".
                   If `False` (default), it will search for all document types.
    :return: A JSON object containing the search results if the request is successful (status code 200).
             Returns `None` and prints an error message if the request fails.
    """
    params = {"p": query, "of": "recjson", "rg": REQUESTED_RESULTS}
    if videos:
        params["c"] = "Presentations & Talks"

    response = requests.get(CERN_DOCUMENT_SERVER_URL, params=params)

    # never got a different response code, but it is probably good to test for it anyway
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def get_pdfs_from_json(jsonfile: List[Dict[str, Any]], number_of_files: int = NUMBER_OF_PAPERS) -> List[Paper]:
    """
    Extracts a specified number of Paper objects with valid PDF URLs from a CDS search response.

    This function iterates through a list of JSON entries (typically from the CERN Document Server API response) and
    attempts to create `Paper` objects from each. It collects `Paper` objects that have a valid URL until the desired
    number of files is reached or all entries have been processed.

    :param jsonfile: A list of dictionaries, where each dictionary represents a document entry
                     from the CDS search API response. Each entry is expected to potentially
                     contain information from which a `Paper` object can be initialized,
                     including a URL.
    :param number_of_files: The maximum number of `Paper` objects (with valid URLs) to retrieve.
                            Default is 5.
    :return: A list of `Paper` objects, each containing a URL to a PDF document.
             The list will contain at most `number_of_files` elements.
             Returns an empty list if no valid papers are found or if `jsonfile` is empty.
    """
    papers: List[Paper] = []
    for entry in jsonfile:
        try:
            paper = Paper(entry)
            if paper.urls:
                papers.append(paper)
            else:
                print("Skipping because there is no PDF to display for: " + paper.title)
            if len(papers) == number_of_files:
                break
        except Exception as e:
            print(f"Error: {e}")
            print(f"The problematic entry was:: {entry}. Skipping this entry.")
    return papers


def get_videos_from_json(jsonfile, number_of_files=NUMBER_OF_VIDEOS) -> List[Video]:
    """get the first n video urls from the search response"""
    videos: list[Video] = []
    for entry in jsonfile:
        try:
            video = Video(entry)
            if video.url:
                videos.append(video)
            if len(videos) == number_of_files:
                break
        except KeyError:
            pass
    return videos


def save_and_get_path(file_storage_object):
    """
    Saves a FileStorage object to the specified upload folder and returns its path.

    :param file_storage_object: The werkzeug.datastructures.FileStorage object.

    :returns: The full path to the saved file, or None if no file was provided.
    """
    file_path = os.path.join(TMP_FOLDER, file_storage_object.filename)
    os.makedirs(TMP_FOLDER, exist_ok=True)
    file_storage_object.save(file_path)
    return file_path


def query_to_url(query: str, number_of_results: int, videos=False) -> List[Paper | Video]:
    """returns the file urls of the first 'number_of_results' results, should be <=10
    Can be toggled to either return PDFs or video urls"""
    jsonfile = query_cds(query, videos=videos)
    if videos:
        return get_videos_from_json(jsonfile, number_of_files=number_of_results)
    else:
        return get_pdfs_from_json(jsonfile, number_of_files=number_of_results)