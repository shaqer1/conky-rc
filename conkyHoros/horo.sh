#!/bin/bash
wget https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx\?sign\=8 --output-document=scorpio.html
wget https://www.horoscope.com/star-ratings/today/scorpio --output-document=scorpioStars.html
grep '<p><strong class="date">' scorpio.html | cut -c 49-1000 | rev | cut -c 5- |rev > /home/shafay/conkyConfigs/conkyHoros/horoscope
grep "<h3>Today's Matches</h3>" scorpio.html -A 15 > matches
grep "<h3>Sex <i" scorpioStars.html -A 8 > stars 


echo '♥ ${alignc} Friendship ${alignr} Career' >> /home/shafay/conkyConfigs/conkyHoros/horoscope
match1=$(cat matches | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev)
match2=$(cat matches | sed -n 11p | cut -c 4- | rev | cut -c 5- | rev)
match3=$(cat matches | sed -n 16p | cut -c 4- | rev | cut -c 5- | rev)
echo "$match1" '${alignc}' "$match2" '${alignr}' "$match3" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 1p | grep -o 'highlight' | wc -l)
description=$(cat stars | sed -n 2p | cut -c 4- | rev | cut -c 5- | rev)
echo 'Sex' "$rating" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 3p | grep -o 'highlight' | wc -l)
description=$(cat stars | sed -n 4p | cut -c 4- | rev | cut -c 5- | rev)
echo 'Hustle' "$rating" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 5p | grep -o 'highlight' | wc -l)
description=$(cat stars | sed -n 6p | cut -c 4- | rev | cut -c 5- | rev)
echo 'Vibe' "$rating" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rating=$(cat stars | sed -n 7p | grep -o 'highlight' | wc -l)
description=$(cat stars | sed -n 8p | cut -c 4- | rev | cut -c 5- | rev)
echo 'Success' "$rating" >> /home/shafay/conkyConfigs/conkyHoros/horoscope
echo "$description" >> /home/shafay/conkyConfigs/conkyHoros/horoscope

rm scorpio* matches stars