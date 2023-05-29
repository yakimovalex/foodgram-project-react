import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def check_name(value):
    if not re.match(r'^[A-Za-zА-Яа-я]+([^._-])+([^.+\-])+([^.@\-])+$', value):
        raise ValidationError(
            _('only letters are allowed'),
            code='invalid_name'
        )


def check_hex(value):
    if not re.match(r'/^#[0-9A-F]{6}$/i', value):
        raise ValidationError(
            _('is not hex'),
            code='invalid_name'
        )
