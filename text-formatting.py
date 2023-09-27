import re

# Sample text containing sentences
text = """I have a dream. That one day. This nation will rise up. And live out the true meaning of its creed. CLOSING on SessionEventArgs(session_id=9321376ecd264ed8becb4eca0729699c)"""

# Define the word to match at the start of a sentence
word_to_match = "CLOSING"

# Split the text into sentences based on periods (.)
sentences = text.split(".")

# Use regex to remove sentences that start with the word_to_match
filtered_sentences = [sentence.strip() for sentence in sentences if not re.match(fr"^\s*{re.escape(word_to_match)}", sentence, re.IGNORECASE)]

# Join the remaining sentences back into a text with newlines
filtered_text = "\n".join(filtered_sentences)

print(filtered_text)
