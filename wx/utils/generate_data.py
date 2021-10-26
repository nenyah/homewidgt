import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homewidgt.settings")
    django.setup()

    from goods.models import Goods

    print("clean database")
    Goods.objects.all().delete()
    names = ["苹果", "梨", "葡萄", "红提", "枣", "柑橘", "柚", "桃", "西瓜", "杏", "甜瓜",
             "香瓜", "荔枝", "甘蔗", "柿", "柠檬", "香蕉", "芒果", "菠萝",
             "哈密瓜", "李", "石榴", "枸杞", "山楂", "椰子", "桑葚", "荸荠", "柚子", "草莓",
             "沙糖桔", "木瓜", "橙", "圣女果", "龙眼", "黄瓜"]
    floors = [
        '一楼',
        '二楼',
        '三楼',
        '四楼',
    ]
    locs = [
        '冰箱',
        '茶几',
        '饭桌',
        '纸箱',
    ]
    print('create goods')
    fake = faker.Faker()
    for _ in range(100):
        Goods.objects.create(name=random.choice(names),
                             location=random.choice(floors) + "-" + random.choice(locs),
                             img='uploads/2021/09/07/nightcity.jpg',
                             exp=fake.future_datetime(end_date="+30d", tzinfo=timezone.get_current_timezone()))
    print("done")
