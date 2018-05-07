# --
# File: ciscota_view.py
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

#
import time


def _get_ctx_result(provides, result):
    """ Function that parse data.

    :param provides: action name
    :param result: result
    :return: context response
    """

    ctx_result = {}

    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param
    if summary:
        ctx_result['summary'] = summary

    if not data:
        ctx_result['data'] = {}
        return ctx_result

    ctx_result['action'] = provides
    ctx_result['data'] = _parse_data(data, provides)

    if provides == "get flows":
        ctx_result["columns"] = _add_columns(data)

    return ctx_result


def _add_columns(data):
    """ This function return the list of columns with contains to display in custom view.

    :param data: ctx_result["data"]
    :return: list of columns to display
    """

    columns_dict = []
    available_columns = list(set().union(*data))

    # Columns to display in view
    columns_in_sequence = [
        {"timestamp": None}, {"src_hostname": "host name"}, {"dst_hostname": "host name"},
        {"src_address": "ip"}, {"dst_address": "ip"}, {"src_port": "port"}, {"dst_port": "port"},
        {"proto": None}, {"start_timestamp": None}, {"src_scope_name": "cisco ta scope"},
        {"dst_scope_name": "cisco ta scope"}, {"vrf_name": None}, {"srtt_usec": None},
        {"total_network_latency_usec": None}, {"server_app_latency_usec": None},
        {"fwd_pkts": None}, {"rev_pkts": None}, {"fwd_bytes": None}, {"rev_bytes": None}
    ]

    # Get list of avaiable columns
    for column in columns_in_sequence:
        if set(column.keys()) < set(available_columns):
            columns_dict.append(column)

    return columns_dict


def _parse_data(data, provides):
    """ Function that parse data.

    :param data: response data
    :return: response data
    """

    if provides == 'lookup ip':
        data = data[0]
        if data.get('flow'):
            for item in data['flow']:

                if type(item['dst_scope_name']) is unicode or type(item['dst_scope_name']) is str:
                    item['dst_scope_name'] = [item['dst_scope_name']]

                if type(item['src_scope_name']) is unicode or type(item['src_scope_name']) is str:
                    item['src_scope_name'] = [item['src_scope_name']]
        return data

    if provides == "get flows":
        for item in data:
            try:
                if item.get("timestamp"):
                    item["timestamp"] = time.strftime(
                        '%b %d %I:%M:%S %p', time.localtime(time.mktime(time.strptime(item["timestamp"],
                                                                                      '%Y-%m-%dT%H:%M:%S.%fZ'))))

                if item.get('start_timestamp'):
                    item['start_timestamp'] = time.strftime('%b %d %I:%M:%S %p',
                                                            time.localtime(int(item['start_timestamp']) / 1000))

                if type(item['dst_scope_name']) is unicode or type(item['dst_scope_name']) is str:
                    item['dst_scope_name'] = [item['dst_scope_name']]

                if type(item['src_scope_name']) is unicode or type(item['src_scope_name']) is str:
                    item['src_scope_name'] = [item['src_scope_name']]

            except ValueError:
                pass

    return data


def display_view(provides, all_app_runs, context):
    """ Function that display flows.

    :param provides: action name
    :param all_app_runs: all_app_runs
    :param context: context
    :return: html page name
    """

    context['results'] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:
            ctx_result = _get_ctx_result(provides, result)
            if not ctx_result:
                continue
            results.append(ctx_result)

    if provides == "get flows":
        return_page = "ciscota_display_flows.html"
    elif provides == "lookup ip":
        return_page = "ciscota_lookup_ip.html"
    elif provides == "list user groups":
        return_page = "ciscota_display_user_group.html"
    elif provides == "list annotations":
        return_page = "ciscota_display_annotations.html"
    elif provides == "list dimensions":
        return_page = "ciscota_display_dimensions.html"
    elif provides == "list metrics":
        return_page = "ciscota_display_metrics.html"
    elif provides == "list scopes":
        return_page = "ciscota_display_scopes.html"
    else:
        return_page = "ciscota_display_vms.html"

    return return_page
