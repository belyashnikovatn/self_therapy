from telegram_django_bot import forms as td_forms
from telegram_django_bot.td_viewset import TelegramViewSet

from selfcare.models import PersonsHelpTips


class PersonsHelpTipsForm(td_forms.TelegramModelForm):
    class Meta:
        model = PersonsHelpTips
        fields = ['text',]


class PersonsHelpTipsViewSet(TelegramViewSet):
    model_form = PersonsHelpTipsForm
    queryset = PersonsHelpTips.objects.all()
    viewset_name = 'PersonsHelpTips'
