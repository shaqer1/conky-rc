#!/bin/bash
declare -A newmap 
newmap['Aries']='♈'
newmap['Taurus']='♉'
newmap['Gemini']='♊'
newmap['Cancer']='♋'
newmap['Leo']='♌'
newmap['Virgo']='♍'
newmap['Libra']='♎'
newmap['Scorpio']='♏'
newmap['Sagittarius']='♐'
newmap['Capricorn']='♑'
newmap['Aquarius']='♒'
newmap['Pisces']='♓'

declare -A monthToNum
monthToNum["Jan"]=01
monthToNum["Feb"]=02
monthToNum["Mar"]=03
monthToNum["Apr"]=04
monthToNum["May"]=05
monthToNum["Jun"]=06
monthToNum["Jul"]=07
monthToNum["Aug"]=08
monthToNum["Sep"]=09
monthToNum["Oct"]=10
monthToNum["Nov"]=11
monthToNum["Dec"]=12

wget https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx\?sign\=8 --output-document=scorpio.html -q

date=$(grep '<p><strong class="date">' scorpio.html | cut -c 25- | rev | grep -o -P ">gnorts/<.{0,}" | cut -c 10- | rev)
year=$(echo "$date" | grep -o -P ', .{0,}' | cut -c 3-)
day=$(echo "$date" | grep -o -P ' .{0,}' | cut -c 2- | rev | grep -o -P ' .{0,}' | cut -c 3- | rev)
if [ "${#day}" -eq 1 ]
then
    day="0$day"
fi
month=$(echo "$date" | grep -oe '[A-Z][a-z]* [0-9]' | cut -c 1-3)
month=${monthToNum["$month"]}
date="$year-$month-$day"
date=$(date -d $date +%s)
systemDate=$(date +'%Y-%m-%d')
systemDate=$(date -d $systemDate +%s)

if [ "$systemDate" -ne "$date" ]
then
    if [ "$systemDate" -gt "$date" ]
    then
        wget https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-tomorrow.aspx\?sign\=8 --output-document=scorpio.html -q
    else
        wget https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-yesterday.aspx\?sign\=8 --output-document=scorpio.html -q
    fi
fi

date=$(grep '<p><strong class="date">' scorpio.html | cut -c 25- | rev | grep -o -P ">gnorts/<.{0,}" | cut -c 10- | rev)
systemDayPrint=$(date +'%a, %b %d')


wget https://www.horoscope.com/star-ratings/today/scorpio --output-document=scorpioStars.html -q
horoscope=$(grep '<p><strong class="date">' scorpio.html | cut -c 49-1000 | rev | cut -c 5- | rev) 
echo "$systemDayPrint-$horoscope"  | fold -s -w 55 > /home/shafay/conkyConfigs/conkyHoros/horoscope
grep "<h3>Today's Matches</h3>" scorpio.html -A 15 > matches
grep "<h3>Sex <i" scorpioStars.html -A 8 > stars 


function getStars {
    rating=$1
    star=$2
    for(( c=1; c<=$rating; c++ )) 
    do
        star="$star ★"
    done
    echo $star
}

rating=$(cat stars | sed -n 1p | grep -o 'highlight' | wc -l)
star='${alignc}'
star=$(getStars $rating $star)
description=$(cat stars | sed -n 2p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Sex' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 3p | grep -o 'highlight' | wc -l)
star='${alignc}'
star=$(getStars $rating $star)
description=$(cat stars | sed -n 4p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Hustle' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 5p | grep -o 'highlight' | wc -l)
star='${alignc}'
star=$(getStars $rating $star)
description=$(cat stars | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Vibe' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 7p | grep -o 'highlight' | wc -l)
star='${alignc}'
star=$(getStars $rating $star)
description=$(cat stars | sed -n 8p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Success' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

echo '♥ ${alignc} ${font Symbola:size=8}🤝${alignr}💼${font DejaVu Sans Mono:size=9}                 ' >> /home/shafay/conkyConfigs/conkyHoros/horoscope
match1=$(cat matches | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev)
match2=$(cat matches | sed -n 11p | cut -c 4- | rev | cut -c 5- | rev)
match3=$(cat matches | sed -n 16p | cut -c 4- | rev | cut -c 5- | rev)
echo "$match1${newmap["$match1"]}\${alignc}$match2${newmap["$match2"]}\${alignr}$match3${newmap["$match3"]}                 " >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rm -f scorpio* matches stars wget-log*