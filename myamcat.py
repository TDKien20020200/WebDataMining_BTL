import json
import requests
import time
import traceback
from bs4 import BeautifulSoup
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import nltk
import os

# Setup NLTK data path
nltk_data_path = os.path.expanduser('~\\AppData\\Roaming\\nltk_data')
nltk.data.path.append(nltk_data_path)

# Check and download required NLTK datasets if needed
def setup_nltk():
    print("Setting up NLTK datasets...")
    for dataset in ['corpora/stopwords', 'tokenizers/punkt']:
        try:
            nltk.data.find(dataset)
        except LookupError:
            print(f"Downloading {dataset.split('/')[-1]}...")
            nltk.download(dataset.split('/')[-1], download_dir=nltk_data_path)

setup_nltk()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rake_nltk import Rake

# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    return ' '.join([word for word in words if word.isalnum() and word not in stop_words])

# Function to add blanks for missing fields
def add_blanks(row):
    for key in row:
        if row[key] is None:
            row[key] = ''

# Load or train a classification model
def load_or_train_model():
    print("Loading or training classification model...")
    model_path = 'job_classifier.pkl'
    if os.path.exists(model_path):
        print("Model found. Loading...")
        return joblib.load(model_path)
    
    print("No model found. Training a new model...")
    training_data = [
        {'jd': 'Software engineer with experience in Python and Django.', 'label': 'IT'},
        {'jd': 'Sales manager with experience in retail and customer relations.', 'label': 'Sales'},
        {'jd': 'Data scientist skilled in machine learning and Python.', 'label': 'IT'},
        {'jd': 'Marketing executive with expertise in digital marketing.', 'label': 'Marketing'}
    ]
    X = [preprocess_text(item['jd']) for item in training_data]
    y = [item['label'] for item in training_data]

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', MultinomialNB())
    ])
    pipeline.fit(X, y)
    joblib.dump(pipeline, model_path)
    print("Model trained and saved.")
    return pipeline

# Function to extract keywords
def extract_keywords(jd):
    rake = Rake()
    rake.extract_keywords_from_text(jd)
    return rake.get_ranked_phrases()

# Main scraping function
def scrape():
    print("Starting scraping process...")
    timestamp = time.time()
    json_filename = './files/myamcat.json'
    os.makedirs('./files/', exist_ok=True)
    headers = {
        "title": "", "applylink": "", "jd": "", "companyname": "",
        "location": "", "experience": "", "salary": "", "created": "",
        "source": "", "timestamp": "", "classification": "", "keywords": ""
    }

    joblist = []
    pipeline = load_or_train_model()  # Load or train the classification model

    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i in range(117, 120):
        url = 'https://www.myamcat.com/jobs-search-ajax?strEventID=1&strCompanyID=&strMinSalary=0&strMaxSalary=9900000&strStartLimit=0&strKeyword=&strAdvCategoryName=0&strAdvLocationID=0&strAdvSectorID=&strAdvFlagID=0&sortBy=2&strJobRolesList=&strCompaniesList=&strInvitedJobs=0&strFreeSearchText=0&strHeaderJobSearchLocation=&_=1524471212{}%20HTTP/1.1'.format(
            i)
        print(f"Fetching data from URL: {url}")
        try:
            response = requests.get(url, headers=request_headers, timeout=10)
            if response.status_code != 200:
                print(f"Error: Unable to fetch data, status code {response.status_code}")
                continue

            print(f"Response received for URL {url}. Parsing data...")
            if '<html' in response.text.lower():
                print(f"Received HTML instead of JSON for URL: {url}")
                continue

            jobs = json.loads(response.text)

            for job in jobs.get('1', []):
                try:
                    print(f"Processing job: {job.get('jobprofileName', 'Unknown Title')}")
                    row = dict.fromkeys(headers)
                    row['title'] = job.get('jobprofileName', '')
                    row['applylink'] = 'https://www.myamcat.com' + job.get('jdLink', '')
                    row['jd'] = ''.join(BeautifulSoup(job.get('description', ''), "lxml").stripped_strings).replace('\u00a0', ' ')
                    row['companyname'] = job.get('companyName', '')
                    row['location'] = job.get('cityName', '')
                    row['experience'] = f"{job.get('minJobEx', '0')} yrs"
                    row['salary'] = job.get('salary', '')
                    row['created'] = job.get('datePosted', '')
                    row['source'] = 'amcat'
                    row['timestamp'] = timestamp

                    # Preprocess JD and classify
                    preprocessed_jd = preprocess_text(row['jd'])
                    row['classification'] = pipeline.predict([preprocessed_jd])[0]

                    # Extract keywords
                    row['keywords'] = extract_keywords(row['jd'])

                    add_blanks(row)
                    joblist.append(row)

                except Exception as job_error:
                    print(f"Error processing job: {job_error}")
                    continue

        except requests.RequestException as req_error:
            print(f"Error fetching URL {url}: {req_error}")
            continue
        except json.JSONDecodeError as json_error:
            print(f"Error decoding JSON: {json_error}")
            continue

    print("Writing data to JSON file...")
    with open(json_filename, 'w') as fp:
        json.dump(joblist, fp, indent=1)
    print(f"Data written to {json_filename}")

# Run the scraping function with error handling
if __name__ == '__main__':
    try:
        scrape()
    except Exception as ex:
        with open("error.log", 'a') as errorlog:
            traceback.print_exc(file=errorlog)
        print("An error occurred. Check error.log for details.")
