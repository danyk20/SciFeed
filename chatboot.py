import requests
from PyPDF2 import PdfReader

from answers import qa_model


def download_pdf_from_link(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for unsuccessful responses

        # Check if the response content is PDF data
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


def read_pdf_from_url(url):
    try:
        path = 'tmp/paper.pdf'
        download_pdf_from_link(url, path)

        # Initialize PyPDF2 PdfReader to read the PDF content
        pdf_reader = PdfReader(path)

        # Extract text from all pages
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
