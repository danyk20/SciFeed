# SciFeed (Research Assistant Web Application)

## Project Overview

This project provides a web-based research assistant application designed to streamline the process of finding and
interacting with academic papers and videos. Leveraging the CERN Document Server (CDS) as its primary data source, the
application allows users to search for relevant research materials, view summarized abstracts, and engage in a
question-answering dialogue with the content of uploaded or linked PDF documents.

The application features:

* **Content Search:** Search for academic papers and videos from the CERN Document Server.

* **Abstract Summarization:** Automatically generates concise summaries for research paper abstracts to quickly grasp
  key information.

* **Interactive Chatbot:** Upload a PDF or provide a URL to a PDF, and then ask questions directly to the document's
  content. The chatbot provides answers along with a confidence score and highlights the relevant snippet from the text.

This tool is ideal for researchers, students, and anyone looking to efficiently navigate and comprehend scientific
literature and presentations.

## Getting Started

Follow these steps to set up and run the Research Assistant Web Application on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.10+**: This project is built with Python. You can download it
  from [python.org](https://www.python.org/downloads/).

* **pipenv**: This tool helps manage project dependencies. If you don't have it, install it using pip:

    ```shell
    pip install pipenv
    ```

### Installation

1. **Clone the Repository:**
   Clone it to your local machine:
   ```shell
   git clone https://github.com/danyk20/SciFeed.git
   ```

2. **Navigate to the Project Directory:**

   ```shell
   cd SciFeed
   ```
3. **Install Dependencies:**
   This project uses `pipenv` for dependency management. The `Pipfile` and `Pipfile.lock` files define the exact
   versions of libraries required.

   ```shell
   pipenv install
   ```
   This command will create a virtual environment for your project and install all dependencies listed in
   `Pipfile.lock`.

4. **Activate the Virtual Environment:**
   ```shell
   pipenv shell
   ```

   You should see `(SciFeed)` or a similar prefix in your terminal prompt, indicating that the virtual
   environment is active. All subsequent Python commands will use the packages installed within this environment.

### Running the Application

1. **Start the Flask Server:**
   With the virtual environment activated, run the main application file:
   ```shell
   python app.py
   ```
   You will see output indicating that the Flask development server is running, typically on `http://127.0.0.1:5000/` or
   `http://localhost:5000/`.

2. **Access the Application:**
   Open your web browser and navigate to the address provided in the terminal (e.g., `http://127.0.0.1:5000/`).

### How to Use

#### 1. Searching for Papers and Videos

* On the main page, you will find a search bar.

* Enter your research query (e.g., "Higgs boson", "quantum entanglement", "dark matter").

* Press Enter or click the search button.

* The application will display a list of relevant papers and videos from the CERN Document Server, along with their
  summaries.

#### 2. Interacting with the Chatbot

* Navigate to the "Ask" section of the application (accessible via a [link](http://127.0.0.1:5000/ask) or button on the
  Feed page).

* You will have two options to provide a document:

* **Upload a PDF File:** Click the `Choose File` button and select a PDF document from your local computer.

* **Provide a PDF URL:** Enter the direct URL to a PDF file hosted online.

* Once the document is loaded (either uploaded or from URL), you can type your questions into the chat input field.

* The chatbot will process your question against the content of the loaded PDF and provide an answer, a confidence
  score, and highlight the relevant text snippet from the document.

## Project Structure

* `app.py`: The main Flask application file, handling routes and rendering templates.

* `chatboot.py`: Contains functions for downloading and reading PDF files, and the question-answering model integration.

* `classes.py`: Defines Python classes for `Paper` and `Video` objects, used to structure data retrieved from CDS.

* `config.py`: Stores configuration variables such as model names, API URLs, and result limits.

* `requirements.txt`: Lists Python dependencies for the project. (Note: `Pipfile` and `Pipfile.lock` are preferred for
  `pipenv`.)

* `summary.py`: Implements the abstract summarization functionality using a pre-trained model.

* `utils.py`: Provides utility functions for querying the CERN Document Server and processing its responses.

* `Pipfile`: Defines project dependencies for `pipenv`.

* `Pipfile.lock`: Locks the exact versions of dependencies for reproducible builds.

## Contributing

SciFeed was born as a winning project at the **CERN Webfest 2023** hackathon. This event brought together bright young
individuals to develop innovative applications supporting science, research, and education. The judges highly praised
SciFeed for its strong technical implementation and significant educational value for the wider community.

We are incredibly grateful for the contributions of the following individuals who made SciFeed a reality:

- Daniel Kosc
- Viona Cufo 
- Kristupa Seskauskaite
- Marta Adamina Krawczyk 
- Peter Blum
- Shrishti Kulkarni


## License

This project is shared under the **MIT License**.