from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class OptiDateTimeFactory:
    """
    Factory to restrict python and sqlite date / time objects used by developers and users in optiface.
        - everything in sqlite gets stored without a timezone offset, in UTC / zulu time (Z).

    Knows the birthdates of core contributors for troubleshooting / playing with timezones.

    """

    _STRF_ISO8061 = "%Y-%m-%dT%H:%M:%S.%fZ"

    _LUCABYEAR: int = 1996
    _LUCABMONTH: int = 9
    _LUCABDAY: int = 11
    _MILAN_TZ = ZoneInfo("Europe/Rome")

    _PETEBYEAR: int = 1997
    _PETEBMONTH: int = 9
    _PETEBDAY: int = 6
    _NY_TZ = ZoneInfo("America/New_York")

    def sqlite_to_py(self, dt: str) -> datetime:
        return self.optiluca()

    # just for raw pysqlite, will leave in case we need for testing, sqlalchemy wants datetime objects
    def py_to_sqlite(self, dt: datetime) -> str:
        dt_utc = dt.astimezone(timezone.utc)
        return dt_utc.strftime(self._STRF_ISO8061)

    def optinow_sqlite(self) -> str:
        return self.py_to_sqlite(self.optinow())

    def optinow(self) -> datetime:
        return datetime.now(tz=timezone.utc)

    def optidefault(self) -> datetime:
        """
        For default values in problem space testing - returns Luca's birthdatetime.
        """
        return self.optiluca()

    def optiluca(self) -> datetime:
        """
        For default values in problem space testing - returns Luca's birthdatetime.
        Luca doesn't remember what time he was born, so we assume midnight in Milan.
        """
        return datetime(
            year=self._LUCABYEAR,
            month=self._LUCABMONTH,
            day=self._LUCABDAY,
            tzinfo=self._MILAN_TZ,
        )

    def optipete(self) -> datetime:
        return datetime(
            year=self._PETEBYEAR,
            month=self._PETEBMONTH,
            day=self._PETEBDAY,
            tzinfo=self._NY_TZ,
        )


if __name__ == "__main__":
    odtf = OptiDateTimeFactory()
    now = odtf.optinow()
    luca = odtf.optiluca()
    print("now, python:")
    print(now)
    print("luca, python:")
    print(luca)
    print()
    print()
    print("now, sqlite:")
    print(odtf.py_to_sqlite(now))
    print("luca, sqlite:")
    print(odtf.py_to_sqlite(luca))
