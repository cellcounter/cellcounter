from datetime import datetime

import factory
import factory.fuzzy
from pytz import utc

from .models import CountInstance


class CountInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CountInstance

    timestamp = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=utc))
    ip_address = "126.168.20.208"
    session_id = factory.fuzzy.FuzzyText(length=32)
    count_total = 200
