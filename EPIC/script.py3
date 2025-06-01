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

		if (req.status_code == 200):
			liste = req.json()

			for e in liste:
				Y, M, D = tuple(e["date"].split("-"))

				output.append(Date(int(Y), int(M), int(D)))
		else:
			raise Exception("")

		return output

	def getMetaData(self, imgType: str, getLast: bool = True, date: Date=None) -> list | dict:
		url: str = ""

		output: list | dict = None

		if (date == None or type(date) != Date):
			url = f"{ApiReq.API_URL}{imgType}/images?api_key={self.api_key}"
		else:
			url = f"{ApiReq.API_URL}{imgType}/date/{date}?api_key={self.api_key}"

		req: Response = get(url)

		if (req.status_code == 200):
			temp: list[dict] = req.json()

			if (len(temp) == 0):
				raise Exception(f"No available {imgType} image for {date}")

			if getLast:
				output = dict(temp[-1])
			else:
				output = list(temp)
		else:
			raise Exception("Can't retrieve metadata")

		return output

	def downloadFromMetaData(self, imgType: str, metadata: dict):
		urlDate: str = metadata["date"].split(" ")[0].replace("-", "/")
		filename: str = f"{metadata["image"]}.png"

		url: str = f"{ApiReq.ARCHIVE_URL}{imgType}/{urlDate}/png/{filename}?api_key={self.api_key}"

		req: Response = get(url)

		if (req.status_code == 200):
			fp = open(filename, "wb")
			fp.write(req.content)
			fp.close()
		else:
			raise Exception(f"Can't download {filename}")

	def downloadLatestImageByDate(self, imgType: str, date: Date=None):
		metadata: dict = self.getMetaData(imgType, date)

		self.downloadFromMetaData(imgType, metadata)

	def downloadAllByDate(self, imgType: str, date: Date=None):
		metadata_list: list[dict] = self.getMetaData(imgType, False, date)

		for metadata in metadata_list:
			self.downloadFromMetaData(imgType, metadata)

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

dates = Reqs.listDates(ImgType.NATURAL)