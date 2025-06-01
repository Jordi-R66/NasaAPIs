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

def makeRequest(lat: float, lng: float, fov: float=None, date: Date=None) -> tuple:
	URL: str = f"https://api.nasa.gov/planetary/earth/imagery?lon={lng}&lat={lat}"

	if (fov != None and type(fov) == float):
		fov = abs(fov)

		URL = f"{URL}&dim={fov}"

	if (date != None and type(date) == Date):
		URL = f"{URL}&date={date}"

	if (API_KEY != None and type(API_KEY) == str):
		URL = f"{URL}&api_key={API_KEY}"
	else:
		raise Exception("No api key")

	req: Response = get(URL)

	if (req.status_code == 200):
		reqAssets = get(URL.replace("imagery", "assets"))

		return req.content, reqAssets.json()

	raise Exception(f"Status code != 200, {req.status_code}\n\n{URL}\n\nRate Limit : ")

def writeData(data: bytes, filename: str):
	fp = open(filename, "wb")
	fp.write(data)
	fp.close()

testCoords: tuple[float, float] = 50.950154977518224, 1.8673541706061054
lat, lng = testCoords

img: bytes = b""
assets: dict = {}

loadApiKey(CRED_FILE)

img, assets = makeRequest(lat, lng, .2)
writeData(img, f"{lat}_{lng}.png")

print(f"Image taken @ {assets.get("date")}")