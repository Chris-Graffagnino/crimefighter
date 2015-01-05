import unittest
import requests
import mock
import getcrime

# run via command line: python -m unittest discover

class CreatePdfLinkTest(unittest.TestCase):
    def test_get_pdf_link(self):
        with mock.patch(requests.get) as request:
            fake_metro_response = StringIO(
                """
                <p>Each Daily Booking list will be removed no later than 14 days after its posting.</p>
                <ul>
                  <li><a href="/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2028.pdf">December 28</a></li>
                  <li><a href="/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2027.pdf">December 27</a></li>
               </ul>
                """
            )
            correct_url = 'http://www.nashville.gov/Portals/0/SiteContent/Police/docs/Media/Daily%20Arrest/December%2028.pdf'
            request.return_value = fake_metro_response
            
            self.assertEqual(getcrime.get_pdf_link(), correct_url)












if  __name__ == '__main__':
    unittest.main()


