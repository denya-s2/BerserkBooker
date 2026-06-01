# BERSERK BOOKER (DEMO VERSION)

<div align="center">

![BERSERKBOOKERLOGO.png](https://i.postimg.cc/xdYmY9w9/BERSERKBOOKERLOGO.png)

</div>

## Changes in v1.8:
 - Fixed issues with crashes after multiple booking tasks due to the browser window not able to start (win+lin).
 - Added a `--browser_exec_path` argument to specify a custom path to the browser of your choice.
 - Added "Continue session" functionality, where the bot can click the "Continue session" button (if it's there) to continue onto the booking task.
 - General bug fixes (win+lin).

### Todo:
 - Make more stable on Windows 10/11.
 - Add Queue bypass functionality.
 - Suggest what I should also do!

## Linux setup instructions
### Automatic
`chmod +x ./linux_setup.sh && ./linux_setup.sh`
### Manual
In-case of errors with running the setup script, do `which python python3` and ensure you are running a up-to-date, non-corrupt installation of python3 (preferably 3.12.12-3.14.3), do `pip3 install -r requirements.txt`, after you ensure that goes well, unpack `chrome-linux.../chrome.xz` (`unxz chrome.xz` if it's not unpacked already) to the same dir and make binaries inside `chrome-linux.../` and `main_linux64.elf` in `notificationProxy/main/` executable using `chmod +x bin_name`.

## Windows setup instructions
### Automatic (inside Powershell)
`.\win_setup.ps1`
### Manual
In-case of errors, follow the same steps as for the manual installation for Linux, except you don't need to ensure execute permissions for any binaries like you would on Linux.
On top of that, make sure to extract chrome.dll.xz and chrome_elf.dll.xz using 7zip in the chrome-win64../ directory if that fails for you (to the same dir, leaving the names as is). 
## How to use
`BerserkBooker_v1_7_demo.elf/exe --help` for details on the command line arguments, or you can just run the executable with no arguments.
To configure variables for the booking like your full name or address -> change the values in the `varCfg.json` file (by default).

## User defined variables (modified in `varCfg.json`)
 - myDrivingLicenceNumber -> string, 16 alphanumeric characters in caps
 - wantedTestCentres -> array of strings, names start with a capital, only English alphabet letters
 - preferredTestDate -> string, DD/MM/YY format
 - title -> string. lower/upper-case, doesn't matter (Mr, mr, MR). Other options: Mrs,Miss,Ms,Pastor,Captain,Lord,Lady,Dr,Mx,Rev,Sir
 - firstNames ->  string, starts with a capital, only English alphabet letters
 - surname -> string, starts with a capital, only English alphabet letters
 - myFullName -> string, words start with capitals, generated dynamically later
 - postcode -> string, only alpha numeric characters, UK postcode format
 - town -> string, starts with a capital letter
 - addressLineOne -> string, words start with capitals, alphanumeric characters
 - email -> string, email format
 - phoneNum -> string, uk phonenumber format
 - cardNumber -> string, 4 numbers 0-9 seperated with spaces
 - cardExpiryMonth -> string, 1 to 12 allowed
 - cardExpiryYear -> string, valid year in 2 letters (27,28,29)
 - cardHolderFullName -> string, generated dynamically later
 - cardSecurityCode -> string, 3 characters 0-9

## Showcase video
https://linkly.link/2gHDB
