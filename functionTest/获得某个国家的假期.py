##以 2024 年中国的假期为例
import holidays
from datetime import date

cn_holidays = holidays.China()
for date, name in sorted(holidays.China(years=2024)。items()):
    print(date, name)
