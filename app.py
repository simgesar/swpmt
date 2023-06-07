import random
import streamlit as st
from gtts import gTTS
from PIL import Image
import playsound
import os
import stanza

# Download the Turkish language model for stanza
stanza.download("tr")

# Load the Turkish language model
nlp = stanza.Pipeline("tr")

# Create a dictionary of words and their corresponding image file paths
words = {
    "et": ["/Users/simgesargin/Desktop/images/et.png",
           "/Users/simgesargin/Desktop/images/el.png",
           "/Users/simgesargin/Desktop/images/tavuk_eti.png",
           "/Users/simgesargin/Desktop/images/davul.png"],
    "elma": ["/Users/simgesargin/Desktop/images/elma.png",
             "/Users/simgesargin/Desktop/images/elmas.png",
             "/Users/simgesargin/Desktop/images/portakal.png",
             "/Users/simgesargin/Desktop/images/büyüteç.png"],
    "bal": ["/Users/simgesargin/Desktop/images/bal.png",
            "/Users/simgesargin/Desktop/images/sal.png",
            "/Users/simgesargin/Desktop/images/arı.png",
            "/Users/simgesargin/Desktop/images/şapka.png"],
    "saç": ["/Users/simgesargin/Desktop/images/saç.png",
            "/Users/simgesargin/Desktop/images/hac.png",
            "/Users/simgesargin/Desktop/images/tokka.png",
            "/Users/simgesargin/Desktop/images/soğan.png"]
}

# Function to extract nouns from user input using stanza
def extract_nouns(text):
    doc = nlp(text)
    nouns = [word.text for sent in doc.sentences for word in sent.words if word.upos == "NOUN"]
    return nouns

# Function to get picture options
def get_picture_options(word):
    # Get the list of image file paths for the word
    image_paths = words[word]

    # The first image file path is the correct picture
    correct_picture_path = image_paths[0]

    # Create a list of the other image file paths as distractors
    distractor_picture_paths = image_paths[1:]

    # Randomly select three of the distractor picture paths
    distractor_picture_paths = random.sample(distractor_picture_paths, 3)

    # Load the images from the file paths
    correct_picture = Image.open(correct_picture_path)
    distractor_pictures = [Image.open(path) for path in distractor_picture_paths]

    # Combine the correct picture and distractors into a list of picture options
    picture_options = [correct_picture] + distractor_pictures

    # Shuffle the list of picture options and remember the correct picture's index
    correct_picture_index = picture_options.index(correct_picture)
    random.shuffle(picture_options)
    correct_picture_index_shuffled = picture_options.index(correct_picture)

    return picture_options, correct_picture_index_shuffled

# Streamlit app
def main():
    # Set Streamlit app title
    st.title("Spoken Word-Picture Matching")

    # Initialize or increment page state
    if 'page_state' not in st.session_state:
        st.session_state['page_state'] = 0
    else:
        st.session_state['page_state'] += 1

    # Ensure page state doesn't exceed number of words
    page_state = st.session_state['page_state'] % len(words)

    # Get the current word
    word = list(words.keys())[page_state]

    with st.container():
        # Get the picture options and the correct picture index
        picture_options, correct_picture_index = get_picture_options(word)

        # Create column objects
        columns = st.columns(4)

        # Iterate over each picture option
        for i, picture_option in enumerate(picture_options):
            with columns[i]:
                # Display the image
                st.image(picture_option)

                # If the select button is clicked for this picture
                if st.button("👆", key=f"button_{word}_{i+1}"):
                    # Check if this picture is the correct picture
                    if i == correct_picture_index:
                        st.success("Correct! You selected the Target Picture.")
                        st.session_state['page_state'] += 1
                        st.experimental_rerun()
                    else:
                        st.error("Incorrect! Please try again.")

        st.markdown("---")  # Add a separator between words

    # Convert the word to speech and play it
    tts = gTTS(word, lang='tr')
    tts.save('word.mp3')
    playsound.playsound('word.mp3', True)
    os.remove('word.mp3')

    # Ask the user for input and validate noun-based choices
    user_response = st.text_input("Enter your response")

    if user_response:
        nouns = extract_nouns(user_response)

        if any(noun in words[word] for noun in nouns):
            st.success("Correct! You selected the picture associated with the noun.")
            st.image(picture_options[correct_picture_index])
        else:
            st.error("Incorrect! Please try again.")


if __name__ == "__main__":
    main()
