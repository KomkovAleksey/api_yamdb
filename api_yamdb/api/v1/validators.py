"""
API validators
"""
import re

from django.db.models import Q
from rest_framework import serializers

from users.models import CustomUser


def validate_data(data):
    """
    Input data validation of username and email fields
    """
    username = data.get('username')
    email = data.get('email')

    if username and email:

        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Check username')
        if username.lower() == 'me':
            raise serializers.ValidationError('Username "me" not allowed')

        if (CustomUser.objects.filter(
                Q(email__iexact=email) & ~Q(username__iexact=username))):
            raise serializers.ValidationError('This email is taken')

        if (CustomUser.objects.filter(
                Q(username__iexact=username) & ~Q(email__iexact=email))):
            raise serializers.ValidationError('This username is taken')

    return data
