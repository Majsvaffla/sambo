from datetime import date


class ISODateConverter:
    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, date_string: str) -> date:
        return date.fromisoformat(date_string)

    def to_url(self, date: date) -> str:
        return date.isoformat()
