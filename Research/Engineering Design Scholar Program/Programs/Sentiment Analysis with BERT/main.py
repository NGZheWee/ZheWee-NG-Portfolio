import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import matplotlib.pyplot as plt
import seaborn as sns
import re
from tqdm import tqdm

# File path
#file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with BERT\\data\\BIFMA Merged.xlsx'
#file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with BERT\\data\\Blue Angel Merged.xlsx'
#file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with BERT\\data\\Fair For Life Merged.xlsx'
#file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with BERT\\data\\FSC Merged.xlsx'
file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with BERT\\data\\Recycled Claim Standard 100 Merged.xlsx'


# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load the sheet into a dataframe
df = pd.read_excel(xls, sheet_name='Sheet1')

# Ensure all entries in 'content' column are strings
df['content'] = df['content'].astype(str)

# Load pre-trained BERT tokenizer and model for sentiment analysis
tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Function to get sentiment scores using BERT
def get_sentiment_score(review):
    try:
        inputs = tokenizer(review, return_tensors='pt', truncation=True, padding=True, max_length=512)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        outputs = model(**inputs)
        scores = outputs.logits.detach().cpu().numpy()
        sentiment = scores.argmax(axis=1)[0]
        return sentiment - 2  # Adjusting to range [-2, 2] to align with VADER's compound score range
    except Exception as e:
        print(f"Error processing review: {review[:30]}... Error: {e}")
        return None

# Apply sentiment analysis on the reviews with progress bar
tqdm.pandas()
df['sentiment'] = df['content'].progress_apply(get_sentiment_score)

# Function to clean price strings and convert to float
def clean_price(price):
    if isinstance(price, str):
        try:
            # Extract the first valid float number from the string
            return float(re.findall(r'\d+\.\d+', price.replace('$', ''))[0])
        except (IndexError, ValueError):
            return None
    else:
        return None

# Apply the cleaning function to the 'price' column
df['price'] = df['price'].apply(clean_price)

# Ensure 'rating_x', 'rating_y', and 'number_of_reviews' are numerical values
df['rating_x'] = df['rating_x'].str.extract(r'(\d+\.\d+)').astype(float)
df['rating_y'] = df['rating_y'].str.extract(r'(\d+\.\d+)').astype(float)
df['number_of_reviews'] = df['number_of_reviews'].str.extract(r'(\d+)').astype(int)

# Remove non-numeric 'product_dimensions' from columns of interest
columns_of_interest = [
    'sentiment',
    'rating_x', 'rating_y', 'price',
    'number_of_reviews'
]

# Compute correlation matrix
correlation_matrix = df[columns_of_interest].corr()

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix between Sentiment, Certification, and Product Attributes')
plt.show()

# Save the updated dataframe to a new Excel file
#new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with BERT/results/BIFMA_with_BERT_Sentiment.xlsx'
#new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with BERT/results/Blue Angel_with_BERT_Sentiment.xlsx'
#new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with BERT/results/Fair For Life_with_BERT_Sentiment.xlsx'
#new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with BERT/results/FSC_with_BERT_Sentiment.xlsx'
new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with BERT/results/Recycled Claim Standard 100_with_BERT_Sentiment.xlsx'
df.to_excel(new_file_path, sheet_name='Sheet1', index=False)

# Display the first few rows of the final dataframe for verification
print(df.head())
