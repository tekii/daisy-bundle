"""GS1"""

import re
from typing import Literal

__all__ = ["GTIN", "GLN"]


class _Base:  # pylint: disable=R0903
    def __init__(self, digits: str, re_: re.Pattern[str]) -> None:
        match = re_.match(digits)
        if match:
            self.digits: str = match[1]
            self.parity: str = match[2]
        else:
            raise ValueError

    def verify(self) -> Literal[True]:
        """Check parity and raise ValueError"""
        sum_: int = 0
        parity: int = 0
        current: int = len(self.digits) - 1
        while current >= 0:
            k: int = 1 if parity % 2 else 3
            sum_ += k * int(self.digits[current])
            current -= 1
            parity += 1
        multiple = sum_ + ((10 - (sum_ % 10)) if (sum_ % 10) else 0)
        calculated = multiple - sum_

        if int(self.parity) != calculated:
            raise ValueError

        return True

    def __str__(self) -> str:
        return self.digits + self.parity


class GTIN(_Base):
    """GS1 GTIN"""

    RE: re.Pattern[str] = re.compile(r"^(\d?\d{12})(\d)$")

    def __init__(self, digits: str) -> None:
        super().__init__(digits, GTIN.RE)

    def __str__(self) -> str:
        return super().__str__().zfill(14)


class GLN(_Base):
    """GS1 GLN"""

    RE: re.Pattern[str] = re.compile(r"^(\d{12})(\d)$")

    def __init__(self, digits: str) -> None:
        super().__init__(digits, GLN.RE)


