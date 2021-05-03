# First time loading (scoreboard + constant creation, etc.)

# Required to track install
scoreboard players set generated enabled 1

scoreboard objectives add constants dummy
scoreboard players set zero constants 0
scoreboard players set one constants 1
scoreboard players set five constants 5
scoreboard players set twenty constants 20

function generated:config/initialize