"""Module with fixtures for tests"""
import json
import os
from collections import Counter

import pytest


@pytest.fixture(scope="module", autouse=True)
def module_fixture(request):
    """Запуск окружения"""

    def fin():
        """Остановка окружения"""
        print("\n")
        print("\n================================== HW 17 ============================================================")
        print("\n")

    request.addfinalizer(fin)


def apache2_logrow(s):
    row = []
    qe = qp = None
    for s in s.replace('\r', '').replace('\n', '').split(' '):
        if qp:
            qp.append(s)
        elif '' == s:
            row.append('')
        elif '"' == s[0]:
            qp = [s]
            qe = '"'
        elif '[' == s[0]:
            qp = [s]
            qe = ']'
        else:
            row.append(s)
        l = len(s)
        if l and qe == s[-1]:
            if l == 1 or s[-2] != '\\':
                row.append(' '.join(qp)[1:-1].replace('\\' + qe, qe))
                qp = qe = None
    return row


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
    for i in get_files:
        with open(i, 'r') as logfile:
            for line in logfile.readlines():
                ip.append(apache2_logrow(line)[0])
                if str(apache2_logrow(line)[4]).__contains__("GET"):
                    get_count = get_count + 1
                if str(apache2_logrow(line)[4]).__contains__("POST"):
                    post_count = post_count + 1
                if len(long_request_list) < 10:
                    long_request_list.append(line)

                if len(long_request_list) == 10:
                    b = long_request_list[0]
                    k = 0
                    for j in range(len(long_request_list)):
                        if int(apache2_logrow(long_request_list[j])[6]) < int(apache2_logrow(b)[6]):
                            b = long_request_list[j]
                            k = j
                    long_request_list[k] = line
                if str(apache2_logrow(line)[5]).startswith('5'):
                    server_error_count = server_error_count + 1
                    k = {}
                    k["IP"] = apache2_logrow(line)[0]
                    k["Status_code"] = apache2_logrow(line)[5]
                    k["Method"] = apache2_logrow(line)[4][0:3]
                    k["Url"] = apache2_logrow(line)[4][4:apache2_logrow(line)[4].rindex(' ')]
                    server_error_list.append(k)
                if str(apache2_logrow(line)[5]).startswith('4'):
                    client_error_count = client_error_count + 1
                    k = {}
                    k["IP"] = apache2_logrow(line)[0]
                    k["Status_code"] = apache2_logrow(line)[5]
                    k["Method"] = apache2_logrow(line)[4][0:3]
                    k["Url"] = apache2_logrow(line)[4][4:apache2_logrow(line)[4].rindex(' ')]
                    client_error_list.append(k)

    get_request_count["Request_type"] = "GET REQUESTS"
    get_request_count["Request_count"] = get_count
    post_request_count["Request_type"] = "POST REQUESTS"
    post_request_count["Request_count"] = post_count
    all_request_count["Request_type"] = "ALL REQUESTS"
    all_request_count["Request_count"] = get_count + post_count

    for i in range(len(long_request_list)):
        max_index = i
        for j in range(i + 1, len(long_request_list)):
            if int(apache2_logrow(long_request_list[j])[6]) > int(apache2_logrow(long_request_list[max_index])[6]):
                max_index = j
        long_request_list[i], long_request_list[max_index] = long_request_list[max_index], long_request_list[i]

    for _ in long_request_list:
        k = {}
        k["Date_Time"] = apache2_logrow(_)[3]
        k["IP"] = apache2_logrow(line)[0]
        k["Status_code"] = apache2_logrow(line)[5]
        k["Method"] = apache2_logrow(line)[4][0:3]
        k["Url"] = apache2_logrow(line)[4][4:apache2_logrow(line)[4].rindex(' ')]
        long_time_request_list.append(k)

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
    all_statistic_list["Requests statistic"] = request_statistic_list, server_error_list,
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
