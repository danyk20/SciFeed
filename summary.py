import time

from transformers import pipeline


def get_summary(abstract):
    summarizer = pipeline("summarization", model="com3dian/Bart-large-paper2slides-expander")
    return summarizer(abstract, max_length=60, min_length=15, do_sample=False)[0]['summary_text']
