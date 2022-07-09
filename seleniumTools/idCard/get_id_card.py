import datetime
import random
from seleniumTools.address.addr import addr


class make_id_card:

    def get_id_card(self):
        """
        随机生成身份证，不限性别
        """
        # 获取100-10000天前的的年月日

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=random.randint(100, 10000))
        n_days = now - delta
        date_year = n_days.strftime('%Y%m%d')

        # 获取省市区编号和对应的地址信息
        addrIndex, addrs = addr[random.randint(0, len(addr) - 1)]

        # 身份证前17位系数
        num1 = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        number = str(addrIndex) + date_year + str(random.randint(100, 999))

        # 前17位乘系数相加和11的余数
        last_dicts = {0: 1, 1: 0, 2: "X", 3: 9, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2}
        sum1 = 0
        for index in range(len(number)):
            sum1 += int(number[index]) * num1[index]
        number += str(last_dicts[sum1 % 11])
        return number

    def get_id_card_by_sex(self, sex: int):
        """
        通过性别生成身份证id
        :param sex: 0 表示女， 1表示男
        :return:
        """
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=random.randint(100, 10000))
        n_days = now - delta
        date_year = n_days.strftime('%Y%m%d')

        # 获取省市区编号和对应的地址信息
        addrIndex, addrs = addr[random.randint(0, len(addr) - 1)]

        # 身份证前17位系数
        num1 = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        sex: str = str(random.randrange(0, 9, 2)) if sex == 0 else str(random.randrange(1, 10, 2))
        number = str(addrIndex) + date_year + str(random.randint(10, 99))  + sex

        # 前17位乘系数相加和11的余数
        last_dicts = {0: 1, 1: 0, 2: "X", 3: 9, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2}
        sum1 = 0
        for index in range(len(number)):
            sum1 += int(number[index]) * num1[index]
        number += str(last_dicts[sum1 % 11])
        return number