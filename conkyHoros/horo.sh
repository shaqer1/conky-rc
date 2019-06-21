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

wget https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx\?sign\=8 --output-document=scorpio.html -q
wget https://www.horoscope.com/star-ratings/today/scorpio --output-document=scorpioStars.html -q
date=$(date +'%a %b %d %Y')
horoscope=$(grep '<p><strong class="date">' scorpio.html | cut -c 49-1000 | rev | cut -c 5- | rev) 
echo "$date - $horoscope"  | fold -s -w 55 > /home/shafay/conkyConfigs/conkyHoros/horoscope
grep "<h3>Today's Matches</h3>" scorpio.html -A 15 > matches
grep "<h3>Sex <i" scorpioStars.html -A 8 > stars 

rating=$(cat stars | sed -n 1p | grep -o 'highlight' | wc -l)
star='${alignc}'
for(( c=1; c<=$rating; c++ )) 
do
    star="$star ★"
done
description=$(cat stars | sed -n 2p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Sex' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 3p | grep -o 'highlight' | wc -l)
star='${alignc}'
for(( c=1; c<=$rating; c++ )) 
do
    star="$star ★"
done
description=$(cat stars | sed -n 4p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Hustle' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 5p | grep -o 'highlight' | wc -l)
star='${alignc}'
for(( c=1; c<=$rating; c++ )) 
do
    star="$star ★"
done
description=$(cat stars | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Vibe' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 7p | grep -o 'highlight' | wc -l)
star='${alignc}'
for(( c=1; c<=$rating; c++ )) 
do
    star="$star ★"
done
description=$(cat stars | sed -n 8p | cut -c 4- | rev | cut -c 5- | rev | fold -s -w 55)
echo 'Success' "$star" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

echo '♥ ${alignc} ${font Symbola:size=8}🤝${alignr}💼${font DejaVu Sans Mono:size=9}                 ' >> /home/shafay/conkyConfigs/conkyHoros/horoscope
match1=$(cat matches | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev)
match2=$(cat matches | sed -n 11p | cut -c 4- | rev | cut -c 5- | rev)
match3=$(cat matches | sed -n 16p | cut -c 4- | rev | cut -c 5- | rev)
echo "$match1${newmap["$match1"]}\${alignc}$match2${newmap["$match2"]}\${alignr}$match3${newmap["$match3"]}                 " >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rm -f scorpio* matches stars wget-log*