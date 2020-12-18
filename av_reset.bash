#!/usr/bin/bash

LOG_BASE=alpha_vantage
DIGITAL_BASE=digital_currency_list


pushd logs
mv $LOG_BASE.log tmp
counter=$(ls -t  | grep log | head -n 1 | grep -o "\..*\." | \
     cut -d "." -f 2 | awk '{print $1+1}')
mv tmp $LOG_BASE.$counter.log

printf "created new logfile backup: %s" $LOG_BASE.$counter.log
popd

pushd data
mv $DIGITAL_BASE.csv tmp
counter=$(ls -t bkp | grep digital_currency | grep -v orig | \
    head -n 1 | grep -o "\..*\." | cut -d "." -f 2 | awk '{print $1+1}')

mv tmp bkp/$DIGITAL_BASE.$counter.csv
printf "created new currencyfile backup: %s" $DIGITAL_BASE.$counter.csv

sed 's/,0$/,/g' bkp/$DIGITAL_BASE.$counter.csv > digital_currency_list.csv
printf "reset failed api requests to missing" $DIGITAL_BASE.$counter.csv
popd
