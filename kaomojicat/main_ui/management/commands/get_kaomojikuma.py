from django.core.management.base import BaseCommand, CommandError
from main_ui.models import Kaomoji, KaomojiCategory
import requests
from bs4 import BeautifulSoup


def find_block(tag):
    if tag.get("class") and "wp-block-heading" in tag.get("class"):
        finder = tag.next_sibling.next_sibling.next_sibling.next_sibling
        if finder.get("name") and finder.get("name")=="cc":
            return True
    return False


class Command(BaseCommand):
    help = "Crawl kaomojies from kaomojikuma.com"

    test_url = "https://kaomojikuma.com/kaomoji-greetings-japanese-emoticons/"
    url_list = [test_url,]

    urk_list = [
        ("https://kaomojikuma.com/kaomoji-greetings-japanese-emoticons/","Greetings"),
        ("https://kaomojikuma.com/kaomoji-animals-japanese-emoticons/","Animals"),
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


    def handle(self, *args, **options):
        
        for url in self.url_list:

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



            self.stdout.write(
                self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)