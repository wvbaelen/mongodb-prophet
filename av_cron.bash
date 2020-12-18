#!/bin/bash

cd $HOME/Develop/crypto/api

/Library/Frameworks/Python.framework/Versions/Current/bin/python \
    ./alpha_vantage_daily.py &> $HOME/cron.log
