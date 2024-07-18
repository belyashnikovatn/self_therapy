"""Models, main part for data structure."""
from django.db import models


class Person(models.Model):
    """Persons profile: just minimum."""

    name = models.CharField(
        max_length=256,
        verbose_name='ФИО пользователя',
    )
    tlg_id = models.PositiveIntegerField(
        verbose_name='ID диалога пользователя',
        unique=True,
    )

    class Meta:
        """Meta class for description."""

        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """For description."""
        return self.name


class PresetsHelpTips(models.Model):
    """Initial tips for self-help."""

    text = models.TextField(
        verbose_name='Текстовое описание подсказки',
    )

    class Meta:
        """Meta class for description."""

        verbose_name = 'базовая подсказка'
        verbose_name_plural = 'Базовые подсказки'

    def __str__(self):
        """For description."""
        return self.text


class PersonsHelpTips(models.Model):
    """Help tips for particular person."""

    text = models.TextField(
        verbose_name='Текстовое описание подсказки',
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='personstips',
        verbose_name='Пользователь',
    )
    is_on = models.BooleanField(
        default=True,
        verbose_name='Показывать',
    )
    likeliness = models.PositiveSmallIntegerField(
        default=100,
        verbose_name='Рейтинг',
    )
    preset_tip = models.ForeignKey(
        PresetsHelpTips, on_delete=models.SET_NULL,
        verbose_name='Базовая подсказка',
        null=True, blank=True,
        related_name='personstips',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Meta class for description."""

        verbose_name = 'подсказка'
        verbose_name_plural = 'Подсказки'

    def __str__(self):
        """For description."""
        return f'{self.text} helps {self.person}'
