import asyncio
import nodriver
import re
import os

USE_PYAUTOGUI=True
try:
  import pyautogui
except Exception as e:
  print(f"[BOOKERCONF->WARN] Failed to import pyautogui: {e}")
  USE_PYAUTOGUI=False

async def getMaxDisplayResolution():
  global USE_PYAUTOGUI
  screenW = None
  screenH = None
  if USE_PYAUTOGUI:
    screenW,screenH = pyautogui.size()
  if not screenW or not screenH:
    print("[BOOKERCONF->ERR] PyAutoGUI couldn't retrieve display resolution.")
    print("[BOOKERCONF->INPUT] Enter screen width in pixels (example: 1920): ")
    screenW = str(input()).strip()
    print("[BOOKERCONF->INPUT] Enter screen height in pixels (example: 1080): ")
    screenH = str(input()).strip()
  print(f"[BOOKERCONF->INFO] Screen resolution (w,h): {screenW},{screenH}px")

  return [screenW,screenH]


'''
These vars normally shouldn't be changed, unless you experience problems with running the browser, 
gov.uk sends you back an Error 15/16 page or you need to tweak the browser window size because you have a different resolution/the default doesn't work for you.
'''
defaultLogFilePath = "./notificationProxy/main/dateslogfile.log"
defaultDateBlacklistPath = "dates_blacklist.txt"
defaultTimeWhitelistPath = "times_whitelist.txt"

async def initBrowser(browserRes):
  defaultBrowserExecutablePath = "chrome-linux64-146.0.7680.165/chrome"
  defaultBrowserExecutablePathWindows = "chrome-win64-146.0.7680.165/chrome.exe"
  if os.name == 'nt':
    browserPath = defaultBrowserExecutablePathWindows
  else:
    browserPath = defaultBrowserExecutablePath
    
  nodriverCfg = nodriver.Config(user_data_dir="./temp_browser_user_data",
                                browser_executable_path = browserPath,
                                _browser_args = ["--window-position=0,0", f"--window-size={browserRes[0]},{browserRes[1]}"],
                                sandbox=True)
  nodriverCfg.add_extension("./required_extensions/0.5.5_0.crx")    # nopeCHA
  nodriverCfg.add_extension("./required_extensions/9.2_0.crx")      # foxyProxy basic 

  return await nodriver.Browser.create(config=nodriverCfg)

'''
These vars SHOULD be changed per user (fields here are placeholders)

myDrivingLicenceNumber -> string, 16 alphanumeric characters in caps
wantedTestCentres -> array of strings, names start with a capital, only English alphabet letters
preferredTestDate -> string, DD/MM/YY format
title -> string. lower/upper-case, doesn't matter (Mr, mr, MR). Other options: Mrs,Miss,Ms,Pastor,Captain,Lord,Lady,Dr,Mx,Rev,Sir
firstNames ->  string, starts with a capital, only English alphabet letters
surname -> string, starts with a capital, only English alphabet letters
myFullName -> string, words start with capitals, generated dynamically later
postcode -> string, only alpha numeric characters, UK postcode format
town -> string, starts with a capital letter
addressLineOne -> string, words start with capitals, alphanumeric characters
email -> string, email format
phoneNum -> string, uk phonenumber format
cardNumber -> string, 4 numbers 0-9 seperated with spaces
cardExpiryMonth -> string, 1 to 12 allowed
cardExpiryYear -> string, valid year in 2 letters (27,28,29)
cardHolderFullName -> string, generated dynamically later
cardSecurityCode -> string, 3 characters 0-9
'''

userVarCfg = {
    "myDrivingLicenceNumber": "AAAAAAAAAAAAAAAA",
    "wantedTestCentres": ["Guildford", "Chertsey", "Farnborough", "York"],
    "preferredTestDate": "12/12/26",
    "title": "MR",
    "firstNames": "John",
    "surname": "Smith",
    "myFullName": None,     # Leave as is, this is generated dynamically
    "postcode": "SW1A 1AA",
    "town": "London",
    "addressLineOne": "Buckingham Palace",
    "email": "nice@email.bro",
    "phoneNum": "01111111111",
    "cardNumber": "1111 1111 1111 1111",
    "cardExpiryMonth": "1",
    "cardExpiryYear": "27",
    "cardHolderFullName": None,     # Leave as is, this is generated dynamically
    "cardSecurityCode": "666"
}

userVarCfg["myFullName"] = userVarCfg["firstNames"]+" "+userVarCfg["surname"]
userVarCfg["cardHolderFullName"] = (userVarCfg["title"]+" "+userVarCfg["myFullName"]).upper()

def validateUserVarConfig(cfg: dict) -> list[str]:
  errors = []

  # myDrivingLicenceNumber — 16 alphanumeric chars, all caps
  dl = cfg.get("myDrivingLicenceNumber", "")
  if not (isinstance(dl, str) and len(dl) == 16 and dl.isalnum() and dl == dl.upper()):
    errors.append(f"myDrivingLicenceNumber invalid: '{dl}' (must be 16 alphanumeric caps)")

  # wantedTestCentres — list of strings
  wtc = cfg.get("wantedTestCentres", [])
  if not (isinstance(wtc, list) and all(isinstance(c, str) for c in wtc)):
    errors.append(f"wantedTestCentres invalid: must be a list of strings")

  # preferredTestDate — DD/MM/YY format
  ptd = cfg.get("preferredTestDate", "")
  if not re.fullmatch(r"\d{2}/\d{2}/\d{2}", ptd):
    errors.append(f"preferredTestDate invalid: '{ptd}' (must be DD/MM/YY)")

  # title — valid title string
  valid_titles = {"mr", "mrs", "miss", "ms", "pastor", "captain", "lord", "lady", "dr", "mx", "rev", "sir"} 
  title = cfg.get("title", "")
  if not (isinstance(title, str) and title.lower() in valid_titles):
    errors.append(f"title invalid: '{title}'")

  # firstNames — string
  fn = cfg.get("firstNames", "")
  if not (isinstance(fn, str) and fn.strip()):
    errors.append(f"firstNames invalid: '{fn}'")

  # surname — string
  sn = cfg.get("surname", "")
  if not (isinstance(sn, str) and sn.strip()):
    errors.append(f"surname invalid: '{sn}'")

  # myFullName — words start with capitals
  mfn = cfg.get("myFullName", "")
  if not (isinstance(mfn, str) and all(w[0].isupper() for w in mfn.split() if w)):
    errors.append(f"myFullName invalid: '{mfn}' (each word must start with capital)")

  # postcode — UK postcode format
  pc = cfg.get("postcode", "")
  if not re.fullmatch(r"[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}", pc.upper()):
    errors.append(f"postcode invalid: '{pc}'")

  # town — string with caps
  town = cfg.get("town", "")
  if not (isinstance(town, str) and town.strip() and town[0].isupper()):
    errors.append(f"town invalid: '{town}'")

  # addressLineOne — is string
  addr = cfg.get("addressLineOne", "")
  if not isinstance(addr, str):
    errors.append(f"addressLineOne invalid: '{addr}'")

  # email — basic email format
  email = cfg.get("email", "")
  if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
    errors.append(f"email invalid: '{email}'")

  # phoneNum — UK phone number (11 digits, starts with 0)
  phone = cfg.get("phoneNum", "")
  if not re.fullmatch(r"0\d{10}", phone):
    errors.append(f"phoneNum invalid: '{phone}' (must be 11 digits starting with 0)")

  # cardNumber — 4 groups of 4 digits separated by spaces
  cn = cfg.get("cardNumber", "")
  if not re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", cn):
    errors.append(f"cardNumber invalid: '{cn}'")

  # cardExpiryMonth — str, 1 to 12
  cem = cfg.get("cardExpiryMonth")
  if not (isinstance(cem, str) and 1 <= int(cem) <= 12):
    errors.append(f"cardExpiryMonth invalid: '{cem}' (must be str 1-12)")

  # cardExpiryYear — string, 2 digits
  cey = cfg.get("cardExpiryYear", "")
  if not (isinstance(cey, str) and re.fullmatch(r"\d{2}", cey)):
    errors.append(f"cardExpiryYear invalid: '{cey}' (must be 2-digit string e.g. '27')")

  # cardHolderFullName — all caps
  chfn = cfg.get("cardHolderFullName", "")
  if not (isinstance(chfn, str) and chfn == chfn.upper() and chfn.strip()):
    errors.append(f"cardHolderFullName invalid: '{chfn}' (must be all caps)")

  # cardSecurityCode — exactly 3 digits
  csc = cfg.get("cardSecurityCode", "")
  if not re.fullmatch(r"\d{3}", csc):
    errors.append(f"cardSecurityCode invalid: '{csc}' (must be 3 digits)")

  return errors

errors = validateUserVarConfig(userVarCfg)
if errors:
  print("[BOOKERCONF->ERR] Validation failed:")
  for e in errors:
    print(f"  - {e}")
  exit(1)
else:
  print("[BOOKERCONF->INFO] All user config variables are valid!")
