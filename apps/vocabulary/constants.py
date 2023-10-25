from django.db.models import TextChoices


class PartOfSpeech(TextChoices):
    NOUN = "noun", "Noun"  # Іменник
    PRONOUN = "pronoun", "Pronoun"  # Займенник
    VERB = "verb", "Verb"  # Дієслово
    ADJECTIVE = "adjective", "Adjective"  # Прикметник
    ADVERB = "adverb", "Adverb"  # Прислівник
    PREPOSITION = "preposition", "Preposition"  # Прийменник
    CONJUNCTION = "conjunction", "Conjunction"  # Сполучник
    INTERJECTION = "interjection", "Interjection"  # Вигук
    ARTICLE = "article", "Article"  # Артикль (the, a, an)
    DETERMINER = "determiner", "Determiner"  # Дефінітор (this, that, these, those)
    PARTICLE = (
        "particle",
        "Particle",
    )  # Частка (phrasal verbs like "give up", "run out of")
