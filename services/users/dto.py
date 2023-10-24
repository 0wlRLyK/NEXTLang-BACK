from dataclasses import dataclass


@dataclass
class AccessRefreshTokensDTO:
    access: str
    refresh: str
