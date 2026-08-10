
import re


def clean_text(raw_text):
    """
    Takes raw OCR text and returns a cleaned version.
    Steps: lowercase, remove junk characters, fix spacing.
    """

    text = raw_text

    text = text.lower()

    junk_chars = ['|', '~', '_', '`', '^', '*', '#', '@', '<', '>']
    for ch in junk_chars:
        text = text.replace(ch, '')

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'\s+([.,;:])', r'\1', text)

    text = text.strip()

    return text


if __name__ == "__main__":
    sample_raw_text = """NiTin ShArMMa is thE beSt """

    cleaned = clean_text(sample_raw_text)

    print("----- BEFORE CLEANING -----")
    print(sample_raw_text)
    print("\n----- AFTER CLEANING -----")
    print(cleaned)