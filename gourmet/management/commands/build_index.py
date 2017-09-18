import sys
import json
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    help = "Build index for the downsized reviews."

    def build_index(self, input_filename, output_filename, delimiter_chars=",.;:!?"):
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
                    words2 = [word.strip(delimiter_chars).lower() for word in words]

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

    def add_arguments(self, parser):

        parser.add_argument(
            '--input_file',
            type=str,
            required=True,
            default=settings.ASSETS_DIR+"food_reviews.json",
            help='Path to downsized food reviews file.',
        )

        parser.add_argument(
            '--output_file',
            type=str,
            required=False,
            default=settings.ASSETS_DIR + "index.json",
            help='Output path for downsized file.',
        )

    def handle(self, *args, **options):

        input_file = options.get('input_file')
        output_file = options.get('output_file')

        self.stdout.write(">> Please sit back and relax while the indexing is done.")
        self.build_index(input_file, output_file)
        self.stdout.write(">> Indexing successfully completed!")

