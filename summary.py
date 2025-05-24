import torch
from transformers import pipeline

from config import SUMMARIZATION_MAX_LENGTH, SUMMARIZATION_MIN_LENGTH, SUMMARIZATION_SAMPLING, SUMMARIZATION_MODEL

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Using NVIDIA GPU (CUDA) for summarization.")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using Apple Silicon GPU (MPS) for summarization.")
else:
    device = torch.device("cpu")
    print("No GPU available, falling back to CPU for summarization.")

summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL, device=device)


def get_summary(abstract, max_length: int = SUMMARIZATION_MAX_LENGTH, min_length: int = SUMMARIZATION_MIN_LENGTH,
                do_sample: bool = SUMMARIZATION_SAMPLING) -> str:
    """
    Generates a summary for a given abstract string using a pre-trained summarization model.

    This function uses the Hugging Face Transformers library to perform text summarization on the provided abstract. It
    employs the "com3dian/Bart-large-paper2slides-expander" model to generate a concise summary by extracting the most
    relevant information from the input abstract within the specified length range.

    :param max_length: The maximum length (in tokens) of the generated summary.
    :param min_length: The minimum length (in tokens) of the generated summary.
    :param do_sample: Whether to use sampling for text generation.
    :param abstract: The text string containing the abstract to be summarized.
    :return: A string containing the generated summary of the input abstract.
    """
    if max_length > len(abstract.split()):
        return abstract
    return summarizer(abstract, max_length=max_length, min_length=min_length, do_sample=do_sample)[0]['summary_text']
