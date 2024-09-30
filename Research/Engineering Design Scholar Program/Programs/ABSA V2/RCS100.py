import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm

# Load data (MODIFY HERE ACROSS CERTIFICATIONS)
file_path = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA V2\data\Recycled Claim Standard 100_with_BERT_Sentiment.xlsx'
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

# Define the new aspects and their related keywords
aspects = {
    'General Sustainability': [
        'benefit', 'certification', 'circular economy', 'eco-conscious', 'eco-friendly', 'eco-label', 'eco-material',
        'eco-product', 'eco-technology', 'ecoconscious', 'ecofriendly', 'ecolabel', 'ecological', 'ecology',
        'ecomaterial', 'ecoproduct', 'environment', 'environmental', 'environmentally friendly', 'impact', 'nature',
        'preventing', 'protection', 'reduce', 'reducing', 'reduction', 'saving', 'savings', 'sustainability',
        'sustainable', 'sustainable design', 'conservation', 'planet-friendly'
    ],

    'Material: Bio-Friendliness': [
        'PET', 'PVC', 'bio-based', 'bio-degradable', 'bio-material', 'bio-plastic', 'bio-product', 'biobased',
        'biodegradable', 'biomaterial', 'bioplastic', 'compost', 'degradation', 'green label', 'green material',
        'green product', 'green technology', 'microplastic', 'natural resource', 'plastic free', 'plastic pollution',
        'plastic waste', 'pollution', 'pollution prevention', 'polyethylene terephthalate', 'polypropylene',
        'polystyrene', 'polyvinyl chloride', 'use plastic', 'water', 'bio-compostable'
    ],

    'Material: Chemical Contents': [
        'chemical free', 'chemical-free', 'organic', 'chemical', 'toxic', 'phthalate-free', 'VOC-Free',
        'eco-chemical', 'toxin'
    ],

    'Material: Recyclability': [
        'closed loop', 'closed-loop', 'cradle to cradle', 'cradle to grave', 'cradle-to-cradle', 'cradle-to-grave',
        'reclaimed', 'recover', 'recovered', 'recovery', 'recycle', 'recycled', 'recycling', 'refurbished',
        'refurbishing', 'reman', 'remanufacture', 'remanufactured', 'renewable', 'repair', 'repurpose', 'restorative',
        'reuse', 'reused', 'reusing', 'single use', 'single-use', 'upcycle', 'upcycled', 'upcycling'
    ],

    'Material: Waste': [
        'conservation', 'conserving', 'disposal', 'waste', 'zero waste', 'landfill-free'
    ],

    'Packaging': [
        'minimalist packaging', 'biodegradable packaging', 'plastic-free packaging', 'green packaging',
        'low-impact packaging', 'waste-free packaging', 'packaging innovation', 'circular packaging',
        'lightweight packaging', 'reduced packaging', 'smart packaging', 'packaging optimization', 'packaging'
    ],

    'Environment: Bio-Environment': [
        'bio-diversity', 'biodiversity', 'eco-system', 'eco system', 'habitat preservation', 'wildlife conservation',
        'eco-balance'
    ],

    'Environment: Climate': [
        'carbon', 'carbon neutral', 'climate', 'climate action', 'climate crisis', 'emission', 'footprint',
        'global warming', 'greenhouse', 'landfill', 'net-zero', 'ozone layer', 'zero carbon', 'acidification',
        'weather patterns'
    ],

    'Energy: Consumption': [
        'consume', 'consumer', 'efficiency', 'efficient', 'energy', 'energy consumption', 'energy saving',
        'energy savings', 'phantom load', 'power consumption', 'power saving', 'power savings'
    ],

    'Energy: Renewability': [
        'bio-diesel', 'bio-energy', 'bio-fuel', 'biodiesel', 'bioenergy', 'biofuel', 'solar', 'geothermal',
        'hydropower', 'renewable energy', 'wind power', 'wind energy', 'renewable resource'
    ],

    'Manufacturing Process: Production': [
        'cleaner production', 'deforestation', 'dematerialisation', 'dematerialization', 'eco-design', 'ecodesign',
        'closed-loop production', 'green manufacturing', 'lean manufacturing', 'low-carbon production',
        'smart manufacturing', 'sustainable production', 'zero-emission production', 'zero-emission manufacturing'
    ],

    'Manufacturing Process: Worker': [
        'employee health', 'fair labor', 'fair wages', 'health and safety', 'human rights', 'labor standards',
        'occupational safety', 'work conditions', 'working conditions', 'social responsibility', 'worker empowerment',
        'worker rights', 'workforce diversity', 'workforce equality', 'workforce safety', 'fair treatment',
        'labor practices', 'employee welfare', 'non-discrimination'
    ],

    'Manufacturing Process: Supply Chain': [
        'fair trade', 'local sourcing', 'responsible sourcing', 'supply chain transparency', 'sustainable sourcing',
        'ethical sourcing', 'Traceability', 'supply chain', 'conflict-free sourcing', 'sourcing', 'green logistics',
        'low-impact transportation', 'responsible procurement', 'supply chain resilience', 'supply chain efficiency',
        'sustainable logistics', 'sustainable supply chain', 'vendor compliance', 'vendor sustainability'
    ],

    'User Experience: Price': [
        'cheap', 'cheaper', 'affordable', 'cost-effective', 'economical', 'low-cost', 'value for money'
    ],

    'User Experience: Quality': [
        'brake', 'broke', 'broken', 'crash', 'crashed', 'die', 'died', 'durability', 'durable', 'dying', 'garbage',
        'last long', 'life cycle', 'lifecycle', 'lifespan', 'lifetime', 'maintainable', 'maintenance', 'stop work',
        'stopped working', 'take back', 'take-back', 'tear', 'useless', 'wear', 'defective', 'high-quality',
        'long-lasting', 'premium', 'reliable', 'sturdy', 'well-made', 'well made', 'quality'
    ],

    'User Experience: Safety': [
        'accident prevention', 'child-safe', 'child safe', 'compliance', 'consumer protection', 'durable safety',
        'electrical safety', 'fail-safe', 'fire-resistant', 'fire-safe', 'hazard-free', 'impact-resistant',
        'non-toxic', 'safe', 'safe design', 'safety certification', 'safety', 'injury prevention'
    ]

}

#Function to identify matching keywords
def identify_matching_keywords(review, aspects):
    matching_keywords = {aspect: [] for aspect in aspects}
    for aspect, keywords in aspects.items():
        for keyword in keywords:
            if keyword in review:
                matching_keywords[aspect].append(keyword)
    return matching_keywords

# Function to map topics to aspects
def map_topics_to_aspects(review, aspects):
    aspect_mentions = {aspect: 0 for aspect in aspects}
    matching_keywords = identify_matching_keywords(review, aspects)
    for aspect, keywords in matching_keywords.items():
        if keywords:
            aspect_mentions[aspect] += 1
    return aspect_mentions, matching_keywords

# Apply aspect mapping with progress bar
tqdm.pandas(desc="Performing Aspect Mapping")
df[['aspect_mentions', 'matching_keywords']] = df['content'].progress_apply(
    lambda x: pd.Series(map_topics_to_aspects(x, aspects))
)

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

# Function to count sentiments for each aspect and calculate percentages
def count_aspect_sentiments(df, aspects):
    sentiment_counts = {aspect: {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0} for aspect in aspects}
    total_entries = len(df)

    for sentiments in df['aspect_sentiments']:
        for aspect, sentiment in sentiments.items():
            sentiment_counts[aspect][sentiment] += 1

    # Calculate percentages based on the total number of entries
    sentiment_percentages = {}
    for aspect, counts in sentiment_counts.items():
        sentiment_percentages[aspect] = {sentiment: (count / total_entries) * 100 for sentiment, count in
                                         counts.items()}
    return sentiment_counts, sentiment_percentages


# Count aspect sentiments and calculate percentages
aspect_sentiment_counts, aspect_sentiment_percentages = count_aspect_sentiments(df, aspects)

# Ensure the directory exists
output_dir = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA V2\results_images'
os.makedirs(output_dir, exist_ok=True)

# Visualize aspect sentiment distribution with percentages
for aspect, counts in aspect_sentiment_counts.items():
    percentages = aspect_sentiment_percentages[aspect]
    sns.barplot(x=list(counts.keys()), y=list(counts.values()))
    plt.title(f'Sentiment Distribution for {aspect}')

    for i, count in enumerate(counts.values()):
        plt.text(i, count, f'{percentages[list(counts.keys())[i]]:.1f}%', ha='center')

    # Create a valid filename by replacing any invalid characters if necessary
    safe_aspect = aspect.replace(" ", "_").replace(":", "_")
    # MODIFY HERE ACROSS CERTIFICATIONS
    file_path = os.path.join(output_dir, f'RCS100_{safe_aspect}.png')
    plt.savefig(file_path)
    plt.close()

# Save results to an Excel file ((MODIFY HERE ACROSS CERTIFICATIONS)
results_path = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA V2\results_excels\RCS100_with_ABSA.xlsx'
df.to_excel(results_path, index=False)

#Filter the dataframe by aspect sentiment
def filter_df_by_aspect_sentiment(df, aspect, sentiment):
    filtered_entries = []
    for idx, row in df.iterrows():
        if aspect in row['aspect_sentiments'] and row['aspect_sentiments'][aspect] == sentiment:
            entry = row.to_dict()
            entry['matched_keyword'] = ', '.join(row['matching_keywords'][aspect])
            filtered_entries.append(entry)
    return pd.DataFrame(filtered_entries)

# Define output directory for the aspect-specific Excel files
output_dir_excels = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA V2\results_excels'
os.makedirs(output_dir_excels, exist_ok=True)

# Define output directory for the LDA topics
output_dir_topics = r'D:\OneDrive\UC Berkeley\Engineering Design Scholar Program\Programs\ABSA V2\results_topics'
os.makedirs(output_dir_topics, exist_ok=True)

# Function to apply LDA and save topics to a file
def extract_and_save_topics(df, aspect, sentiment):
    safe_aspect = aspect.replace(" ", "_").replace(":", "_")
    #print(f"Processing {safe_aspect} ({sentiment})")
    if not df.empty:
        num_docs = df.shape[0]
        min_df = max(2, int(num_docs * 0.01))  # at least 1% of the documents, but no less than 2
        max_df = 0.95  # max_df should be at most 95%

        # Ensure min_df < max_df
        if min_df >= num_docs * max_df:
            min_df = max(1, int(num_docs * max_df) - 1)  # Adjust min_df to be less than max_df if necessary

        vectorizer = CountVectorizer(max_df=max_df, min_df=min_df, stop_words='english')
        try:
            X = vectorizer.fit_transform(df['content'])

            lda = LatentDirichletAllocation(n_components=10, random_state=42)
            lda.fit(X)

            def display_topics(model, feature_names, no_top_words):
                topics = []
                for topic_idx, topic in enumerate(model.components_):
                    topics.append(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
                return topics

            topics = display_topics(lda, vectorizer.get_feature_names_out(), 10)

            # Create a valid filename by replacing any invalid characters if necessary
            # (MODIFY HERE ACROSS CERTIFICATIONS)
            topics_file_path = os.path.join(output_dir_topics, f'RCS100_{safe_aspect}_{sentiment}_Topics.txt')

            with open(topics_file_path, 'w', encoding='utf-8') as f:
                for idx, topic in enumerate(topics):
                    f.write(f"Topic {idx + 1}: {topic}\n")
            #print(f"Topics for {safe_aspect} ({sentiment}) saved to {topics_file_path}")
        except ValueError as e:
            print(f"Error processing {safe_aspect} ({sentiment}): {e}")
    else:
        print(f"No data for {safe_aspect} ({sentiment})")

# Save aspect-specific Excel files for each aspect and sentiment
for aspect in aspects.keys():
    positive_df = filter_df_by_aspect_sentiment(df, aspect, 'POSITIVE')
    negative_df = filter_df_by_aspect_sentiment(df, aspect, 'NEGATIVE')

    # Create a valid filename by replacing any invalid characters if necessary
    safe_aspect = aspect.replace(" ", "_").replace(":", "_")

    #(MODIFY HERE ACROSS CERTIFICATIONS)
    positive_file_path = os.path.join(output_dir_excels, f'RCS100_{safe_aspect}_POSITIVE.xlsx')
    negative_file_path = os.path.join(output_dir_excels, f'RCS100_{safe_aspect}_NEGATIVE.xlsx')

    positive_df.to_excel(positive_file_path, index=False)
    negative_df.to_excel(negative_file_path, index=False)

    # Extract and save topics
    extract_and_save_topics(positive_df, aspect, 'POSITIVE')
    extract_and_save_topics(negative_df, aspect, 'NEGATIVE')
