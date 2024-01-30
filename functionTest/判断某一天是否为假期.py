##判断某一天是否为假期
import holidays
from datetime import date

cn_holidays = holidays.CountryHoliday('CN')

if date(2024, 1, 1) in cn_holidays:
    print("2024.1.1("+cn_holidays.get('2024-01-01')+") is a holiday!")
else:
    print("2024.1.1 is not a holiday :(")
