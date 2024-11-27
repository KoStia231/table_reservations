from main.models import SiteText


def site_title(request):
    """
    Контекстный процессор для добавления названия сайта на каждую страницу.
    """
    site_title = SiteText.objects.filter(key=SiteText.KeyChoices.SITE_TITLE).first()
    return {'site_title': site_title}
