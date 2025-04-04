from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class OptiDateTimeFactory:
    """
    Factory to restrict python datetime objects used by developers and users in optiface.

    Also, knows the birthdates of core contributors for no reason aside from troubleshooting / playing with timezones.

    """

    _LUCABYEAR: int = 1996
    _LUCABMONTH: int = 9
    _LUCABDAY: int = 11
    _MILAN_TZ = ZoneInfo("Europe/Rome")

    _PETEBYEAR: int = 1997
    _NY_TZ = ZoneInfo("America/New_York")

    def optinow(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def optidefault(self) -> datetime:
        """
        For default values in problem space testing - returns Luca's birthday.
        Luca doesn't remember what time he was born, so we assume midnight in Milan.
        """
        return self.optiluca()

    def optiluca(self) -> datetime:
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

    def optipete(self) -> datetime:
        return self.optiluca()
        # return datetime(year=self._PETEBYEAR, month=, day=, tzinfo=self._NY_TZ)
