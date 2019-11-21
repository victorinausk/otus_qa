"""Linux sys info example"""
import json
import os
import platform
import subprocess
import sys


def getAllInterfaces():
    return os.listdir('/sys/class/net/')


def get_platform():
    """Platform parser"""
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def get_system_info():
    """
    Generates sysinfo in json format
    :return:
    """
    try:
        cpu_info = subprocess.check_output(['lscpu']).decode("utf8").replace("\n", "")
    except subprocess.CalledProcessError as e:
        cpu_info = str(platform.processor())
    try:
        pl = subprocess.Popen(['ps', '-U', '0'], stdout=subprocess.PIPE).communicate()[0].decode("utf8").replace("\n",
                                                                                                                 "")
    except subprocess.CalledProcessError as e:
        pass
    os_info = {
        'os_information': get_platform() + ' ' + platform.release(),
        'interpreter:': platform.architecture(),
        'node': platform.node(),
        'version': platform.version(),
        'machine': platform.machine(),
        'cpu_info': cpu_info,
        'python_core': sys.version,
        'default_path': os.getenv('PATH'),
        'network interfaces': getAllInterfaces(),
        'processes': pl
    }

    print(json.dumps(os_info, indent=4))


def test_sys_info():
    get_system_info()
