import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Texts to be analyzed
texts = [
    """
    yum  i try to only buy fair trade chocolate because of the child slave labor involved in producing most chocolate  
    i also like organic  but i love andes mints and york peppermint patties  voila  i found my niche  they really are 
    delicious   does her chocolate happy dance 
    """,
    """
    dr  bronner s magic castile soap is vegan  fair trade  biodegradable  and organic  i m crazy for the incredible 
    scents  peppermint and almond are my favorites  but i m loving this tea tree scent  this soap doesn t contain harsh 
    and drying foaming agents  it s concentrated and must be diluted  this stuff will burn your pee hole and eyeballs  
    seriously   dilute  dilute  ok  you ll absolutely get your money s worth because a little goes a long way  saying it 
    s a multipurpose soap is an understatement  from armpits to dishes  i ve been using this brand for over twenty years  
    here s a list  i love lists and will find any excuse to make one  of my favorite uses body washa couple decent squirts 
    in the bath  the bottle is nice reading material shavingtoothpaste  peppermint of course   only in a serious pinch  it s 
    gross  but it works general purpose household cleanerlaundry soap  again  in a pinch soft scrubdish soapfoaming hand 
    soap  the best  houseplant pesticide  peppermint   this totally works  i even wash my car with it perfect for travel   
    it s concentratedperfect for camping   it s biodegradableif you ve never tried castile soap you really should give it a 
    go  you ll only miss your traditional thick lather at first  but soon realize it s a grandeur you can live without  
    castile soap does lather  just not like mainstream soaps containing additives and surfactants  dr  bronner s truly sells 
    itself  it s a natural  wonderful  high quality castile soap  it s a staple in many homes and it won t disappoint 
    """
]

# Clean text data
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

cleaned_texts = [clean_text(text) for text in texts]

# Vectorize the text
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_texts)

# Apply LDA
lda = LatentDirichletAllocation(n_components=1, random_state=42)
lda.fit(X)

# Extract topics
def display_topics(model, feature_names, no_top_words):
    topic = model.components_[0]
    return " ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])

topics = [display_topics(lda, vectorizer.get_feature_names_out(), 10)]
print("Extracted Topics for each text:")
for i, topic in enumerate(topics):
    print(f"Text {i + 1} Topic:", topic)
