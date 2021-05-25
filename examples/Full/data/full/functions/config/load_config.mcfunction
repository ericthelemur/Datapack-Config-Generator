scoreboard objectives add constants dummy
scoreboard players set zero constants 0

scoreboard objectives add enabled dummy
scoreboard players operation full enabled += zero constants
execute if score full enabled = zero constants run function generated:config/init_config
