from django.test import TestCase

from main.forms import JsonInputDateForm

json_date = {
    '''[
        {
            "name": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': True,
    '''[
        {
            "name": "1",
            "date": "2000-01-01_00:00"
        }, 
        {
            "name": "1234567890123456789012345678901234567890123456789",
            "date": "2000-01-01_00:00"
        }
    ]''': True,
    '''[
        {
            "name": "1",
            "name_": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': True,
    '''[
        {
            "name": "1",
            "date_": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': True,
    '''[
        {
            "name": "",
            "date": "2000-01-01_00:00"
        }
    ]''': False,
    '''[
        {
            "name": "1",
            "date_": "1",
            "date": "2000-01-01 00:00"
        }
    ]''': False,
    '''[
        {
            "name": "123456789012345678901234567890123456789012345678901234567890",
            "date_": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': False,
    '''[
        {
            "name": "1234567890123456789012345678901234567890123456789",
            "date": "2000_01_01 00:00"
        }
    ]''': False,
    '''[
        {
            "date": "2000_01_01 00:00"
        }
    ]''': False,
    '''[
        {
            "name": "12345678901234567890"
        }
    ]''': False,
}


class FormsTests(TestCase):

    def test_valid_format(self):
        for entry, is_valid in json_date.items():
            func_value = JsonInputDateForm.valid_format(entry)
            self.assertEqual(func_value, is_valid)
