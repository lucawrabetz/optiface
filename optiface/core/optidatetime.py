from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class OptiDateTimeFactory:
    """
    Factory to restrict python datetime objects used by developers and users in optiface.
    """

    _LUCABYEAR: int = 1996
    _LUCABMONTH: int = 9
    _LUCABDAY: int = 11
    _MILAN_TZ = ZoneInfo("Europe/Rome")

    def optinow(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def optidefault(self) -> datetime:
        """
        For default values in problem space testing - returns Luca's birthday.
        Luca doesn't remember what time he was born, so we assume midnight in Milan.
        """
        return datetime(
            year=self._LUCABYEAR,
            month=self._LUCABMONTH,
            day=self._LUCABDAY,
            tzinfo=self._MILAN_TZ,
        )
