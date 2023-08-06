import requests
from cerberus import Validator


class SmsEdgeApi(object):
    # MAIN

    endpoint = 'https://api.smsedge.io/v1/'
    apiKey = ''

    def __init__(self, api_key):
        self.api_key = api_key

    # REFERENCES

    def get_functions(self):
        """
        This function returns all available API functions
        :return:
        """
        return self._validate_and_run('references/functions/')

    def get_http_statuses(self):
        """
        This function returns all HTTP response status codes
        :return:
        """
        return self._validate_and_run('references/statuses/')

    def get_countries(self):
        """
        This function returns list of countries
        :return:
        """
        return self._validate_and_run('references/countries/')

    # SMS

    def send_single_sms(self, fields):
        """
        Send a single SMS message
        :param fields:
        :return:
        """
        rules = {
            'from': {'required': True, 'type': 'string'},
            'to': {'required': True, 'type': 'integer', 'maxlength': 64},
            'text': {'required': True, 'type': 'string'},
            'name': {'type': 'string'},
            'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            'country_id': {'type': 'integer', 'maxlength': 32},
            'reference': {'type': 'string'},
            'shorten_url': {'type': 'boolean'},
            'list_id': {'type': 'integer', 'maxlength': 32},
            'transactional': {'type': 'integer', 'maxlength': 32},
            'preferred_route_id': {'type': 'integer', 'maxlength': 32},
            'delay': {'type': 'integer', 'maxlength': 32},
        }

        return self._validate_and_run('sms/send-single/', fields, rules)

    def send_list(self, fields):
        """
        Send SMS messages to all good numbers in a list
        :param fields:
        :return:
        """
        rules = {
            'list_id': {'required': True, 'type': 'integer', 'maxlength': 32},
            'from': {'required': True, 'type': 'string'},
            'text': {'required': True, 'type': 'string'},
            'shorten_url': {'type': 'boolean'},
            'preferred_route_id': {'type': 'integer', 'maxlength': 32}
        }

        return self._validate_and_run('sms/send-list/', fields, rules)

    def get_sms_info(self, fields):
        """
        Get information about sent SMS messages
        :param fields:
        :return:
        """
        rules = {
            'ids': {'required': True, 'type': 'string'}
        }

        return self._validate_and_run('sms/get/', fields, rules)

    # LISTS OF NUMBERS

    def create_list(self, fields):
        """
        Creating A new list
        :param fields:
        :return:
        """
        rules = {
            'name': {'required': True, 'type': 'string'}
        }

        return self._validate_and_run('lists/create/', fields, rules)

    def delete_list(self, fields):
        """
        Deleting an existing list
        :param fields:
        :return:
        """
        rules = {
            'id': {'required': True, 'type': 'integer'}
        }

        return self._validate_and_run('lists/delete/', fields, rules)

    def get_list_info(self, fields):
        """
        Get all info about a list, including sending stats and numbers segmentation
        :param fields:
        :return:
        """
        rules = {
            'id': {'required': True, 'type': 'integer'}
        }

        return self._validate_and_run('lists/info/', fields, rules)

    def get_all_lists(self):
        """
        Get all the lists that user created, with information about stored numbers
        :return:
        """
        return self._validate_and_run('lists/getall/')

    # PHONE NUMBERS

    def create_number(self, fields):
        """
        Create a new contact to a list
        :param fields:
        :return:
        """
        rules = {
            'number': {'required': True, 'type': 'string'},
            'list_id': {'required': True, 'type': 'integer', 'maxlength': 32},
            'country_id': {'type': 'integer', 'maxlength': 32},
            'name': {'type': 'string'},
            'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        }

        return self._validate_and_run('numbers/create/', fields, rules)

    def delete_numbers(self, fields):
        """
        Delete a record (contact) from an existing list
        :param fields:
        :return:
        """
        rules = {
            'ids': {'required': True, 'type': 'string'}
        }

        return self._validate_and_run('numbers/delete/', fields, rules)

    def get_numbers(self, fields):
        """
        Get extended information about numbers
        :param fields:
        :return:
        """
        rules = {
            'list_id': {'type': 'integer', 'maxlength': 32},
            'ids': {'type': 'string'},
            'limit': {'type': 'integer', 'maxlength': 32},
            'offset': {'type': 'integer', 'maxlength': 32}
        }

        return self._validate_and_run('numbers/get/', fields, rules)

    def get_unsubscribers(self):
        """
        Get list of unsubscribed numbers
        :return:
        """
        return self._validate_and_run('numbers/unsubscribers/')

    # ROUTES

    def get_routes(self, fields=None):
        """
        Get all available Routes with prices for different countries
        :param fields:
        :return:
        """
        rules = {
            'country_id': {'type': 'integer', 'maxlength': 32},
            'transactional': {'type': 'boolean'},
        }

        return self._validate_and_run('routes/getall/', fields, rules)

    # AUXILIARY TOOLS

    def number_simple_verify(self, fields):
        """
        Logical verification of number
        :param fields:
        :return:
        """
        rules = {
            'number': {'required': True, 'type': 'string'},
            'country_id': {'type': 'integer', 'maxlength': 32}
        }

        return self._validate_and_run('verify/number-simple/', fields, rules)

    def number_hlr_verify(self, fields):
        """
        Verifying number by request to Home Location Register
        :param fields:
        :return:
        """
        rules = {
            'number': {'required': True, 'type': 'string'},
            'country_id': {'type': 'integer', 'maxlength': 32}
        }

        return self._validate_and_run('verify/number-hlr/', fields, rules)

    def text_analyzing(self, fields):
        """
        Verification of text before sending an SMS
        :param fields:
        :return:
        """
        rules = {
            'text': {'required': True, 'type': 'string'}
        }

        return self._validate_and_run('text/analyze/', fields, rules)

    def get_sending_report(self, fields):
        """
        This function returns a report about SMS sending process
        :param fields:
        :return:
        """
        rules = {
            'status': {'type': 'string'},
            'date_from': {'type': 'date'},
            'date_to': {'type': 'date'},
            'limit': {'type': 'integer', 'maxlength': 32},
            'offset': {'type': 'integer', 'maxlength': 32}
        }

        return self._validate_and_run('reports/sending/', fields, rules)

    def get_sending_stats(self, fields):
        """
        This function returns a statistics about SMS sending
        :param fields:
        :return:
        """
        rules = {
            'country_id': {'required': True, 'type': 'integer', 'maxlength': 32},
            'date_from': {'required': True, 'type': 'date'},
            'date_to': {'required': True, 'type': 'date'},
            'route_id': {'type': 'integer', 'maxlength': 32},
        }

        return self._validate_and_run('reports/stats/', fields, rules)

    # USER

    def get_user_details(self):
        """
        This functions returns API user details
        :return:
        """
        return self._validate_and_run('user/details/')

    # MAIN CURE FUNCTIONS

    def _validate_and_run(self, path, fields=None, rules=None):
        """
        Verify rules if exists and run _make_request if validate pass
        :param path:
        :param fields:
        :param rules:
        :return:
        """
        if fields is None:
            fields = {}

        if rules is not None:
            v = Validator(rules)
            is_valid = v.validate(fields)
            errors = v.errors
        else:
            is_valid = True
            errors = 'Unknown error'

        if is_valid:
            return self._make_request(path, fields)
        else:
            return errors

    def _make_request(self, path, fields=None):
        """
        Main function of sending request
        :param path:
        :param fields:
        :return:
        """
        if fields is None:
            fields = {}

        fields['api_key'] = self.api_key

        try:
            r = requests.post(self.endpoint + path, data=fields)
            return r.json()
        except:
            print('Can\'t proceed request')
            return None
