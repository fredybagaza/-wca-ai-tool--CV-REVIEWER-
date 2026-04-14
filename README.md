import re
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_scanned_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        text = ""

        for i, image in enumerate(images):
            print(f"📄 Processing page {i+1}...")
            text += pytesseract.image_to_string(image)

        return text.lower()

    except Exception as e:
        print("❌ Error:", e)
        return None
def review_cv(cv_text):
    print("\n📄 CV REVIEW REPORT")
    print("=" * 40)
    # Length
    words = len(cv_text.split())
    print(f"\n📝 Word count: {words}")
    # Sections
    for sec in ["education", "experience", "skills"]:
        print(f"{'✅' if sec in cv_text else '❌'} {sec.capitalize()}")
    # Email
    print("✅ Email found" if re.search(r'\S+@\S+\.\S+', cv_text) else "❌ No email")

    # Phone
    print("✅ Phone found" if re.search(r'\+?\d[\d\s\-]{7,}', cv_text) else "❌ No phone")

    # Action verbs
    verbs = ["developed", "managed", "led", "created"]
    found = [v for v in verbs if v in cv_text]
    print(f"✅ Verbs: {', '.join(found)}" if found else "⚠️ No strong verbs")

def main():
    path = input("Enter scanned PDF path: ")
    text = extract_text_from_scanned_pdf(path)

    if text:
        review_cv(text)

if __name__ == "__main__":
    main()
