import logging

from hw20.example.sqllitelogger import MySQLiteHandler


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # sqlite handler
    sh = MySQLiteHandler()
    sh.setLevel(logging.INFO)
    logging.getLogger().addHandler(sh)

    # test
    logging.info('Start')
    print("Hell o")
    logging.info('End')
    print(sh.exec("select * from log"))


if __name__ == '__main__':
    main()
