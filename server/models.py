from dataclasses import dataclass
import time

@dataclass
class UserPreferences:
	timezone: str
	

@dataclass
class User:
	username: str
	password: str
	roles: list
	preferences: UserPreferences
	created_ts: float
	active: bool = True