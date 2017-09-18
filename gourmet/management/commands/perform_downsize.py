import json
from django.core.management import BaseCommand
from django.conf import settings

ASSETS_DIR = getattr(settings, "ASSETS_DIR")


class Command(BaseCommand):

    help = "Downsize the gourmet data."

    def read_chunks(self, f, newline):
        buf = ""
        while True:
            while newline in buf:
                pos = buf.index(newline)
                yield buf[:pos]
                buf = buf[pos + len(newline):]
            chunk = f.read(4096)
            if not chunk:
                yield buf
                break
            buf += chunk

    def perform_down_size(self, file_input, file_output, count=100000):
        with open(file_input) as f:
            reviews = []
            review_dict = {}
            last_key = None
            for line in self.read_chunks(f, "\n"):
                if len(reviews) == count:
                    break
                if line == "":
                    reviews.append(review_dict)
                    review_dict = {}
                else:
                    try:
                        key, val = line.split(":", 1)
                        flag = 1
                    except:
                        review_dict[last_key] += line.replace("\n", "")
                        flag = 0
                    if flag == 1:
                        key = key.strip().replace("\n", "")
                        val = val.strip().replace("\n", "")
                        review_dict[key] = unicode(val, errors='ignore')
                        last_key = key

        with open(file_output, 'w') as outfile:
            json.dump(reviews, outfile)

    def add_arguments(self, parser):

        parser.add_argument(
            '--input_file',
            type=str,
            required=True,
            default=ASSETS_DIR + "foods.txt",
            help='File path for gourmet food reviews.',
        )

        parser.add_argument(
            '--output_file',
            type=str,
            required=False,
            default=ASSETS_DIR + "food_reviews.json",
            help='Output path for downsized file.',
        )

        parser.add_argument(
            '--count',
            type=int,
            required=False,
            default=100000,
            help='Total reviews expected after downsizing.',
        )

    def handle(self, *args, **options):

        input_file = options.get('input_file')
        output_file = options.get('output_file')
        count = options.get('count')

        self.stdout.write(">> Please sit back and relax while downsizing to %d is being done!" % (count, ))
        self.perform_down_size(input_file, output_file, count)
        self.stdout.write(">> Downsizing successfully completed!")

