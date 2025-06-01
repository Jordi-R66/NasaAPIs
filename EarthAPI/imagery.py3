from requests import *

class Date:
	def __init__(self, year: int, month: int, day: int):
		self.year = year
		self.month = month
		self.day = day

	def __str__(self):
		return f"{self.year}-{self.month}-{self.day}"

API_KEY: str = ""
CRED_FILE: str = "credentials"

def loadApiKey(filename: str) -> None:
	global API_KEY
	fp = open(filename, "r")

	API_KEY = fp.read()
	fp.close()

def makeRequest() -> bytes:
	return b""