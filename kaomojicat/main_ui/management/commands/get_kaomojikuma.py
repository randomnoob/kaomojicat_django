from django.core.management.base import BaseCommand, CommandError
from main_ui.models import Kaomoji, KaomojiCategory
import requests
from bs4 import BeautifulSoup
import json

def find_block(tag):
    if tag.get("class") and "wp-block-heading" in tag.get("class"):
        finder = tag.next_sibling.next_sibling.next_sibling.next_sibling
        if finder.name=="ul" and finder.get("class")==["cc"]:
            return True
    return False


class Command(BaseCommand):
    help = "Crawl kaomojies from kaomojikuma.com"


    url_list = [
        ("https://kaomojikuma.com/kaomoji-greetings-japanese-emoticons/","Greetings"),
        # ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/","Animals"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/kaomoji-bears/","Bears"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/kaomoji-cats/","Cats"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/kaomoji-dogs/","Dogs"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/kaomoji-bunny-rabbits/","Bunnies/Rabbit"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/more-animals/","Exotic Animals"),
        ("https://kaomojikuma.com/kaomoji-characters-japanese-emoticons/","Characters"),
        ("https://kaomojikuma.com/positive-emotions-japanese-emoticons/","Positive"),
        ("https://kaomojikuma.com/negative-emotions-japanese-emoticons/","Negative"),
        ("https://kaomojikuma.com/sad-kaomoji-japanese-emoticons/","Sad"),
        ("https://kaomojikuma.com/stressed-kaomoji-emotions-japanese-emoticons/","Stressed"),
        ("https://kaomojikuma.com/affectionate-actions-japanese-emoticons/","Affectionate Actions"),
        ("https://kaomojikuma.com/kaomoji-activities/","Activities"),
        ("https://kaomojikuma.com/neutral-actions-japanese-emoticons/", "Neutral Actions"),
        ("https://kaomojikuma.com/aggressive-actions-japanese-emoticons/", "Aggressive Actions"),
        ("https://kaomojikuma.com/bodily-functions-japanese-emoticons/", "Bodily Functions"),
        ("https://kaomojikuma.com/kaomoji-statements-japanese-emoticons/", "Kaomoji Statements"),
        ("https://kaomojikuma.com/friends-enemies/", "Friends & Enemies"),
        ("https://kaomojikuma.com/event-kaomojis-japanese-emoticons/", "Events"),
        ("https://kaomojikuma.com/cute-kawaii-face-japanese-emoticons/", "Cute Kawaii Face"),
        ("https://kaomojikuma.com/flower-girl-kaomoji/", "Flower Girl Kaomoji (✿◕‿◕)"),
        ("https://kaomojikuma.com/owo-whats-this-japanese-emoticons/", "OwO What’s this?"),
        ("https://kaomojikuma.com/uwu-meme-face-emoticons/", "UwU Meme Face Emoticons"),
    ]

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--import",
            action="store_true",
            help="IMport",
        )

    def handle(self, *args, **options):
        if options["import"]:
            self.do_import()
        else:
            all_targets = []
            for url, title in self.url_list:

                page = requests.get(url)
                soup = BeautifulSoup(page.text, "lxml")
                targets = []
                headers = soup.find_all(find_block)
                descriptions = [x.next_sibling.next_sibling for x in headers]
                kaomoji_list = [x.next_sibling.next_sibling for x in descriptions]
                merged = tuple(zip(headers, descriptions, kaomoji_list))
                for head, desc, kmjlist in merged:
                    section = {
                    'title': head.get_text().strip(),
                    'desc': desc.get_text().strip(),
                    'kaomoji': [x.get_text().strip() for x in kmjlist.find_all('li')],
                    }
                    targets.append(section)

                pagedata = {
                    "page": url,
                    "title": title,
                    "content": targets,
                }
                all_targets.append(pagedata)
                print(f"PAGEDATA: {pagedata}")

            with open("./kkuma.json","w") as fout:
                json.dump(all_targets, fout, indent=2)

                self.stdout.write(
                    self.style.SUCCESS('Successfully closed poll'))
                

    def do_import(self):
        with open("./kkuma.json") as fin:
            data = json.load(fin)
        parent_cate_names = list(set([x['title'] for x in data]))
        for name in parent_cate_names:
            k, k_is_done = KaomojiCategory.objects.get_or_create(name=name)
            print(f"Created {k}")
        for page in data:
            parentcat = KaomojiCategory.objects.filter(name=page['title']).first()
            for sub in page['content']:
                name = sub['title']
                subcat = KaomojiCategory.objects.create(
                        name=name, description=sub['desc'], parent=parentcat)
                self.stdout.write(
                    self.style.WARNING(f'Successfully created {subcat} in {parentcat}'))
                for k in sub['kaomoji']:
                    kd = Kaomoji.objects.create(kaomoji=k, category=subcat)
                    self.stdout.write(
                        self.style.NOTICE(f'Successfully created {k} in {subcat}'))

        
        
