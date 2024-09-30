import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Load data
file_path = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA\data\FSC_with_BERT_Sentiment.xlsx'
df = pd.read_excel(file_path)

# Extract relevant columns
df = df[['product_id', 'name', 'description', 'sustainability_features', 'content']]

# Clean text data
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

df['content'] = df['content'].apply(clean_text)

# Vectorize customer reviews
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
X = vectorizer.fit_transform(df['content'])

# Apply LDA
lda = LatentDirichletAllocation(n_components=10, random_state=42)
lda.fit(X)

# Extract topics
def display_topics(model, feature_names, no_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
    return topics

topics = display_topics(lda, vectorizer.get_feature_names_out(), 10)
print("Extracted Topics:", topics)

# Save extracted topics to a file with UTF-8 encoding
topics_path = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA\results\FSC_Extracted_Topics.txt'
with open(topics_path, 'w', encoding='utf-8') as f:
    for idx, topic in enumerate(topics):
        f.write(f"Topic {idx + 1}: {topic}\n")

# Define the new aspects and their related keywords
aspects = {
    'General Sustainability': [
        'benefit', 'certification', 'circular economy', 'eco-conscious', 'eco-friendly',
        'eco-label', 'eco-material', 'eco-product', 'eco-technology', 'ecoconscious',
        'ecofriendly', 'ecolabel', 'ecological', 'ecology', 'ecomaterial', 'ecoproduct',
        'environment', 'environmental', 'environmentally friendly', 'impact', 'nature',
        'preventing', 'protection', 'reduce', 'reducing', 'reduction', 'saving', 'savings',
        'sustainability', 'sustainable', 'sustainable design'
    ],
    'Material: Bio Friendly': [
        'PET', 'PVC', 'bio-based', 'bio-degradable', 'bio-material', 'bio-plastic',
        'bio-product', 'biobased', 'biodegradable', 'biomaterial', 'bioplastic', 'compost',
        'degradation', 'green label', 'green material', 'green product', 'green technology',
        'microplastic', 'natural resource', 'plastic free', 'plastic pollution', 'plastic waste',
        'pollution', 'pollution prevention', 'polyethylene terephthalate', 'polypropylene',
        'polystyrene', 'polyvinyl chloride', 'use plastic', 'water'
    ],
    'Material: Chemical Contents': [
        'chemical free', 'chemical-free', 'organic'
    ],
    'Material: Recyclability': [
        'closed loop', 'closed-loop', 'cradle to cradle', 'cradle to grave', 'cradle-to-cradle',
        'cradle-to-grave', 'reclaimed', 'recover', 'recovered', 'recovery', 'recycle',
        'recycled', 'recycling', 'refurbished', 'refurbishing', 'reman', 'remanufacture',
        'remanufactured', 'renewable', 'repair', 'repurpose', 'restorative', 'reuse', 'reused',
        'reusing', 'single use', 'single-use'
    ],
    'Material: Waste': [
        'conservation', 'conserving', 'disposal', 'waste', 'zero waste'
    ],
    'Energy: Consumption': [
        'consume', 'consumer', 'efficiency', 'efficient', 'energy', 'energy consumption',
        'energy saving', 'energy savings', 'phantom load', 'power consumption'
    ],
    'Energy: Renewability': [
        'bio-diesel', 'bio-energy', 'bio-fuel', 'biodiesel', 'bioenergy', 'biofuel', 'solar'
    ],
    'Environment: Bioenvironment': [
        'bio-diversity', 'biodiversity'
    ],
    'Environment: Climate': [
        'carbon', 'carbon neutral', 'climate', 'climate action', 'climate crisis',
        'emission', 'footprint', 'global warming', 'greenhouse', 'landfill', 'net-zero',
        'ozone layer', 'zero carbon'
    ],
    'Environment: Soil': [
        'acidification'
    ],
    'Product: Price': [
        'cheap', 'cheaper'
    ],
    'Product: Quality': [
        'brake', 'broke', 'broken', 'crash', 'crashed', 'die', 'died', 'durability', 'durable',
        'dying', 'garbage', 'last long', 'life cycle', 'lifecycle', 'lifespan', 'lifetime',
        'maintainable', 'maintenance', 'stop work', 'stopped working', 'take back', 'take-back',
        'tear', 'useless', 'wear'
    ],
    'Manufacturing Process': [
        'cleaner production', 'deforestation', 'dematerialisation', 'dematerialization',
        'eco-design', 'ecodesign', 'fair trade'
    ]
}

# Function to map topics to aspects
def map_topics_to_aspects(review, aspects):
    aspect_mentions = {aspect: 0 for aspect in aspects}
    for aspect, keywords in aspects.items():
        if any(keyword in review for keyword in keywords):
            aspect_mentions[aspect] += 1
    return aspect_mentions

# Apply aspect mapping with progress bar
tqdm.pandas(desc="Performing Topic Modelling")
df['aspect_mentions'] = df['content'].progress_apply(lambda x: map_topics_to_aspects(x, aspects))

# Load pre-trained sentiment-analysis pipeline with specified model and revision
model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
model_revision = "af0f99b"
sentiment_analysis = pipeline('sentiment-analysis', model=model_name, revision=model_revision)

# Function to extract aspect-specific sentiment
def extract_aspect_sentiment(review, aspects):
    max_len = 512
    if len(review) > max_len:
        review = review[:max_len]
    aspect_sentiments = {}
    for aspect, keywords in aspects.items():
        if any(keyword in review for keyword in keywords):
            aspect_sentiments[aspect] = sentiment_analysis(review)[0]['label']
    return aspect_sentiments

# Apply aspect-based sentiment analysis with progress bar
tqdm.pandas(desc="Performing Sentiment Analysis")
df['aspect_sentiments'] = df['content'].progress_apply(lambda x: extract_aspect_sentiment(x, aspects))

# Example: Show aspect sentiments for the first few reviews
print(df[['content', 'aspect_mentions', 'aspect_sentiments']].head())

# Function to count sentiments for each aspect
def count_aspect_sentiments(df, aspects):
    sentiment_counts = {aspect: {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0} for aspect in aspects}
    for sentiments in df['aspect_sentiments']:
        for aspect, sentiment in sentiments.items():
            sentiment_counts[aspect][sentiment] += 1
    return sentiment_counts

# Count aspect sentiments
aspect_sentiment_counts = count_aspect_sentiments(df, aspects)

# Visualize aspect sentiment distribution
for aspect, counts in aspect_sentiment_counts.items():
    sns.barplot(x=list(counts.keys()), y=list(counts.values()))
    plt.title(f'Sentiment Distribution for {aspect}')
    plt.show()

# Save results to an Excel file
results_path = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA\results\FSC_with_ABSA.xlsx'
df.to_excel(results_path, index=False)
