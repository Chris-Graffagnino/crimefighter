import unittest
import requests
import mock
import getcrime

# run via command line: python -m unittest discover

class BaseClassData(unittest.TestCase):

    fake_metro_html =\
        """
        <p>Each Daily Booking list will be removed no later than 14 days after its posting.</p>
        <ul>
          <li><a href="/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2028.pdf">December 28</a></li>
          <li><a href="/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2027.pdf">December 27</a></li>
        </ul>
        """

    text_data = """
        Arrest   Date   Charge Description                              Last Name    First Name  Street

        1/2/2015 23:17  ALCOHOL- UNDER 21, CONSUMPTION                  SMITH        JACKSON     HARDING PIKE

        1/3/2015 12:04  ASSAULT- FEAR OF BODILY INJURY                  PENIX        KENNETH     RURAL HILL RD"""


    fake_json = """
        [
            {
                "fields": {
                    "first_name": "jackson",
                    "surname": "smith",
                    "location": "harding pike",
                    "time": "23:17",
                    "date": "2015-01-02",
                    "offense": "alcohol- under 21, consumption"
                },
                "model": "crimeapp.crimes"
            },
            {
                "fields": {
                    "first_name": "kenneth",
                    "surname": "penix",
                    "location": "rural hill rd",
                    "time": "12:04",
                    "date": "2015-01-03",
                    "offense": "assault- fear of bodily injury"
                },
                "model": "crimeapp.crimes"
            },
        ]
        """

class CreatePdfLinkTest(BaseClassData):
    def test_get_pdf_link(self):
        with mock.patch('__main__.getcrime.get_metro_html', auto_spec=True) as req:
            
            correct_url = 'http://www.nashville.gov/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2028.pdf'
            req.return_value  = self.fake_metro_html

            self.assertEqual(getcrime.get_first_pdf_link(req.return_value), correct_url)


class TestParseTextFile(BaseClassData):
    def test_parse_test_file_good_data(self):
        
        fake_readlines = [x.strip() for x in self.text_data.split('\n') if len(x) > 0]

        with mock.patch('getcrime.read_text_file') as text:
            text.return_value = fake_readlines
            correct_parse_text_file = [
                ["2015-01-02", "23:17", "alcohol- under 21, consumption", "smith", "jackson", "harding pike"], 
                ["2015-01-03", "12:04", "assault- fear of bodily injury", "penix", "kenneth", "rural hill rd"]
            ]

            self.assertEqual(getcrime.parse_text_file(text.return_value), correct_parse_text_file)



if  __name__ == '__main__':
    unittest.main()


