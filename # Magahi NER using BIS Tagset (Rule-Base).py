# Magahi NER using BIS Tagset (Rule-Based)

# BIS Tagset (33 tags):
# 1.  N_NN     - Common Noun
# 2.  N_NNP    - Proper Noun
# 3.  N_NST    - Location Noun
# 4.  PR_PRP   - Personal Pronoun
# 5.  PR_PRF   - Reflexive Pronoun
# 6.  PR_PRC   - Reciprocal Pronoun
# 7.  PR_PRL   - Relative Pronoun
# 8.  PR_PRQ   - Interrogative Pronoun
# 9.  PR_PRI   - Indefinite Pronoun
# 10. DM_DMD   - Demonstrative Determiner
# 11. DM_DMR   - Relative Determiner
# 12. DM_DMQ   - Interrogative Determiner
# 13. DM_DMI   - Indefinite Determiner
# 14. V_VM     - Main Verb
# 15. V_VAUX   - Auxiliary Verb
# 16. JJ       - Adjective
# 17. RB       - Adverb
# 18. PSP      - Postposition
# 19. CC_CCD   - Coordinating Conjunction
# 20. CC_CCS   - Subordinating Conjunction
# 21. RP_RPD   - Default Particle
# 22. RP_CL    - Classifier
# 23. RP_INJ   - Interjection
# 24. RP_INTF  - Intensifier
# 25. RP_NEG   - Negation
# 26. QT_QTF   - General Quantifier
# 27. QT_QTC   - Cardinal Quantifier
# 28. QT_QTO   - Ordinal Quantifier
# 29. RD_SYM   - Symbol
# 30. RD_PUNC  - Punctuation
# 31. RD_ECH   - Echo Word
# 32. RD_UNK   - Unknown
# 33. NNP-PER  - Person (NER)
# Additional NER: NST-LOC - Location, NNP-ORG - Organization

import re
import pdfplumber

# ─────────────────────────────────────────────
# PDF READING
# ─────────────────────────────────────────────
pdf_path = r"c:\Users\rites\OneDrive\Desktop\2nd internal\Bihar Sharif mein Babu Samlal bada mokhtar hala baki i bada bahut neechta ke baad hola hal.pdf"

with pdfplumber.open(pdf_path) as pdf:
    text = ''
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:                      # BUG FIX: skip None pages
            text += page_text

# Convert text to lowercase
text = text.lower()

# ─────────────────────────────────────────────
# TOKENIZATION
# ─────────────────────────────────────────────
words = re.findall(r'\b\w+\b', text)

# ─────────────────────────────────────────────
# LEXICON LISTS
# ─────────────────────────────────────────────

# --- NER Lists ---
persons = [
    "singh", "ji", "samlal", "mokhtar", "saheb", "nawab",
    "babu", "haldhar", "ram", "kisun", "bulaki", "khan",
    "singh ji", "mokhtar saheb", "nawab saheb",
    "babu haldhar singh", "ram kisun singh", "bulaki khan"
]

locations = [
    "bihaar", "bihar", "sariiph", "sharif", "kiul",
    "bakhtiaarpur", "bakhtiyarpur", "manabhuum", "manbhum",
    "ranchi", "simla", "shimla", "vrindaban", "vrindavan",
    "patan", "saharanpur", "delhi", "mumbai", "kolkata",
    "patna", "varanasi", "lucknow", "agra", "jaipur",
    "udaipur", "bikaner", "jodhpur", "amritsar", "chennai",
    "hyderabad", "bangalore", "kochi", "guwahati", "bhopal",
    "indore", "nagpur", "nashik", "aurangabad", "ludhiana",
    "jalandhar", "dehradun", "mussoorie", "nainital",
    "rishikesh", "haridwar", "roorkee", "gaya"
]

organizations = [
    "sdo", "secretariat", "kachahari", "gazette",
    "police", "court", "hospital", "school", "office",
    "sarkar", "thana", "collectorate", "munsif"
]

# --- Nouns ---
# BUG FIX: Removed duplicate entries; separated Common from Proper nouns
Common = [
    "aadmi", "aurat", "ladka", "ladki", "baccha",
    "kaam", "ghar", "dost", "duniya", "sahar", "shehar",
    "raasta", "rasta", "kagaj", "saboot", "chithi",
    "khabar", "safai", "taala", "chhath", "daku",
    "salah", "khabindi", "gaon", "zameen", "paisa",
    "rupya", "naam", "baat", "din", "raat", "samay",
    "jagah", "log", "jaan", "desh", "naukri", "nokri",
    "adhikar", "nyay", "dawa", "ilaj", "khet", "naadi",
    "pul", "sadak", "jamin", "maakan", "makaan"
]

# BUG FIX: Proper nouns separate from NER persons to avoid double listing
Proper = [
    "ramji", "shyamji", "lalta", "deena", "shambhu",
    "ramdayal", "jagdish", "mahesh", "suresh", "naresh"
]

# Location nouns (spatial/directional)
Nloc = [
    "agari", "pichhari", "upar", "niche", "paas",
    "door", "andar", "bahar", "aage", "peeche",
    "daaye", "baaye", "saamne", "peeche", "beech"
]

# --- Pronouns ---
# BUG FIX: Pronouns and Demonstratives used same variable names (Relatives,
#           Wh_words, Indefinite) — the second assignment silently overwrote
#           the first. Now renamed clearly.

Personal = [
    "ham", "hum", "hamani", "hamani", "tohani", "tohar",
    "tu", "tum", "aap", "woh", "yeh", "voh",
    "is", "us", "unka", "unki", "unke", "inka",
    "inki", "inke", "mein", "main", "hamar", "tohar"
]

Reflexive = [
    "apne", "apna", "apni", "aap", "khud", "swayam"
]

Reciprocal = [
    "ek dusre", "aapas", "aapas mein"
]

# BUG FIX: Renamed to PR_Relatives / PR_Wh / PR_Indef for pronouns
PR_Relatives = ["je", "jekar", "jeker"]
PR_Wh        = ["kaun", "kekra", "ke"]
PR_Indef     = ["koi", "kuch", "sab", "har", "kisi", "sabhi", "kono"]

# --- Demonstratives ---
Deictics = [
    "iha", "uha", "ye", "vo", "yahaan", "wahan",
    "idhar", "udhar", "yahan", "wahan", "ihan", "uhan"
]

# BUG FIX: Renamed to DM_Relatives / DM_Wh / DM_Indef for demonstratives
DM_Relatives = ["jo", "jise", "jiska", "jis", "jinke", "jinki", "jeker"]
DM_Wh        = ["kaun", "kekra", "kaunsa", "kitna"]
DM_Indef     = ["i", "u", "koi", "kuch", "kono"]

# --- Verbs ---
# BUG FIX: Expanded verb lists with common Magahi verb forms
Main = [
    "kar", "kara", "kare", "karis", "karela", "karelak",
    "bolla", "bollaa", "bolal", "bola", "bol",
    "chal", "chali", "chalal", "chalela",
    "pahunch", "pahuncha", "pahunchala",
    "kailka", "kailun", "kailkau",
    "dekh", "dekhla", "dekhlaun", "dekhlaulak", "dekhel",
    "ja", "jaa", "gela", "gel", "gail", "gaila",
    "aa", "aail", "aala", "aawa",
    "le", "lela", "leil", "lia",
    "de", "dela", "deil", "dia",
    "kha", "khail", "khala", "khael",
    "pi", "pila", "piyal", "piel",
    "sun", "sunla", "sunal", "sunel",
    "uth", "uthla", "uthal",
    "baith", "baithla", "baithal",
    "so", "soila", "soal",
    "ro", "roila", "roal",
    "has", "hasla", "hasal",
    "maar", "maarla", "maaral",
    "maral", "mara",
    "likh", "likhla", "likhal",
    "padh", "padhla", "padhal",
    "khol", "kholla", "kholal",
    "band", "bandla", "bandal",
    "rakhe", "rakhel", "rakhla"
]

Auxiliary = [
    "hal", "hala", "halaa", "hau", "haue",
    "hai", "hain", "he", "hein",
    "hove", "hovela", "hoibe",
    "tha", "the", "thi",
    "rahela", "rahal", "rahel",
    "sakela", "sakel", "sake",
    "chahela", "chahel", "chahe",
    "gela", "gel", "gail",
    "aail", "aawela"
]

# --- Adjectives ---
Adjectives = [
    "acchaa", "acha", "achha", "bura", "buri",
    "bada", "bdaa", "bara", "chhota", "chhoti",
    "lamba", "lambi", "sundar", "sundari",
    "kharab", "kharabi", "naya", "nayi", "purana",
    "garam", "thanda", "saaf", "ganda", "motaa",
    "patla", "uncha", "neecha", "tez", "dhima",
    "khush", "dukhi", "bimar", "tandrust",
    "ameer", "garrib", "garib", "buddhaa", "jawaan",
    "neech", "neechta", "uchha"
]

# --- Adverbs ---
Adverbs = [
    "bahut", "bhut", "bahute", "jaldi", "dhire",
    "kabhi", "hamesha", "abhi", "phir", "tab",
    "yahan", "wahan", "kal", "aaj", "parso",
    "subah", "shaam", "raat", "din",
    "acchhe se", "seedha", "ulta",
    "fir", "dobara", "wapis", "vapas"
]

# --- Postpositions ---
Postpositions = [
    "ke", "se", "mem", "mein", "par", "pe",
    "ka", "ki", "ko", "tak", "bhar",
    "liye", "hetu", "dwara", "saath",
    "bina", "andar", "bahar", "upar",
    "niche", "aage", "peeche", "beech",
    "baad", "pahle", "baat", "waste"
]

# --- Conjunctions ---
Coordinator = [
    "aur", "ya", "lekin", "parantu", "magar",
    "kintu", "tatha", "athva", "balki", "phir bhi"
]

Subordinator = [
    "ki", "jab", "agar", "to", "toh", "jab tak",
    "kyunki", "isliye", "taaki", "jaise", "jaisa",
    "jo", "jis", "jise", "jiska", "jab se"
]

# --- Particles ---
Default = [
    "bhi", "hi", "toh", "mat", "bas",
    "kya", "na", "naa", "haan", "haa"
]

Classifiers = [
    "ek", "do", "teen", "char", "paanch",
    "chhah", "saat", "aath", "nau", "das",
    "gyarah", "barah", "tera", "chaudah", "pandrah",
    "solah", "satrah", "atharah", "unnis", "bees",
    "pachas", "sau", "hazaar"
]

Interjections = [
    "arrey", "are", "oh", "wah", "hmm",
    "haaye", "haye", "uff", "aah", "arre",
    "shabbash", "accha", "theek"
]

Intensifiers = [
    "bahut", "bhut", "ati", "ekdum", "bilkul",
    "poori tarah", "bilkul sahi", "thoda", "thodi"
]

Negations = [
    "nahi", "nahin", "na", "naa", "mat",
    "kabhi nahi", "bilkul nahi", "nako"
]

# --- Quantifiers ---
General = [
    "kuch", "sab", "sabhi", "har", "kisi",
    "kaafi", "thoda", "thodi", "zyada",
    "bahut saare", "bahut se", "kuch bhi", "poora"
]

Cardinal = [
    "ek", "do", "teen", "char", "paanch",
    "chhah", "saat", "aath", "nau", "das",
    "bees", "tees", "chalis", "pachas",
    "sau", "hazaar", "lakh"
]

Ordinal = [
    "pehla", "pehli", "dusra", "dusri",
    "teesra", "teesri", "chotha", "chouthi",
    "paanchwa", "chhatha", "saatwa",
    "aathwa", "nauwa", "daswa"
]

# --- Residuals ---
Symbols = [
    "@", "#", "$", "%", "^", "&", "*",
    "(", ")", "-", "_", "+", "=",
    "{", "}", "[", "]", "|", "\\",
    ":", ";", "<", ">", "/", "~"
]

Punctuation = [".", ",", "!", "?", ";", ":", "-", "(", ")", "\"", "'"]

# BUG FIX: Echo words are reduplication-type words in Magahi, not just vowels
Echowords = [
    "khaana waana", "paani waani", "ghar waar",
    "chai waai", "kaam waam", "baat waat",
    "roti shoti", "kapda wapda"
]

# ─────────────────────────────────────────────
# HELPER: multi-word phrase tagger
# (handles phrases like "babu haldhar singh")
# ─────────────────────────────────────────────
def tag_phrases(words, phrase_list, tag):
    """Mark phrase positions so single-word loop can skip them."""
    tagged = {}
    text_joined = " ".join(words)
    for phrase in sorted(phrase_list, key=len, reverse=True):   # longest match first
        phrase_lower = phrase.lower()
        phrase_words = phrase_lower.split()
        plen = len(phrase_words)
        for i in range(len(words) - plen + 1):
            if words[i:i+plen] == phrase_words and i not in tagged:
                for j in range(i, i + plen):
                    tagged[j] = (words[j], tag) if j > i else (phrase, tag)
    return tagged

# Pre-tag multi-word phrases
phrase_tags = {}
phrase_tags.update(tag_phrases(words, persons,       "NNP-PER"))
phrase_tags.update(tag_phrases(words, locations,     "NST-LOC"))
phrase_tags.update(tag_phrases(words, organizations, "NNP-ORG"))

# ─────────────────────────────────────────────
# MAIN TAGGING LOOP
# ─────────────────────────────────────────────
tagged_output = []

for idx, word in enumerate(words):

    # Skip words already tagged as part of a phrase (middle tokens)
    if idx in phrase_tags and phrase_tags[idx][0] != word:
        continue

    # Use pre-tagged phrase result if available
    if idx in phrase_tags:
        tagged_output.append(phrase_tags[idx])
        continue

    # ── Lexicon lookup (order matters: NER → POS) ──

    if word in persons:
        tagged_output.append((word, "NNP-PER"))

    elif word in locations:
        tagged_output.append((word, "NST-LOC"))

    elif word in organizations:
        tagged_output.append((word, "NNP-ORG"))

    elif word in Common:
        tagged_output.append((word, "N_NN"))

    elif word in Proper:
        tagged_output.append((word, "N_NNP"))

    elif word in Nloc:
        tagged_output.append((word, "N_NST"))

    elif word in Personal:
        tagged_output.append((word, "PR_PRP"))

    elif word in Reflexive:
        tagged_output.append((word, "PR_PRF"))

    elif word in Reciprocal:
        tagged_output.append((word, "PR_PRC"))

    # BUG FIX: Use renamed PR_Relatives (was overwritten by DM_Relatives)
    elif word in PR_Relatives:
        tagged_output.append((word, "PR_PRL"))

    # BUG FIX: Use renamed PR_Wh (was overwritten by DM_Wh)
    elif word in PR_Wh:
        tagged_output.append((word, "PR_PRQ"))

    # BUG FIX: Use renamed PR_Indef (was overwritten by DM_Indef)
    elif word in PR_Indef:
        tagged_output.append((word, "PR_PRI"))

    elif word in Deictics:
        tagged_output.append((word, "DM_DMD"))

    elif word in DM_Relatives:
        tagged_output.append((word, "DM_DMR"))

    elif word in DM_Wh:
        tagged_output.append((word, "DM_DMQ"))

    elif word in DM_Indef:
        tagged_output.append((word, "DM_DMI"))

    elif word in Negations:
        tagged_output.append((word, "RP_NEG"))

    elif word in Auxiliary:
        tagged_output.append((word, "V_VAUX"))

    elif word in Main:
        tagged_output.append((word, "V_VM"))

    elif word in Adjectives:
        tagged_output.append((word, "JJ"))

    # BUG FIX: Use renamed Intensifiers (was same name as Adverbs causing overlap)
    elif word in Intensifiers:
        tagged_output.append((word, "RP_INTF"))

    elif word in Adverbs:
        tagged_output.append((word, "RB"))

    elif word in Postpositions:
        tagged_output.append((word, "PSP"))

    elif word in Coordinator:
        tagged_output.append((word, "CC_CCD"))

    elif word in Subordinator:
        tagged_output.append((word, "CC_CCS"))

    elif word in Default:
        tagged_output.append((word, "RP_RPD"))

    elif word in Ordinal:
        tagged_output.append((word, "QT_QTO"))

    elif word in Cardinal:
        tagged_output.append((word, "QT_QTC"))

    elif word in Classifiers:
        tagged_output.append((word, "RP_CL"))

    elif word in General:
        tagged_output.append((word, "QT_QTF"))

    elif word in Interjections:
        tagged_output.append((word, "RP_INJ"))

    elif word in Symbols:
        tagged_output.append((word, "RD_SYM"))

    elif word in Punctuation:
        tagged_output.append((word, "RD_PUNC"))

    elif word in Echowords:
        tagged_output.append((word, "RD_ECH"))

    # ── Morphological Rules (expanded for Magahi) ──

    # Magahi past tense verb endings
    elif word.endswith(("ela", "elak", "elau", "elai", "elaa")):
        tagged_output.append((word, "V_VM"))

    # Magahi perfective verb endings
    elif word.endswith(("ala", "alak", "alau", "alai", "alaa")):
        tagged_output.append((word, "V_VM"))

    # General verb endings (la, aa, na, bo)
    elif word.endswith(("la", "bo", "be", "bai", "ega", "egi", "enge")):
        tagged_output.append((word, "V_VM"))

    # Auxiliary / copula endings
    elif word.endswith(("hal", "hau", "hei", "hain", "tha", "the", "thi")):
        tagged_output.append((word, "V_VAUX"))

    # Noun suffixes common in Magahi/Hindi
    elif word.endswith(("iya", "pan", "taa", "ta", "waa", "wala", "wali")):
        tagged_output.append((word, "N_NN"))

    # Noun/name suffixes (proper nouns)
    elif word.endswith(("singh", "lal", "ram", "devi", "bai", "prasad", "kumar", "dhar")):
        tagged_output.append((word, "N_NNP"))

    # Adjective suffix
    elif word.endswith(("baar", "maar", "ful", "ish", "waan", "mand")):
        tagged_output.append((word, "JJ"))

    # Adverb suffix
    elif word.endswith(("tak", "bhar")):
        tagged_output.append((word, "RB"))

    # BUG FIX: noun ending 'ii' / 'ai' retained
    elif word.endswith(("ii", "ai")):
        tagged_output.append((word, "N_NN"))

    # BUG FIX: generic 'aa' / 'ka' could be verb OR noun — default to N_NN
    # (previously defaulted to V_VM which was incorrect for most cases)
    elif word.endswith(("aa", "ka")):
        tagged_output.append((word, "N_NN"))

    # ── BUG FIX: Default fallback changed from RD_UNK to N_NN ──
    # Rationale: in Indo-Aryan languages the open word class is noun;
    # most OOV words in a Magahi corpus are common nouns.
    else:
        tagged_output.append((word, "N_NN"))


# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────
print("\nBIS NER + POS Tagging Output:\n")
print(f"{'Word':<25} {'Tag'}")
print("-" * 40)
for word, tag in tagged_output:
    print(f"{word:<25} {tag}")

# ── Tag Frequencies ──
# BUG FIX: Used collections.Counter instead of manual dict for cleaner code
from collections import Counter

tag_freq = Counter(tag for _, tag in tagged_output)

print("\n" + "=" * 40)
print("Tag Frequencies (sorted by count):\n")
print(f"{'Tag':<15} {'Count':>8}")
print("-" * 25)
for tag, count in tag_freq.most_common():
    print(f"{tag:<15} {count:>8}")

print("\n" + "=" * 40)
print(f"Total words tagged : {len(tagged_output)}")
print(f"Unique tags used   : {len(tag_freq)}")