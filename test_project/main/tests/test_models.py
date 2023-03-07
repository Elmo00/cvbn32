from django.test import TestCase

from main.models import JsonInputDate


class ModelsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.date = JsonInputDate.objects.create(
            name='aaaaaaaaaaaaaaaaaaaaa',
            date='2000-01-01 00:00:00'
        )
        cls.name_field = cls.date._meta.get_field('name')

    def test_max_length(self):
        real_max_length = getattr(self.name_field, 'max_length')
        self.assertEqual(real_max_length, 49)
