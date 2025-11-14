"""
Urdu Language Support Module
Handles Urdu/Hindi commands and responses
"""


class UrduSupport:
    def __init__(self):
        """Initialize Urdu language support"""
        # Common Urdu/Hindi phrases and their English equivalents
        self.urdu_to_english = {
            # Greetings
            'سلام': 'hello',
            'السلام علیکم': 'hello',
            'assalam o alaikum': 'hello',
            'salam': 'hello',
            'kya hal hai': 'how are you',
            'کیا حال ہے': 'how are you',

            # Time related
            'waqt': 'time',
            'وقت': 'time',
            'waqt kya hua': 'what time is it',
            'وقت کیا ہوا': 'what time is it',
            'tareekh': 'date',
            'تاریخ': 'date',
            'aaj kya din hai': 'what day is today',
            'آج کیا دن ہے': 'what day is today',

            # Weather
            'mausam': 'weather',
            'موسم': 'weather',
            'mausam kaisa hai': 'how is the weather',
            'موسم کیسا ہے': 'how is the weather',

            # Music
            'gaana': 'song',
            'گانا': 'song',
            'gaana bajao': 'play song',
            'گانا بجاؤ': 'play song',
            'music chalao': 'play music',
            'music band karo': 'stop music',
            'موسیقی بند کرو': 'stop music',
            'roko': 'stop',
            'روکو': 'stop',

            # Alarms
            'alarm': 'alarm',
            'الارم': 'alarm',
            'alarm lagao': 'set alarm',
            'الارم لگاؤ': 'set alarm',
            'yaad dilao': 'remind me',
            'یاد دلاؤ': 'remind me',

            # Common words
            'kya': 'what',
            'کیا': 'what',
            'kaise': 'how',
            'کیسے': 'how',
            'kab': 'when',
            'کب': 'when',
            'kahan': 'where',
            'کہاں': 'where',
            'kyun': 'why',
            'کیوں': 'why',
            'haan': 'yes',
            'ہاں': 'yes',
            'nahi': 'no',
            'نہیں': 'no',
            'shukriya': 'thank you',
            'شکریہ': 'thank you',
            'meherbani': 'please',
            'مہربانی': 'please',
        }

        # English to Urdu responses
        self.english_to_urdu_responses = {
            'hello': 'السلام علیکم',
            'how are you': 'میں ٹھیک ہوں، شکریہ',
            'thank you': 'خوش آمدید',
            'goodbye': 'اللہ حافظ',
            'yes': 'ہاں',
            'no': 'نہیں',
            'playing': 'بجا رہا ہوں',
            'stopped': 'بند کر دیا',
            'alarm set': 'الارم لگا دیا',
        }

        print("✓ Urdu language support initialized")

    def detect_urdu(self, text):
        """
        Check if text contains Urdu/Hindi words

        Args:
            text: Input text

        Returns:
            bool: True if Urdu is detected
        """
        text_lower = text.lower()

        # Check for Urdu script (Arabic-based characters)
        has_urdu_script = any('\u0600' <= char <= '\u06FF' for char in text)

        # Check for Urdu/Hindi romanized words
        has_urdu_words = any(urdu_word in text_lower for urdu_word in self.urdu_to_english.keys())

        return has_urdu_script or has_urdu_words

    def translate_to_english(self, text):
        """
        Translate Urdu/Hindi text to English

        Args:
            text: Input text in Urdu/Hindi

        Returns:
            str: Translated English text
        """
        text_lower = text.lower()
        translated = text

        # Replace Urdu phrases with English equivalents
        for urdu_phrase, english_phrase in self.urdu_to_english.items():
            if urdu_phrase in text_lower:
                translated = translated.lower().replace(urdu_phrase, english_phrase)

        print(f"🔄 Urdu translation: '{text}' → '{translated}'")
        return translated

    def get_urdu_response(self, english_text):
        """
        Get Urdu response for common English phrases

        Args:
            english_text: English text

        Returns:
            str: Urdu response if available, None otherwise
        """
        text_lower = english_text.lower()

        for english_phrase, urdu_response in self.english_to_urdu_responses.items():
            if english_phrase in text_lower:
                return urdu_response

        return None

    def add_urdu_context_to_prompt(self, prompt):
        """
        Add Urdu language context to AI prompt

        Args:
            prompt: Original prompt

        Returns:
            str: Enhanced prompt with Urdu support
        """
        urdu_context = "\n\nNote: User may speak in Urdu/Hindi (Roman Urdu). Understand common Urdu phrases and respond appropriately. You can use simple Urdu words in your response if appropriate."

        return prompt + urdu_context
