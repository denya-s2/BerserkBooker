function Write-Info  { param([string]$msg) Write-Host ('[BB_SETUP_INFO] ' + $msg) -ForegroundColor Green }
function Write-Warn  { param([string]$msg) Write-Host ('[BB_SETUP_WARN] ' + $msg) -ForegroundColor Yellow }
function Write-Err   { param([string]$msg) Write-Host ('[BB_SETUP_ERR]  ' + $msg) -ForegroundColor Red }

$ErrorActionPreference = 'Stop'

Write-Info 'Checking for Python3...'

$pythonCmd = $null
foreach ($cmd in @('python3', 'python', 'py')) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match 'Python 3') {
            $pythonCmd = $cmd
            break
        }
    } catch { continue }
}

if (-not $pythonCmd) {
    Write-Err 'Python3 is not installed or not in PATH. Please install Python3.12+.'
    exit 1
}

# Parse version
$versionOutput = & $pythonCmd --version 2>&1
if ($versionOutput -match 'Python (\d+)\.(\d+)\.(\d+)') {
    $pyMajor = [int]$Matches[1]
    $pyMinor = [int]$Matches[2]
    $pyPatch = [int]$Matches[3]
} else {
    Write-Err ('Could not parse Python version from: ' + $versionOutput)
    exit 1
}

Write-Info ('Found Python3 version: ' + $pyMajor + '.' + $pyMinor + '.' + $pyPatch + ' (using ' + $pythonCmd + ')')

if ($pyMajor -lt 3 -or ($pyMajor -eq 3 -and $pyMinor -lt 12)) {
    Write-Warn ('Python3 version ' + $pyMajor + '.' + $pyMinor + '.' + $pyPatch + ' is below 3.12. Some features may not work correctly.')
}

$chromeDir = '.\chrome-win64-146.0.7680.165'
$chromeDllXz = 'chrome.dll.xz'
$chromeDll = 'chrome.dll'
$chromeDllFullPath = $chromeDir + '\' + $chromeDll
$chromeDllXzFullPath = $chromeDir + '\' + $chromeDllxz

$chromeBinaries = @(
    'chrome.exe',
    'chrome-wrapper.exe',
    'chrome_sandbox.exe',
    'chrome_crashpad_handler.exe'
)

Write-Info ('Processing Chrome binaries in ' + $chromeDir + '...')
Write-Info ('Unpacking ' + $chromeDllXzFullPath)

$7zIsInstalled = get-wmiobject Win32_Product | Where {$_.name -match '7(-)?zip'}
if ($7zIsInstalled) {
   Write-Info ('7zip seems to be installed!') 
} else {
   Write-Info ('Installing 7zip...') 
   msiexec /i https://www.7-zip.org/a/7z2201-x64.msi /qb
   Write-Info ('Powershell may need to be restarted for changes to take effect.')
   $7zIsInstalled = get-wmiobject Win32_Product | Where {$_.name -match '7(-)?zip'}
   if ($7zIsInstalled) {
       Write-Info ('7zip is now installed!') 
   } else {
       Write-Err ('Error installing 7zip!')
       exit 1
   }
}

& 'C:\Program Files\7-Zip\7z.exe' e $chromeDllXzFullPath -o"$chromeDir" -y

$isChromeDllExtracted = test-path $chromeDllFullPath -pathtype Leaf
if ($isChromeDllExtracted) {
    Write-Info ($chromeDll + ' successfully extracted!')
} else {
    Write-Err ('Extracting ' + $chromeDllXzFullPath + ' failed!')
    exit 1
}

foreach ($binary in $chromeBinaries) {
    $binaryPath = Join-Path $chromeDir $binary
    if (-not (Test-Path $binaryPath)) {
        Write-Warn ('Binary not found, skipping: ' + $binaryPath)
        continue
    }
    try {
        Unblock-File -Path $binaryPath
        $acl = Get-Acl $binaryPath
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            [System.Security.Principal.WindowsIdentity]::GetCurrent().Name,
            'ReadAndExecute',
            'Allow'
        )
        $acl.SetAccessRule($rule)
        Set-Acl -Path $binaryPath -AclObject $acl
        Write-Info ('Unblocked + set ReadAndExecute: ' + $binaryPath)
    } catch {
        Write-Err ('Failed to set permissions on: ' + $binaryPath + ' - ' + $_)
        exit 1
    }
}

Write-Info 'All done!'
