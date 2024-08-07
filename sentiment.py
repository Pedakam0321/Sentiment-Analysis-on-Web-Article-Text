
import pandas as pd
import requests
from bs4 import BeautifulSoup

file_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/Input.xlsx"
data = pd.read_excel(file_path)

def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article title
    title = soup.find('h1')
    title_text = title.get_text(strip=True) if title else 'No Title'

    # Extract the article body
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])

    return title_text, article_text

import os

# Define the directory where you want to save the files
extracted_articles = '/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/extracted_articles'


# Loop through the DataFrame as before
for index, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    try:
        title, article_text = extract_article_text(url)
        full_text = f"{title}\n\n{article_text}"

        # Modify the path where the file will be saved
        file_path = os.path.join(extracted_articles, f"{url_id}.txt")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(full_text)

        print(f"Successfully extracted and saved article {url_id}")
    except Exception as e:
        print(f"Failed to extract article {url_id}: {e}")

print("Article extraction completed.")

pip install pandas openpyxl nltk textstat

import os
import pandas as pd
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from textstat import textstat
import nltk

# Download necessary NLTK data
nltk.download('punkt')


# Define paths
extracted_articles_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/extracted_articles"  # Directory where article text files are stored
stopwords_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/StopWords"  # Directory containing stop words files
master_dict_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/MasterDictionary"  # Path containing positive and negative words

# Load stop words
stop_words = set()
for file in os.listdir(stopwords_path):
    if file.endswith(".txt"):
        with open(os.path.join(stopwords_path, file), 'r', encoding='latin-1') as f:
            stop_words.update(f.read().splitlines())

# Load positive and negative words
positive_words = set()
negative_words = set()
with open(os.path.join(master_dict_path, "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/MasterDictionary/positive-words.txt"), 'r', encoding='latin-1') as f:
    positive_words.update(f.read().splitlines())
with open(os.path.join(master_dict_path, "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/MasterDictionary/negative-words.txt"), 'r', encoding='latin-1') as f:
    negative_words.update(f.read().splitlines())

import os

# Function to compute text metrics
def compute_metrics(text):
    blob = TextBlob(text)
    words = blob.words
    sentences = blob.sentences

    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    avg_sentence_length = len(words) / len(sentences)
    complex_words = [word for word in words if len(dic.inserted(word).split('-')) > 2]
    percentage_complex_words = len(complex_words) / len(words) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = avg_sentence_length
    complex_word_count = len(complex_words)
    word_count = len(words)
    syllables_per_word = sum(len(dic.inserted(word).split('-')) for word in words) / len(words)
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in words) / len(words)

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllables_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length,
    }


# Path to the folder containing the articles
extracted_articles_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/extracted_articles"  # Directory where article text files are stored


# Dictionary to store metrics for each article
all_article_metrics = {}

# Loop through each file in the folder
for filename in os.listdir(extracted_articles_path):
    if filename.endswith(".txt"):  # Assuming all files are text files
        file_path = os.path.join(extracted_articles_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
            metrics = compute_metrics(article_text)
            all_article_metrics[filename] = metrics

# Print metrics for each article
for article, metrics in all_article_metrics.items():
    print(f"Metrics for {article}:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    print("\n")

import csv

def save_to_csv(metrics_data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Article'] + list(metrics_data[list(metrics_data.keys())[0]].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article, metrics in metrics_data.items():
            row = {'Article': article}
            row.update(metrics)
            writer.writerow(row)


# Path to the output CSV file
output_csv_path = '/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/Output Data Structure.csv'

# Save the metrics to CSV
save_to_csv(all_metrics, output_csv_path)

import csv
import os
import pandas as pd

# Function to save metrics to a CSV file
def save_to_csv(metrics_data, output_file):
    fieldnames = ["URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
                  "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE",
                  "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"]

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url_id, metrics in metrics_data.items():
            writer.writerow(metrics)

# Path to the folder containing the articles
extracted_articles_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/extracted_articles"  # Directory where article text files are stored

# Dictionary to store metrics for each article
all_article_metrics = {}

# Read the URL_ID and URL columns from the Excel file
input_excel_path = "/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/Input.xlsx"
df = pd.read_excel(input_excel_path)
input_data = dict(zip(df['URL_ID'], df['URL']))

# Loop through each file in the folder
for filename in os.listdir(extracted_articles_path):
    if filename.endswith(".txt"):  # Assuming all files are text files
        file_path = os.path.join(extracted_articles_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            article_text = file.read()
            metrics = compute_metrics(article_text)
            # Get the URL and URL_ID from the dictionary
            url_id = filename.split('.')[0]  # Example: If filename is 'article1.txt', url_id will be 'article1'
            metrics['URL_ID'] = url_id
            metrics['URL'] = input_data.get(url_id, '')  # Get the URL corresponding to the URL_ID
            all_article_metrics[url_id] = metrics

# Path to the output CSV file
output_csv_path = '/content/drive/MyDrive/Test Assignment-blockoffer/20211030 Test Assignment/Output Data Structure.csv'

# Save the metrics to CSV
save_to_csv(all_article_metrics, output_csv_path)
