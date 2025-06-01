import requests

API_KEY: str = ""
CRED_FILE: str = "../credentials"

def loadApiKey(filename: str) -> None:
	global API_KEY
	fp = open(filename, "r")

	API_KEY = fp.read()
	fp.close()

def makeRequest() -> bytes:
	return b""