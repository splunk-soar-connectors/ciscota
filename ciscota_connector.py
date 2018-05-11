# --
# File: ciscota_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber Corporation.
#
# --

# Standard library imports
import json
from datetime import datetime
from time import mktime
import ipaddress
from bs4 import BeautifulSoup
from tetpyclient import RestClient
from tetpyclient import tetpyclient

# Phantom imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
from phantom.vault import Vault

# Local imports
from ciscota_consts import *


class RetVal(tuple):

    def __new__(cls, val1, val2):

        return tuple.__new__(RetVal, (val1, val2))


class CiscotaConnector(BaseConnector):
    """ This is an AppConnector class that inherits the BaseConnector class. It implements various actions supported by
    ciscota and helper methods required to run the actions.
    """

    def __init__(self):

        # Calling the BaseConnector's init function
        super(CiscotaConnector, self).__init__()

        self._api_key = None
        self._api_secret = None
        self._server_url = None
        self._verify_server_cert = False

        return

    def initialize(self):
        """ This is an optional function that can be implemented by the AppConnector derived class. Since the
        configuration dictionary is already validated by the time this function is called, it's a good place to do any
        extra initialization of any internal modules. This function MUST return a value of either phantom.APP_SUCCESS or
        phantom.APP_ERROR. If this function returns phantom.APP_ERROR, then AppConnector::handle_action will not get
        called.
        """

        config = self.get_config()
        self._server_url = config[CISCO_TA_CONFIG_URL].strip("/")
        self._api_key = config[CISCO_TA_CONFIG_API_KEY]
        self._api_secret = config[CISCO_TA_CONFIG_API_SECRET]
        self._verify_server_cert = config.get(CISCO_TA_CONFIG_VERIFY_SSL, False)

        # Custom validation for IP address
        self.set_validator('ip', self._is_ip)

        return phantom.APP_SUCCESS

    def _is_ip(self, ip_address):
        """ Function that checks given address and return True if address is valid IPv4/IPv6 address.

        :param ip_address: IP address
        :return: status (success/failure)
        """

        try:
            # It validates both IPV4 and IPV6 address and throws
            # Exception if it is an invalid IP
            ipaddress.ip_address(unicode(ip_address))
        except Exception as e:
            self.debug_print("parameter 'ip' validation failed", e)
            return False

        return True

    def _make_rest_call(self, endpoint, action_result, json_body=None, method="get", timeout=None, file_path=None):
        """ Function that makes the REST call to the device. It is a generic function that can be called from various
        action handlers.

        :param endpoint: REST endpoint that needs to appended to the service address
        :param action_result: object of ActionResult class
        :param json_body: request body
        :param method: get/post/put/delete (Default method will be 'get')
        :param timeout: request timeout
        :param file_path: path of a file to upload
        :return: status success/failure (along with appropriate message), response obtained by making an API call
        """

        response_data = None

        # Prepare args
        args = {
            'api_key': self._api_key,
            'api_secret': self._api_secret,
            'verify': self._verify_server_cert
        }

        # If URL or credentials are invalid, it will throw an exception
        try:
            # Create rest_client object
            rest_client = RestClient(self._server_url, **args)
        except Exception as e:
            self.debug_print(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, CISCO_TA_ERROR_CONNECTING_SERVER),
                          response_data)

        try:
            request_func = getattr(rest_client, method)
        except AttributeError:
            self.debug_print(CISCO_TA_ERR_API_UNSUPPORTED_METHOD.format(method=method))
            # set the action_result status to error, the handler function will most probably return as is
            return RetVal(action_result.set_status(phantom.APP_ERROR, CISCO_TA_ERR_API_UNSUPPORTED_METHOD.
                                                   format(method=method)), response_data)
        except Exception as e:
            self.debug_print(CISCO_TA_EXCEPTION_OCCURRED, e)
            # set the action_result status to error, the handler function will most probably return as is
            return RetVal(action_result.set_status(phantom.APP_ERROR, CISCO_TA_EXCEPTION_OCCURRED), response_data)

        try:
            # call request_func according to parameter passed
            if method == 'upload':
                response = request_func(file_path, endpoint, json_body)  # pylint: disable=E1121
            else:
                if json_body:
                    response = request_func(endpoint, json_body=json.dumps(json_body))
                elif file_path:
                    response = request_func(file_path, endpoint)  # pylint: disable=E1121
                else:
                    if self.get_action_identifier() == 'test_asset_connectivity' and timeout:
                        response = request_func(endpoint, timeout=timeout)
                    else:
                        response = request_func(endpoint)

        except Exception as e:
            self.debug_print(CISCO_TA_EXCEPTION_OCCURRED)
            return RetVal(action_result.set_status(phantom.APP_ERROR, "{error}. Details: {details}".
                                                   format(error=CISCO_TA_ERROR_CONNECTING_SERVER, details=str(e))),
                          response_data)

        return self._process_response(response, action_result)

    def _process_empty_response(self, response, action_result):
        """ This function is used to process empty response.

        :param response: response data
        :param action_result: object of Action Result
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message)
        """

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"),
                      None)

    def _process_html_response(self, response, action_result):
        """ This function is used to process html response.

        :param response: response data
        :param action_result: object of Action Result
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message)
        """

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except Exception as e:
            error_text = "Cannot parse error details"
            self.debug_print(error_text, e)

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text.encode('utf-8'))

        message = message.replace('{', '{{').replace('}', '}}')

        if len(message) > 500:
            message = CISCO_TA_ERROR_CONNECTING_SERVER

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, response, action_result):
        """ This function is used to process json response.

        :param response: response data
        :param action_result: object of Action Result
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message)
        """

        # Try a json parse
        try:
            resp_json = response.json()
        except Exception as e:
            self.debug_print("Unable to parse the response into a dictionary", e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".
                                                   format(str(e))), None)

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        message = "Error from server. Status Code: {0} Data from server: {1}".format(response.status_code,
                                                                                     response.text.replace('{', '{{').
                                                                                     replace('}', '}}'))

        # Process the error returned in the json
        if resp_json.get('error'):
            message = "Error from server. Status Code: {0} Data from server: {1}".format(
                response.status_code, resp_json['error'])

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_text_response(self, response, action_result):
        """ This function is used to parse text response.

        :param response: response data
        :param action_result: action_result: object of Action Result
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message)
        """

        # Try a json parse
        try:
            resp_data = response.json()
        except Exception as e:
            self.debug_print("Unable to parse the response into a dictionary", e)
            resp_data = response.text

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, resp_data)

        message = "Error from server. Status Code: {0} Data from server: {1}".format(response.status_code,
                                                                                     response.text.replace('{', '{{').
                                                                                     replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, response, action_result):
        """ This function is used to process html response.

        :param response: response data
        :param action_result: object of Action Result
        :return: status phantom.APP_ERROR/phantom.APP_SUCCESS(along with appropriate message)
        """

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': response.status_code})
            action_result.add_debug_data({'r_text': response.text})
            action_result.add_debug_data({'r_headers': response.headers})

        # Process each 'Content-Type' of response separately
        # Process a json response
        if 'json' in response.headers.get('Content-Type', ''):
            return self._process_json_response(response, action_result)

        # Process an HTML response, Do this no matter what the API talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in response.headers.get('Content-Type', ''):
            return self._process_html_response(response, action_result)

        if 'text' in response.headers.get('Content-Type', ''):
            return self._process_text_response(response, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not response.text:
            return self._process_empty_response(response, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".\
            format(response.status_code, response.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _list_endpoints(self, param):
        """ This action is used to list endpoints.

        :param param: dictionary of param
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        # Querying endpoint to generate access token
        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_SENSORS_ENDPOINT, action_result=action_result, method='get')

        # Something went wrong
        if phantom.is_fail(status):
            return action_result.get_status()

        if response.get("results"):
            for item in response.get("results", []):
                action_result.add_data(item)

        # Update summary
        summary_data["total_endpoints"] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _search_flow(self, param):
        """ This is a helper function used to search the flow.

        :param param: dictionary of input parameters
        :return: response data
        """

        action_result = ActionResult()

        json_body = {
            "t1": int(mktime(datetime.now().timetuple())),
            'limit': 100
        }
        json_body['t0'] = json_body['t1'] - 86400

        filter_dict = {'type': 'or', 'filters': []}

        for key, value in param.iteritems():
            filter_dict['filters'].append({'type': 'eq', 'field': key, 'value': value})

        json_body['filter'] = filter_dict

        # Querying endpoint to generate access token
        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_FLOWSEARCH_ENDPOINT, action_result=action_result, json_body=json_body, method='post')

        # Something went wrong
        if phantom.is_fail(status):
            return action_result.set_status(phantom.APP_ERROR), None

        return action_result.set_status(phantom.APP_SUCCESS), response

    def _get_flows(self, param):
        """ This action is used to get flow.

        :param param: dictionary of param
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        # Get required parameter
        start_time = (param[CISCO_TA_JSON_START_TIME]).upper()
        end_time = (param[CISCO_TA_JSON_END_TIME]).upper()

        limit = param.get(CISCO_TA_JSON_LIMIT, "100")
        if not str(limit).isdigit() or int(limit) == 0:
            self.debug_print(CISCO_TA_LIMIT_ERROR)
            return action_result.set_status(phantom.APP_ERROR, CISCO_TA_LIMIT_ERROR)

        limit = int(limit)

        # Get optional parameter
        query_filter = param.get(CISCO_TA_JSON_FILTER, {})
        dimension = param.get(CISCO_TA_JSON_DIMENSIONS)
        metrics = param.get(CISCO_TA_JSON_METRICS)
        scope_name = param.get(CISCO_TA_JSON_SCOPE_NAME)

        json_body = dict(t0=start_time, t1=end_time, limit=limit)

        try:
            if query_filter:
                query_filter = json.loads(query_filter)
        except Exception as e:
            self.debug_print(CISCO_TA_JSON_LOADS_ERROR, e)
            return action_result.set_status(phantom.APP_ERROR, CISCO_TA_JSON_LOADS_ERROR)

        json_body[CISCO_TA_JSON_FILTER] = query_filter
        # Get optional parameter
        if scope_name:
            json_body["scopeName"] = scope_name

        if dimension:
            dimension = dimension.replace(" ", "").split(",")

            # if empty string in list, remove
            dimension = [item for item in dimension if item]
            json_body[CISCO_TA_JSON_DIMENSIONS] = dimension

        if metrics:
            metrics = metrics.replace(" ", "").split(",")

            # if empty string in list, remove
            metrics = [item for item in metrics if item]
            json_body[CISCO_TA_JSON_METRICS] = metrics

        # Querying endpoint to generate access token
        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_FLOWSEARCH_ENDPOINT, action_result=action_result, json_body=json_body, method='post')

        # Something went wrong
        if phantom.is_fail(status):
            return action_result.get_status()

        if response.get("results"):
            for item in response.get("results", []):
                action_result.add_data(item)

        # Update summary
        summary_data["total_flows"] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _lookup_ip(self, param):
        """ This function is used to lookup the IP.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        ip = param[CISCO_TA_JSON_IP]

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_SENSORS_ENDPOINT, action_result=action_result)

        if phantom.is_fail(status):
            return action_result.get_status()

        endpoint_list = []
        for result in response['results']:
            for interface in result['interfaces']:
                if interface[CISCO_TA_JSON_IP] == ip:
                    # if IP is same, add into list
                    endpoint_list.append(result)
                    break

        flow_status, flow_response = self._search_flow(param={'src_address': ip, 'dst_address': ip})

        if phantom.is_fail(flow_status):
            return action_result.get_status()

        # for endpoint in endpoint_list:
        action_result.add_data({'endpoints': endpoint_list, 'flow': flow_response['results']})

        summary_data['total_endpoints'] = len(endpoint_list)

        if flow_response['results']:
            summary_data['total_flows'] = len(flow_response['results'])
        else:
            summary_data['total_flows'] = 0

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_user_groups(self, param):
        """ This action is used to list user groups.

        :param param: dictionary of param
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        # Get list of user roles
        status, user_roles = self._make_rest_call(endpoint=CISCO_TA_REST_USER_ROLES_ENDPOINT, action_result=action_result)

        # Something went wrong
        if phantom.is_fail(status):
            return action_result.get_status()

        # Get list of users
        status, users = self._make_rest_call(endpoint=CISCO_TA_REST_USER_ENDPOINT, action_result=action_result)

        # Something went wrong
        if phantom.is_fail(status):
            return action_result.get_status()

        # Iterate through all the users
        for user in users:
            for role_id in user.get('role_ids', []):
                for role_dict in user_roles:
                    if role_dict['id'] == role_id:
                        users_of_roles = role_dict.get('users', [])
                        users_of_roles.append(user)
                        role_dict.update({'users': users_of_roles})

        # Add the rules to action_result data
        for role_dict in user_roles:
            action_result.add_data(role_dict)

        # Update Summary
        summary_data['total_roles'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _test_asset_connectivity(self, param):
        """ This function tests the connectivity of an asset with given credentials.

        :param param: (not used in this method)
        :return: status success/failure
        """

        action_result = ActionResult()

        self.save_progress(CISCO_TA_CONNECTION_TEST_MSG)
        self.save_progress(CISCO_TA_QUERY_AN_ENDPOINT)

        # Querying endpoint to generate access token
        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_DIMENSIONS_ENDPOINT, action_result=action_result, timeout=15)

        # Something went wrong
        if phantom.is_fail(status):
            self.save_progress(action_result.get_message())
            self.set_status(phantom.APP_ERROR, CISCO_TA_TEST_CONNECTIVITY_FAIL)
            return action_result.get_status()

        self.set_status_save_progress(phantom.APP_SUCCESS, CISCO_TA_TEST_CONNECTIVITY_PASS)
        return action_result.get_status()

    def _list_annotations(self, param):
        """ This function is used to list annotations.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        scope_name = param[CISCO_TA_SCOPE_NAME]

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_LIST_ANNOTATIONS_ENDPOINT.format(scope_name=scope_name),
                                                action_result=action_result, method='get')

        if phantom.is_fail(status):
            return action_result.get_status()

        if response:
            # Add data in action result
            for item in response:
                action_result.add_data({'annotation_name': item})

        # Update Summary
        summary_data['total_annotations'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _flush_annotations(self, param):
        """ This function is used to clear all annotations.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        scope_name = param[CISCO_TA_SCOPE_NAME]

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_LIST_ANNOTATIONS_ENDPOINT.format(scope_name=scope_name),
                action_result=action_result, method='get')

        if phantom.is_fail(status):
            return action_result.get_status()

        message = CISCO_TA_NO_ANNOTATIONS_FOUND

        if response:
            status, response = self._make_rest_call(endpoint=CISCO_TA_REST_FLUSH_ANNOTATIONS_ENDPOINT.format(scope_name=scope_name),
                    action_result=action_result, method='post')
            if phantom.is_fail(status):
                return action_result.get_status()
            message = CISCO_TA_ANNOTATIONS_FLUSHED

        return action_result.set_status(phantom.APP_SUCCESS, status_message=message)

    def _upload_annotations(self, param):
        """ This function is used to upload annotations.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        scope_name = param[CISCO_TA_SCOPE_NAME]

        operation = param[CISCO_TA_JSON_OPERATION].lower()

        # Get optional parameter
        vault_id = param.get(CISCO_TA_JSON_VAULT_ID)
        filename = param.get(CISCO_TA_JSON_FILE_NAME)

        # Validate vault_id and filename
        if not (vault_id or filename):
            self.debug_print(CISCO_TA_MISSING_PARAMETER)
            return action_result.set_status(phantom.APP_ERROR, CISCO_TA_MISSING_PARAMETER), None

        # Get vault_id if only file name is provided
        if vault_id:
            vault_list = Vault.get_file_info(vault_id=vault_id, container_id=self.get_container_id())
        else:
            vault_list = Vault.get_file_info(container_id=self.get_container_id())

        # Iterate through each vault item in the container and compare name and size of file
        for vault in vault_list:
            if (filename and vault.get("name") == filename) or \
                    (vault_id and vault.get(CISCO_TA_JSON_VAULT_ID) == vault_id):

                # If file is not CSV file
                if (vault_id and not str(vault.get("name", "")).lower().endswith(".csv")) or \
                        (filename and not str(filename).lower().endswith(".csv")):
                    self.debug_print(CISCO_TA_INVALID_FILE_FORMAT)
                    return action_result.set_status(phantom.APP_ERROR, CISCO_TA_INVALID_FILE_FORMAT), None

                vault_id = vault.get(CISCO_TA_JSON_VAULT_ID)
                break
        # If any file or vault ID does not match
        else:
            if filename:
                message = CISCO_TA_INVALID_FILE_NAME
            else:
                message = CISCO_TA_INVALID_VAULT_ID

            self.debug_print(message)
            return action_result.set_status(phantom.APP_ERROR, message), None

        # Get file path using vault ID
        file_path = Vault.get_file_path(vault_id)

        # Prepare payload
        req_payload = [tetpyclient.MultiPartOption(key='X-Tetration-Oper', val=operation)]

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_UPLOAD_ANNOTATIONS_ENDPOINT.format(scope_name=scope_name),
                action_result=action_result, method='upload', file_path=file_path, json_body=req_payload)

        if phantom.is_fail(status):
            return action_result.get_status()

        # Add data in action result
        action_result.add_data(response)

        # Update Summary
        summary_data['warnings'] = response.get('warnings')

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_dimensions(self, param):
        """ This function is used to list all dimensions.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_DIMENSIONS_ENDPOINT, action_result=action_result, method='get')

        if phantom.is_fail(status):
            return action_result.get_status()

        for dimension in response:
            action_result.add_data({'dimension_name': dimension})

        # Update Summary
        summary_data['total_dimensions'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_metrics(self, param):
        """ This function is used to list all metrics.

        :param param: dictionary of input parameters
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_METRICS_ENDPOINT, action_result=action_result, method='get')

        if phantom.is_fail(status):
            return action_result.get_status()

        for metric in response:
            action_result.add_data({'metric_name': metric})

        # Update Summary
        summary_data['total_metrics'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _list_scopes(self, param):
        """ List all scopes.

        :param param: Dictionary of input parameters
        :return: status success/failure
        """

        action_result = self.add_action_result(ActionResult(dict(param)))
        summary_data = action_result.update_summary({})

        status, response = self._make_rest_call(endpoint=CISCO_TA_REST_LIST_SCOPES_ENDPOINT, method='get', action_result=action_result)

        if phantom.is_fail(status):
            return action_result.get_status()

        for scope in response:
            # Change all the numeric values into string format as some fields may have both string and numeric value
            scope = self._process_data(scope)
            action_result.add_data(scope)

        # Update Summary
        summary_data['total_scopes'] = action_result.get_data_size()

        return action_result.set_status(phantom.APP_SUCCESS)

    def _process_data(self, data):
        """ This function is used to convert all numeric values of dictionaries into string.``

        :param scope_dict:
        :return:
        """

        # If data is of boolean type, return
        if isinstance(data, bool):
            return data

        # If data is int or float convert it into string
        if isinstance(data, int) or isinstance(data, float):
            data = str(data)

        # If data is list, iterate through each item and call function recursively
        if isinstance(data, list):
            for index, item in enumerate(data):
                data[index] = self._process_data(item)

        # If data is dict, iterate through it and call function recursively for each value
        if isinstance(data, dict):
            for key, value in data.iteritems():
                data[key] = self._process_data(value)

        return data

    def handle_action(self, param):
        """ This function gets current action identifier and calls member function of its own to handle the action.

        :param param: dictionary which contains information about the actions to be executed
        :return: status success/failure
        """

        # Dictionary mapping each action with its corresponding actions
        action_mapping = {
            'test_asset_connectivity': self._test_asset_connectivity,
            'get_flows': self._get_flows,
            'list_endpoints': self._list_endpoints,
            'list_scopes': self._list_scopes,
            'lookup_ip': self._lookup_ip,
            'list_user_groups': self._list_user_groups,
            'list_annotations': self._list_annotations,
            'flush_annotations': self._flush_annotations,
            'upload_annotations': self._upload_annotations,
            'list_dimensions': self._list_dimensions,
            'list_metrics': self._list_metrics
        }

        action = self.get_action_identifier()
        action_execution_status = phantom.APP_SUCCESS

        if action in action_mapping.keys():
            action_function = action_mapping[action]
            action_execution_status = action_function(param)

        return action_execution_status


if __name__ == '__main__':

    import sys
    import pudb

    pudb.set_trace()
    if len(sys.argv) < 2:
        print 'No test json specified as input'
        exit(0)
    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print json.dumps(in_json, indent=4)
        connector = CiscotaConnector()
        connector.print_progress_message = True
        return_value = connector._handle_action(json.dumps(in_json), None)
        print json.dumps(json.loads(return_value), indent=4)
    exit(0)
