import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Download the VADER lexicon
nltk.download('vader_lexicon')

# File path
file_path = 'D:\\OneDrive\\UC Berkeley\\Engineering Design Scholar Program\\Programs\\Sentiment Analysis with VADER\\data\\Recycled Claim Standard 100 Merged.xlsx'

# Load the Excel file
xls = pd.ExcelFile(file_path)

# Load the sheet into a dataframe
df = pd.read_excel(xls, sheet_name='Sheet1')

# Ensure all entries in 'content' column are strings
df['content'] = df['content'].astype(str)

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Apply sentiment analysis on the reviews
df['sentiment'] = df['content'].apply(lambda review: sid.polarity_scores(review)['compound'])

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
new_file_path = 'D:/OneDrive/UC Berkeley/Engineering Design Scholar Program/Programs/Sentiment Analysis with VADER/results/Recycled Claim Standard 100_with_VADER_Sentiment.xlsx'
df.to_excel(new_file_path, sheet_name='Sheet1', index=False)

# Display the first few rows of the final dataframe for verification
print(df.head())
