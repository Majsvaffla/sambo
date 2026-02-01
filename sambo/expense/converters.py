from datetime import date, datetime


class ISODateConverter:
    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, date_string: str) -> date:
        return datetime.strptime(date_string, "%Y-%m-%d").date()

    def to_url(self, date: date) -> str:
        return date.isoformat()
