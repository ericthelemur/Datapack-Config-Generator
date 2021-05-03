scoreboard objectives add constants dummy
scoreboard players set zero constants 0
scoreboard players set one constants 1

scoreboard objectives add enabled dummy
scoreboard objectives add values dummy

# If blank = 0 (default, += 0 creates), run initialize
scoreboard players operation blank enabled += zero constants
execute if score blank enabled = zero constants run function blank:initialize
