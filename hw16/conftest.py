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


def sort_size(e):
    return e['size']


@pytest.fixture
def request_count(get_files):
    """Fixture to count statistics"""
    get_count = 0
    post_count = 0
    server_error_count = 0
    client_error_count = 0
    ip = []
    all_request_count = {}
    get_request_count = {}
    post_request_count = {}
    long_request_list = []
    long_time_request_list = []
    server_error_list = []
    client_error_list = []
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
    ]
    pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')

    # Initiazlie required variables
    log_data = []

    # Get components from each line of the log file into a structured dict
    for i in get_files:
        with open(i, 'r') as logfile:
            for line in logfile.readlines():
                log_data.append(pattern.match(line).groupdict())

    for i in sorted(log_data, key=lambda k: k['size'], reverse=True)[0:10]:
        k = {}
        k["Date_Time"] = i['time']
        k["IP"] = i['host']
        k["Status_code"] = i['status']
        k["Method"] = i['method']
        k["Url"] = i['request']
        long_time_request_list.append(k)

    for i in list(filter(lambda k: k['status'].startswith('5'), log_data)):
        server_error_count = server_error_count + 1
        k = {}
        k["IP"] = i['host']
        k["Status_code"] = i['status']
        k["Method"] = i['method']
        k["Url"] = i['request']
        server_error_list.append(k)

    for i in list(filter(lambda k: k['status'].startswith('4'), log_data)):
        client_error_count = client_error_count + 1
        k = {}
        k["IP"] = i['host']
        k["Status_code"] = i['status']
        k["Method"] = i['method']
        k["Url"] = i['request']
        client_error_list.append(k)

    get_request_count["Request_type"] = "GET REQUESTS"
    get_request_count["Request_count"] = len(list(filter(lambda k: k['method'] == 'GET', log_data)))
    post_request_count["Request_type"] = "POST REQUESTS"
    post_request_count["Request_count"] = len(list(filter(lambda k: k['method'] == 'POST', log_data)))
    all_request_count["Request_type"] = "ALL REQUESTS"
    all_request_count["Request_count"] = len(log_data)

    request_statistic_list = []
    request_statistic_list.append(get_request_count)
    request_statistic_list.append(post_request_count)
    request_statistic_list.append(all_request_count)

    ip_list = []
    c = {}
    for key, value in Counter(ip).most_common(10):
        c["IP"] = key
        c["Count"] = value
        ip_list.append(c)

    return request_statistic_list, ip_list, long_time_request_list, server_error_list, client_error_list


@pytest.fixture
def save_to_json(request_count, request, get_files):
    """Fixture to save result yo log"""
    path = get_files[0].replace(request.config.getoption("--file_name"), '')
    print(path)
    request_statistic_list, ip_list, long_time_request_list, server_error_list, client_error_list = request_count
    all_statistic_list = {}
    all_statistic_list["Requests statistic"] = request_statistic_list, server_error_list
    all_statistic_list["Top 10 IP"] = ip_list
    all_statistic_list["Top 10 long requests"] = long_time_request_list
    all_statistic_list["Server error"] = server_error_list
    all_statistic_list["Client error"] = client_error_list
    print(all_statistic_list)
    with open(path + "data_file.json", "w") as write_file:
        json.dump(all_statistic_list, write_file)


@pytest.fixture
def log_parcer(save_to_json):
    """fixture to l"""
    current_result = find_path("data_file.json")
    return current_result
