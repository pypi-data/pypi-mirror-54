from unittest import TestCase, mock
from aws.ec2 import set_default_region, get_default_region


class TestEc2(TestCase):
    
    def test_default_region(self):
        region = 'us-east-1'
        set_default_region(region)
        self.assertEqual(region, get_default_region())
