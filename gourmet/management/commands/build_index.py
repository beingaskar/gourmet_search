import sys
import json
import re
import string
from django.core.management import BaseCommand
from django.conf import settings

from gourmet.utils import load_json_data

ASSETS_DIR = getattr(settings, "ASSETS_DIR")


class Command(BaseCommand):

    help = "Build index for the downsized reviews."

    def strip_html(self, content):
        """
        Strip off any HTML tags (or portions of it) present in the content.
        """

        cleanr = re.compile('<.*?>')
        clean_text = re.sub(cleanr, '', content)

        incomplete_tags = ["(<br", "<br", "br>", "/>"]
        for tag in incomplete_tags:
            clean_text = clean_text.replace(tag, "")

        return clean_text

    def clean_words(self, word):
        """
        Convert given word string to various substrings (if possible) after removing punctuations.
        """

        for char in string.punctuation:
            word = word.strip(char)
            word = word.replace(char, " ")
        return [w for w in word.split(" ") if w]

    def build_index_terms(self, input_filename, output_filename):
        """
        Generate the index (terms-> review) for given input file.
        """

        try:
            word_occurrences = {}

            with open(input_filename) as f:
                data = json.load(f)
                word_id_map = {}
                for i, entry in enumerate(data):
                    review_summary = entry.get('review/summary')
                    review_text = entry.get('review/text')
                    words_summary = review_summary.split()
                    words_text = review_text.split()
                    words = words_summary
                    words.extend(words_text)
                    words = list(set(words))

                    words2 = []
                    for word in words:
                        word = word.lower()
                        word = self.strip_html(word)
                        words = self.clean_words(word)
                        words2.extend(words)

                    for word in words2:
                        if word:
                            if not word_occurrences.has_key(word):
                                word_occurrences[word] = []

                            if not word_id_map.has_key(word):
                                word_id_map[word] = set()
                            if i not in word_id_map[word]:
                                word_occurrences[word].append(i)
                                word_id_map[word].add(i)
        except IOError as ioe:
            print input_filename
            sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
            sys.exit(1)

        if word_occurrences:
            with open(output_filename, 'w') as outfile:
                json.dump(word_occurrences, outfile)

    def build_index_review(self, reviews_data, terms_index, output_filename):
        terms_index = load_json_data(terms_index)
        reviews_data = load_json_data(reviews_data)
        result = {}
        for term, indices in terms_index.items():
            for ind in indices:
                if not result.has_key(ind):
                    result[ind] = {"terms": {}, "review_score": reviews_data[ind].get("review/score", '0.0')}
                result[ind]["terms"][term] = 1

        if result:
            with open(output_filename, 'w') as outfile:
                json.dump(result, outfile)

    def add_arguments(self, parser):

        parser.add_argument(
            '--input_file',
            type=str,
            required=True,
            default=ASSETS_DIR+"/food_reviews.json",
            help='Path to downsized food reviews file.',
        )

        parser.add_argument(
            '--output_file_1',
            type=str,
            required=False,
            default=ASSETS_DIR + "/index_1.json",
            help='Output path for index (term -> documents) file.',
        )

        parser.add_argument(
            '--output_file_2',
            type=str,
            required=False,
            default=ASSETS_DIR + "/index_2.json",
            help='Output path for index (document -> terms) file.',
        )

    def handle(self, *args, **options):

        input_file = options.get('input_file')
        output_file_1 = options.get('output_file_1')
        output_file_2 = options.get('output_file_2')

        # self.stdout.write(">> Building Index (1 of 2).")
        # self.build_index_terms(input_file, output_file_1)
        self.stdout.write(">> Building Index (2 of 2).")
        self.build_index_review(input_file, output_file_1, output_file_2)
        self.stdout.write(">> Indexing successfully completed!")

