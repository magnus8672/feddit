from unittest import TestCase

import feddit


class Test(TestCase):

    def test_get_json_when_index_param_is_greater_than_zero(self):
        """
        GIVEN indexParam is greater than 0
        WHEN the function getJson is executed
        THEN it should return a reddit string with returned data from server
        """

        self.assertTrue(False)

    def test_get_json_when_index_param_is_zero(self):
        """
        GIVEN indexParam is 0
        WHEN the function getJson is executed
        THEN it should return a reddit string with returned data from server
        """

        self.assertTrue(False)

    def test_get_json_when_index_param_is_less_than_zero(self):
        """
        GIVEN indexParam is less than 0
        WHEN the function getJson is executed
        THEN it should return a reddit string with returned data from server
        """

        self.assertTrue(isinstance(feddit.getJson(-1), str))

    def test_get_children_when_d_is_a_valid_json_string(self):
        self.assertTrue(False)

    def test_get_children_when_d_is_an_empty_string(self):
        self.assertTrue(False)

    def test_get_children_when_d_is_a_none(self):
        self.assertTrue(False)

    def test_make_videos_when_scraped_ids_is_a_valid_array(self):
        self.assertTrue(False)

    def test_make_videos_when_scraped_ids_is_an_empty_array(self):
        self.assertTrue(False)

    def test_make_videos_when_scraped_ids_is_none(self):
        self.assertTrue(False)

    def test_clean_up_os_remove_is_executed(self):
        self.assertTrue(False)




