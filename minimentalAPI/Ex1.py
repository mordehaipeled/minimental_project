from datetime import datetime as date

"""
getDay() -> str = today in hebrew
getMonth() -> str = month name in hebrew
getYear() -> str = current year
getHour() -> str = the current hour
getDate() -> list = the current date in different formats
getSeason() -> list = the possible seasons (there is a month with 2 seasons)
"""


class Date:
    day_in_hebrew = {
        'Sunday': 'ראשון',
        'Monday': 'שני',
        'Tuesday': 'שלישי',
        'Wednesday': 'רביעי',
        'Thursday': 'חמישי',
        'Friday': 'שישי',
        'Saturday': 'שבת'
    }

    months_in_hebrew = {
        'January': 'ינואר',
        'February': 'פברואר',
        'March': 'מרץ',
        'April': 'אפריל',
        'May': 'מאי',
        'June': 'יוני',
        'July': 'יולי',
        'August': 'אוגוסט',
        'September': 'ספטמבר',
        'October': 'אוקטובר',
        'November': 'נובמבר',
        'December': 'דצמבר'
    }

    seasons = {
        'January': ['חורף'],
        'February': ['חורף'],
        'March': ['חורף', 'אביב'],
        'April': ['אביב'],
        'May': ['אביב'],
        'June': ['אביב', 'קיץ'],
        'July': ['קיץ'],
        'August': ['קיץ'],
        'September': ['קיץ', 'סתיו'],
        'October': ['סתיו'],
        'November': ['סתיו'],
        'December': ['סתיו', 'חורף']
    }

    def getDay(self) -> str:
        return self.day_in_hebrew[
            date.today().strftime("%A")]  # using 'day_in_hebrew' dictionary to get the name of today

    def getMonth(self) -> str:
        return self.months_in_hebrew[
            date.today().strftime("%B")]  # using 'months_in_hebrew' dictionaryget to get the name of the month

    def getYear(self) -> str:
        return date.today().strftime("%Y")  # using 'months_in_hebrew' dictionaryget to get the name of the month

    def getHour(self) -> str:
        return date.today().strftime("%H:%M")

    def getDate(self) -> list[str]:
        today = date.today()
        _date = list()
        # Format 1
        _date.append(today.strftime("%d.%m.%y"))  # dd.mm.yy
        _date.append(today.strftime("%#d.%#m.%y"))  # dd.mm.yy    (without leading zeros in day and month)
        _date.append(today.strftime("%d.%m.%Y"))  # dd.mm.yyyy
        _date.append(today.strftime("%#d.%#m.%Y"))  # dd.mm.yyyy  (without leading zeros in day and month)
        _date.append(today.strftime("%d.%m"))  # dd.mm
        _date.append(today.strftime("%#d.%#m"))  # dd.mm  (without leading zeros in day and month)
        # Format 2
        _date.append(today.strftime("%d/%m/%y"))  # dd/mm/yy
        _date.append(today.strftime("%#d/%#m/%y"))  # dd/mm/yy    (without leading zeros in day and month)
        _date.append(today.strftime("%d/%m/%Y"))  # dd/mm/yyyy
        _date.append(today.strftime("%#d/%#m/%Y"))  # dd/mm/yyyy  (without leading zeros in day and month)
        _date.append(today.strftime("%d/%m"))  # dd/mm
        _date.append(today.strftime("%#d/%#m"))  # dd/mm  (without leading zeros in day and month)
        # Format 3
        _date.append(today.strftime("%d-%m-%y"))  # dd-mm-yy
        _date.append(today.strftime("%#d-%#m-%y"))  # dd-mm-yy    (without leading zeros in day and month)
        _date.append(today.strftime("%d-%m-%Y"))  # dd-mm-yyyy
        _date.append(today.strftime("%#d-%#m-%Y"))  # dd-mm-yyyy  (without leading zeros in day and month)
        _date.append(today.strftime("%d-%m"))  # dd-mm
        _date.append(today.strftime("%#d-%#m"))  # dd-mm  (without leading zeros in day and month)
        # Format 4
        _date.append(today.strftime("%d:%m:%y"))  # dd:mm:yy
        _date.append(today.strftime("%#d:%#m:%y"))  # dd:mm:yy    (without leading zeros in day and month)
        _date.append(today.strftime("%d:%m:%Y"))  # dd:mm:yyyy
        _date.append(today.strftime("%#d:%#m:%Y"))  # dd:mm:yyyy  (without leading zeros in day and month)
        _date.append(today.strftime("%d:%m"))  # dd:mm
        _date.append(today.strftime("%#d:%#m"))  # dd:mm  (without leading zeros in day and month)

        return _date

    def getSeason(self) -> list[str]:
        return self.seasons[date.today().strftime("%B")]

