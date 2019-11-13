"""Module with fixtures for tests"""
import json
import os
import re
from collections import Counter

import pytest


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""

    def fin():
        """Остановка окружения"""
        print("\n")

    request.addfinalizer(fin)


def pytest_addoption(parser):
    """Addoption fixture:"""
    parser.addoption(
        "--file_name", default="access.log", help="file name option"
    )
    parser.addoption(
        "--folder", action="store", default=r".",
        help="folder option"
    )
    parser.addoption(
        "--file_number", action="store", default="one", help="file number option one/all"
    )


def find_path(file_name):
    """ Find file in sub dirs """
    rootdir = os.getcwd()

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file

            if filepath.endswith(file_name):
                return filepath
    raise Exception("Files not found")


@pytest.fixture
def opt_file_path(request, opt_folder):
    if opt_folder == '.':
        path = find_path(request.config.getoption("--file_name"))
    else:
        path = opt_folder + request.config.getoption("--file_name")
    yield path


@pytest.fixture
def get_files(opt_folder, opt_file_path, opt_file_number):
    """Fixture to open & return log/logs"""
    directory = opt_folder
    print(directory)
    logs = []
    if opt_file_number == "all":
        for file in os.listdir(directory):
            if file.endswith(".log"):
                logs.append(file)
    elif opt_file_number == "one":
        file = opt_file_path
        logs.append(file)
    else:
        raise Exception("Files not found")
    return logs


@pytest.fixture
def opt_folder(request):
    """folder option"""
    return request.config.getoption("--folder")


@pytest.fixture
def opt_file_number(request):
    """file number options"""
    return request.config.getoption("--file_number")


def parse_data(line):
    k = {}
    k["Date_Time"] = line['time']
    k["IP"] = line['host']
    k["Status_code"] = line['status']
    k["Method"] = line['method']
    k["Url"] = line['request']
    return k


def reg_pattern():
    # Regex for the common Apache log format.
    parts = [

        r'(?P<host>\S+)',  # host %h
        r'\S+',  # indent %l (unused)
        r'(?P<user>\S+)',  # user %u
        r'\[(?P<time>.+)\]',  # time %t
        r'"(?P<method>[A-Z]+)',  # method
        r'(?P<request>[^',  # request
        r'"]+)?',  # unused
        r'(?P<protocol>HTTP/[0-9.]+")',
        r'(?P<status>[0-9]+)',  # status %>s
        r'(?P<size>\S+)',  # size %b (careful, can be '-')
        r'"(?P<referrer>.*)"',  # referrer "%{Referer}i"
        r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
        r'(?P<resp_time>\S+)'  # response time 

    ]
    return re.compile(r'\s+'.join(parts) + r'\s*\Z')


@pytest.fixture
def get_parsed_list(get_files):
    # Get components from each line of the log file into a structured dict
    log_data = []
    pattern = reg_pattern()
    for i in get_files:
        with open(i, 'r') as logfile:
            for line in logfile.readlines():
                log_data.append(pattern.match(line).groupdict())
    return log_data


@pytest.fixture
def request_count(get_parsed_list):
    """Fixture to count statistics"""
    # Initiazlie required variables
    all_request_count = {}
    get_request_count = {}
    post_request_count = {}
    long_time_request_list = []
    server_error_list = []
    client_error_list = []

    log_data = get_parsed_list
    for resp_time in sorted(log_data, key=lambda k: k['resp_time'] and k['method'] in {'GET', 'POST'}, reverse=True)[
                     0:10]:
        long_time_request_list.append(parse_data(resp_time))

    for server_error in list(
            filter(lambda k: k['status'].startswith('5') and k['method'] in {'GET', 'POST'}, log_data))[0:10]:
        server_error_list.append(parse_data(server_error))

    for client_error in list(
            filter(lambda k: k['status'].startswith('4') and k['method'] in {'GET', 'POST'}, log_data))[0:10]:
        client_error_list.append(parse_data(client_error))

    get_request_count["Request_type"] = "GET REQUESTS"
    get_request_count["Request_count"] = len(list(filter(lambda k: k['method'] == 'GET', log_data)))
    post_request_count["Request_type"] = "POST REQUESTS"
    post_request_count["Request_count"] = len(list(filter(lambda k: k['method'] == 'POST', log_data)))
    all_request_count["Request_type"] = "ALL REQUESTS"
    all_request_count["Request_count"] = len(list(filter(lambda k: k['method'] == 'GET', log_data))) + len(
        list(filter(lambda k: k['method'] == 'POST', log_data)))

    request_statistic_list = []
    request_statistic_list.append(get_request_count)
    request_statistic_list.append(post_request_count)
    request_statistic_list.append(all_request_count)

    ip = list(map(lambda k: k['host'], list(filter(lambda k: k['method'] in {'GET', 'POST'}, log_data))))
    ip_list = []

    c = {}
    for key, value in Counter(ip).most_common(10):
        if value > 1:
            c["IP"] = key
            c["Count"] = value
            ip_list.append(c)

    return request_statistic_list, ip_list, long_time_request_list, server_error_list, client_error_list


@pytest.fixture
def save_to_json(request_count, request, get_files):
    """Fixture to save result yo log"""
    path = get_files[0].replace(request.config.getoption("--file_name"), '')
    request_statistic_list, ip_list, long_time_request_list, server_error_list, client_error_list = request_count
    all_statistic_list = {}
    all_statistic_list["Requests statistic"] = request_statistic_list
    all_statistic_list["Top 10 IP"] = ip_list
    all_statistic_list["Top 10 long requests"] = long_time_request_list
    all_statistic_list["Top 10 Server error"] = server_error_list
    all_statistic_list["Top 10 Client error"] = client_error_list
    with open(path + "data_file.json", "w") as write_file:
        json.dump(all_statistic_list, write_file, indent=2)
    print(json.dumps(all_statistic_list, indent=2))


@pytest.fixture
def log_parcer(save_to_json):
    """fixture to l"""
    current_result = find_path("data_file.json")
    return current_result
