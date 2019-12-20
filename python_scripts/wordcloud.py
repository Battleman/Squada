from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np


def create_wordcloud(pandas_series, max_words=2000, max_font_size=None, filepath=None):
    mask = np.array(Image.open("images/NYC_silhouette.png"))
    mask[mask > 0] = 255
    # this is because the WordCloud library uses bigrams and if we do not shuffle data, we will
    # see noise like: Noise Residential, Residential Noise
    pandas_series = pandas_series.sample(frac=1)["Complaint Type"]

    wordcloud = WordCloud(
        width=3000,
        height=2000,
        max_words=max_words,
        max_font_size=max_font_size,
        background_color='black',
        stopwords=STOPWORDS,
        random_state=1,
        mask=mask,
        contour_width=3,
        contour_color='white'
    )

    text = pandas_series.astype(str).values
    processed_text = wordcloud.process_text(" ".join(text))
    wordcloud.generate_from_frequencies(processed_text)
    if filepath:
        wordcloud.to_file(filepath)
