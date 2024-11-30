## gorker

Google dorking with Selenium.

## Installation
```
git clone https://github.com/rix4uni/gorker.git
cd gorker
python3 setup.py install
```

## pipx
Quick setup in isolated python environment using [pipx](https://pypa.github.io/pipx/)
```
pipx install --force git+https://github.com/rix4uni/gorker.git
```

## Usage
```
usage: gorker.py [-h] [--gui] [--wait WAIT] [-o OUTPUT] [--silent] [--version] [--verbose]

Google dorking with Selenium

options:
  -h, --help            show this help message and exit
  --gui                 Run in gui mode
  --wait WAIT           reCAPTCHA wait time in seconds (default 20)
  -o OUTPUT, --output OUTPUT
                        Output file to save results
  --silent              Run without printing the banner
  --version             Show current version of gorker
  --verbose             Enable verbose mode
```

## Examples

Single URLs:
```
echo "https://www.google.com/search?q=site%3Atesla.com" | gorker
```

Multiple URLs:
```
cat dorks.txt | gorker
```

## TODO
```
-system-chrome                   Use local installed chrome ("C:\Program Files\Google\Chrome\Application\chrome.exe")
```