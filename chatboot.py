import requests
from PyPDF2 import PdfReader

from answers import qa_model


def download_pdf_from_link(url: str, save_path: str):
    """
    Downloads a PDF file from a given URL and saves it to a specified path.

    :param url: The URL of the PDF file to download.
    :param save_path: The local path where the downloaded PDF will be saved.
    :return: None
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for unsuccessful responses

        if response.headers['content-type'] == 'application/pdf':
            with open(save_path, 'wb') as file:
                # Write the content to the file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"PDF downloaded and saved at: {save_path}")
        else:
            print("The provided URL does not point to a valid PDF file.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the PDF: {e}")


def read_pdf_from_url(url: str) -> str:
    """
    Reads the content of a PDF file from a given URL.

    This function downloads a PDF from the specified URL to a temporary location,
    then uses read_pdf_from_file() to extract and return all text content from the PDF..

    :param url: The URL of the PDF file to be read.
    :return: A string containing all extracted text from the PDF, or an empty string if an error occurs.
    """
    try:
        path = 'tmp/paper.pdf'
        download_pdf_from_link(url, path)
    except Exception as e:
        print(f"Error: {e}")
        return ""
    return read_pdf_from_file(path)


def read_pdf_from_file(path: str) -> str:
    """
    Reads the content of a PDF file from a given path.

    This uses PyPDF2 to extract and return all text content from the PDF.

    :param path: The path of the PDF file to be read.
    :return: A string containing all extracted text from the PDF, or an empty string if an error occurs.
    """
    try:
        pdf_reader = PdfReader(path)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        return pdf_text
    except Exception as e:
        print(f"Error: {e}")
        return ""


def chatbot(paper_text):
    while True:
        print("I am your personal chat-boot fell free to ask me anything related to the paper you used as input.")
        user_input = input("Your question: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        else:
            print("Give me a sec, I am thinking...")
            answers = qa_model(question=user_input, context=paper_text)
            print("Chatbot answer: " + answers['answer'])
            print("I am " + str(round(answers['score'] * 100, 2)) + '% confident')

# Example usage:
# pdf_url = "https://is.muni.cz/auth/th/n3kmo/Automated_problem_generation_for_cybersecurity_game_Daniel_Kosc.pdf"  # Replace with the actual URL of the PDF
# chatbot(read_pdf_from_url(pdf_url))
