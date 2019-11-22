import pkg_resources


def test_is_wheel_exists():
    """
    Проверка установленного пакета
    :return:
    """
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                      for i in installed_packages])
    assert installed_packages_list.__contains__('otus-qa==1')
