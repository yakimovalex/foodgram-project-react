import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_name(value):
    # Проверяем, содержит ли значение только буквы
    if not re.match(r'^[A-Za-zА-Яа-я]+$', value):
        raise ValidationError(
            _('only letters are allowed'),
            code='invalid_name'
        )
