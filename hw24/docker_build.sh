echo "building docker"
LATEST_CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
echo "Latest chrome driver version:" $LATEST_CHROMEDRIVER_VERSION
docker build --build-arg CROMEDRIVER_RELEASE=$LATEST_CHROMEDRIVER_VERSION .