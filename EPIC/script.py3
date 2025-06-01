from requests import *

class Date:
	def __init__(self, year: int, month: int, day: int):
		self.year = year
		self.month = month
		self.day = day

	def __str__(self):
		return f"{self.year}-{self.month}-{self.day}"

class ImgType:
	NATURAL: str = "natural"
	ENHANCED: str = "enhanced"

class ApiReq:
	BASE_URL: str = "https://api.nasa.gov/EPIC/"

	API_URL: str = f"{BASE_URL}api/"
	ARCHIVE_URL: str = f"{BASE_URL}archive/"

	def __init__(self, apiKey: str):
		self.api_key: str = apiKey

	def listDates(self, imgType: str) -> list[Date]:
		output: list[Date] = []

		url: str = f"{ApiReq.API_URL}{imgType}/all?api_key={self.api_key}"

		req: Response = get(url)

		print(req.text)

		return output

# -----------------------------------------------------------------------------

API_KEY: str = ""
CRED_FILE: str = "credentials"

def loadApiKey(filename: str) -> None:
	global API_KEY
	fp = open(filename, "r")

	API_KEY = fp.read()
	fp.close()

loadApiKey(CRED_FILE)

Reqs = ApiReq(API_KEY)

Reqs.listDates(ImgType.NATURAL)