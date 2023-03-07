from django.test import TestCase

from main.views import convert_to_list_of_dict

json_date = {
    '''[
        {
            "name": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': [{
            "name": "1",
            "date": "2000-01-01_00:00"
        }],
    '''[
        {
            "name": "1",
            "date": "2000-01-01_00:00"
        }, 
        {
            "name": "1234567890123456789012345678901234567890123456789",
            "date": "2000-01-01_00:00"
        }
    ]''': [{
            "name": "1",
            "date": "2000-01-01_00:00"
        },
        {
            "name": "1234567890123456789012345678901234567890123456789",
            "date": "2000-01-01_00:00"
        }],
    '''[
        {
            "name": "1",
            "name_": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': [{
            "name": "1",
            "date": "2000-01-01_00:00"
        }],
    '''[
        {
            "name": "1",
            "date_": "1",
            "date": "2000-01-01_00:00"
        }
    ]''': [{
            "name": "1",
            "date": "2000-01-01_00:00"
        }]
}


class ViewsTests(TestCase):

    def test_convert_to_list_of_dict(self):
        for entry, expected_date in json_date.items():
            real_answer = convert_to_list_of_dict(entry)
            self.assertEqual(real_answer, expected_date)
