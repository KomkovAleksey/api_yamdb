from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Year Validation"""

    if value > timezone.now().year:
        raise ValidationError(f'{value}Oops wrong year!')
