# encoding=utf-8
import logging
import os.path
import time


class Logger(object):
    """
    日志输出
    """

    def __init__(self, logger: str, write_log: bool = False):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        :param logger: 日志输出名称
        :param write_log: 是否写入log文件
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 创建一个handler，用于写入日志文件
        if write_log is True:
            rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
            log_path = os.path.dirname(os.getcwd())
            log_name = log_path + rq + '.log'
            # 将日志写入文件
            fh = logging.FileHandler(log_name, 'a', 'utf-8')
            fh.setLevel(logging.DEBUG)
            # 设置一下格式
            fh.setFormatter(formatter)

            # 给logger添加handler
            self.logger.addHandler(fh)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 设置一下格式
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
