#!/usr/bin/env bash
# Install
# via http://askubuntu.com/questions/510056/how-to-install-google-chrome

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable


# Update

sudo apt-get --only-upgrade install google-chrome-stable