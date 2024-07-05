# Sentiment-Analysis-on-Web-Article-Text

## Overview
The primary objective of this assignment is to extract textual data from given URLs and perform text analysis to compute various metrics. The goal is to derive meaningful insights and sentiment scores from the articles provided in the ”Input.xlsx” file.

## Project Structure

### Data Extraction
The extraction process begins by reading URLs from an Excel file containing a list of articles. For each URL, the script sends a request to fetch the article’s content. Using BeautifulSoup, it parses the HTML to extract the title and body text of the article. The extracted title and text are then saved to a local file, with each file named according to a unique identifier from the Excel sheet. This organized storage ensures that each article’s text is readily available for subsequent analysis.

### Text Analysis
In the analysis phase, the script first loads a list of stop words, as well as sets of positive and negative words from predefined directories. It then processes each saved article, computing a range of text metrics. These metrics include sentiment scores (positive, negative, polarity, and subjectivity), readability scores (average sentence length, fog index, etc.), and other linguistic features such as word count and average word length. The computed metrics are stored in a dictionary and ultimately saved to a CSV file, providing a comprehensive dataset for further evaluation or reporting.

