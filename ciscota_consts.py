# --
# File: ciscota_consts.py
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

CISCO_TA_CONFIG_URL = "server_url"
CISCO_TA_CONFIG_API_KEY = "api_key"
CISCO_TA_CONFIG_API_SECRET = "api_secret"
CISCO_TA_CONFIG_VERIFY_SSL = "verify_server_cert"
CISCO_TA_CONNECTION_TEST_MSG = "Querying endpoint to verify the credentials provided"
CISCO_TA_REST_DIMENSIONS_ENDPOINT = "/openapi/v1/flowsearch/dimensions"
CISCO_TA_REST_METRICS_ENDPOINT = "/openapi/v1/flowsearch/metrics"
CISCO_TA_REST_FLOWSEARCH_ENDPOINT = "/openapi/v1/flowsearch"
CISCO_TA_REST_LIST_SCOPES_ENDPOINT = "/openapi/v1/app_scopes"
CISCO_TA_REST_SENSORS_ENDPOINT = "/openapi/v1/sensors"
CISCO_TA_REST_LIST_ANNOTATIONS_ENDPOINT = "/openapi/v1/assets/cmdb/annotations/{scope_name}"
CISCO_TA_REST_UPLOAD_ANNOTATIONS_ENDPOINT = "/openapi/v1/assets/cmdb/upload/{scope_name}"
CISCO_TA_REST_FLUSH_ANNOTATIONS_ENDPOINT = "/openapi/v1/assets/cmdb/flush/{scope_name}"
CISCO_TA_REST_USER_ROLES_ENDPOINT = "/roles"
CISCO_TA_REST_USER_ENDPOINT = "/users"
CISCO_TA_ERR_API_UNSUPPORTED_METHOD = "Unsupported method {method}"
CISCO_TA_EXCEPTION_OCCURRED = "Exception occurred"
CISCO_TA_TEST_CONNECTIVITY_FAIL = "Test connectivity failed"
CISCO_TA_TEST_CONNECTIVITY_PASS = "Test Connectivity passed"
CISCO_TA_QUERY_AN_ENDPOINT = "Query an endpoint"
CISCO_TA_JSON_START_TIME = "start_time"
CISCO_TA_JSON_END_TIME = "end_time"
CISCO_TA_JSON_FILTER = "filter"
CISCO_TA_JSON_SCOPE_NAME = "scope_name"
CISCO_TA_JSON_DIMENSIONS = "dimensions"
CISCO_TA_JSON_METRICS = "metrics"
CISCO_TA_JSON_LIMIT = "limit"
CISCO_TA_JSON_LOADS_ERROR = "Error while converting string to dictionary"
CISCO_TA_LIMIT_ERROR = "Parameter limit must be a positive integer"
CISCO_TA_JSON_VAULT_ID = "vault_id"
CISCO_TA_JSON_FILE_NAME = "filename"
CISCO_TA_JSON_OPERATION = "operation"
CISCO_TA_JSON_IP = "ip"
CISCO_TA_SCOPE_NAME = "scope_name"
CISCO_TA_MISSING_PARAMETER = "At least one of the Vault ID or File name must be specified"
CISCO_TA_INVALID_VAULT_ID = "Invalid Vault ID"
CISCO_TA_INVALID_FILE_NAME = "Invalid file name"
CISCO_TA_INVALID_FILE_FORMAT = "Invalid file format"
CISCO_TA_NO_ANNOTATIONS_FOUND = "No annotations found to flush"
CISCO_TA_ANNOTATIONS_FLUSHED = "Annotations flushed successfully"
CISCO_TA_ERROR_CONNECTING_SERVER = "Error while connecting to server"
