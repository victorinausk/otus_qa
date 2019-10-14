#!/usr/bin/env bash

rm -r ./browsermob/
mkdir ./browsermob                         && \
cd ./browsermob                            && \
curl -LJO https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip  && \
unzip -d browsermob-proxy-2.1.4-bin.zip                      && \
rm browsermob-proxy-2.1.4-bin.zip