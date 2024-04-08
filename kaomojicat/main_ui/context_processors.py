from django.conf import settings
from main_ui.models import Kaomoji, KaomojiCategory


def kaomoji_category(request):
    return {"kaomoji_category": KaomojiCategory.objects.filter(parent__isnull=True)}
