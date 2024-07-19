"""Add some admin models."""
from django.contrib import admin

from selfcare.models import Person, PersonsHelpTip, PresetHelpTip


class CustomModelAdmin(admin.ModelAdmin):
    """Custom base for all classes."""

    def __init__(self, model, admin_site):
        """For the list display."""
        self.list_display = [
            field.name for field in model._meta.fields if field.name != 'id'
            ]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(Person)
class PersonAdmin(CustomModelAdmin):
    """Admin Person."""


@admin.register(PresetHelpTip)
class PresetsHelpTipsAdmin(CustomModelAdmin):
    """Admin PresetsHelpTips."""


@admin.register(PersonsHelpTip)
class PersonsHelpTipsAdmin(CustomModelAdmin):
    """Admin PersonsHelpTips."""
