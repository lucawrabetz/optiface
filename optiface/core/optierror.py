from typing import TypeVar, Generic, TypeAlias

S = TypeVar("S")


class Success(Generic[S]):
    def __init__(self, value: S | None = None, title: str = "") -> None:
        self.value: S | None = value
        self.title: str = title
        self.notes: dict[str, list[str]] = dict()

    @property
    def has_errs(self) -> bool:
        raise ValueError("Called has_errs on Success type.")

    def add_note(self, note: str, file: str) -> None:
        if file not in self.notes:
            self.notes[file] = [note]
        else:
            self.notes[file].append(note)

    def add_err(self, err: str, file: str) -> None:
        raise ValueError(f"Trying to add err {err} from file {file} to a Success type.")

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap_title(self) -> str:
        return self.title

    def unwrap_err(self) -> dict[str, list[str]]:
        raise ValueError("Called unwrap_err on Success type.")

    def unwrap(self) -> S | None:
        return self.value

    def unwrap_notes(self) -> dict[str, list[str]]:
        return self.notes


class Failure(Generic[S]):
    """
    Note that Failure is typed to be Generic so the type annotations (see unwrap) perfectly align with Success.
    This is purely for type-checking, as Failure.unwrap should never be called and will raise.
    """

    def __init__(
        self,
        title: str = "",
    ) -> None:
        self.title: str = title
        self.errs: dict[str, list[str]] = dict()
        self.notes: dict[str, list[str]] = dict()

    @property
    def has_errs(self) -> bool:
        return len(self.errs) > 0

    def add_title(self, title: str) -> None:
        self.title = title

    def add_note(self, note: str, file: str) -> None:
        if file not in self.notes:
            self.notes[file] = [note]
        else:
            self.notes[file].append(note)

    def add_err(self, err: str, file: str) -> None:
        if file not in self.notes:
            self.errs[file] = [err]
        else:
            self.errs[file].append(err)

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap_title(self) -> str:
        return self.title

    def unwrap_err(self) -> dict[str, list[str]]:
        return self.errs

    def unwrap(self) -> S | None:
        raise ValueError("Called unwrap on Failure type.")

    def unwrap_notes(self) -> dict[str, list[str]]:
        return self.notes


StatusOr: TypeAlias = Success[S] | Failure[S]
Status: TypeAlias = StatusOr[None]


def main():
    print("hello")


if __name__ == "__main__":
    main()
