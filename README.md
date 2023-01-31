# Bamboodle

implements a command that will retrieve authorisation cookies for a
bamboo hr session. These cookies can then be used in subsequent
scripting

## Installation

You must install selenium and a suitable driver.

### Arch linux

in `package/arch` you will find a `PKGBUILD` file that will build a
package suitable for installing with pacman (or more likely a wrapper
around pacman that allows installation of AUR packages.

``` shell
$ cd ${REPO_HOME}/package/arch

# Install AUR package requirements
$ yay -S selenium chromedriver


# Will install dependencies that can be found via pacman
# This will pull the latest version of this repo and build a pacman package, 
# with version related to the git `SHA`
$ makepkg -s .

# Install the package you just built
$ yay -U bamboodle-git*.tar.zst
```

## Usage

``` shell
# If you have a custom domain.
$ export BAMBOOHR_DOMAIN=a-company.bamboohr.com 

# The last line are the cookies you need for scripting.
$ bamboodle <username>
Hunting for cookies for <username>
Logging into https://a-company.bamboohr.com...
Entered username
Entered password
Clicked trust button
DONE
Cookie is:

trusted_browser=XXXXX;lluidt=XXXXX;lluidh=XXXXX;llfn=Bob;lluid=XXXXX;PHPSESSID=XXXXX

# the logging is sent to stderr, so in a script something like this:
$ COOKIE=$(bamboodle <username> 2> /dev/null)


```
