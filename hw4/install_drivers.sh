#!/usr/bin/env bash
#
#  Install WebDrivers for Linux
#  ----------------------------
#  * Binary webdrivers are required to drive Firefox and Chrome browsers from Selenium.
#  * This script will fetch the 64-bit binaries (geckodriver/chromedriver) for Linux.


set -e


install_dir="/usr/local/bin"

# geckodriver
json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
geckodriver_url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
curl -s -L $geckodriver_url | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$install_dir"
echo "latest geckodriver is now available in '$install_dir'"

# chromedriver
base_url="http://chromedriver.storage.googleapis.com"
version=$(curl -s "$base_url/LATEST_RELEASE")
filename="chromedriver_linux64.zip"
chromedriver_url="${base_url}/${version}/${filename}"
curl -sL -O# -o "$filename" "$chromedriver_url"
unzip -q "$filename"
rm "$filename"
chmod +x chromedriver
sudo mv chromedriver "$install_dir"
echo "latest chromedriver is now available in '$install_dir'"
