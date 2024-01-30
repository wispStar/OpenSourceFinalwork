##创建自定义假期
##将 7 月 13 日定为“我的假日”

from datetime import date
from holidays.countries import china
class MyHolidays(china.CN):
    def _populate(self, year):
        # Call the parent class method first, then add our own
        # holidays on top
        super()._populate(year)
        self[date(year, 7, 13)] = "My Holiday"

#创建一个日历：
holidays = MyHolidays()
print(holidays.get('2023-07-13'))
#output: My Holiday
print(holidays.get('2023-10-01'))
#output: 国庆节
