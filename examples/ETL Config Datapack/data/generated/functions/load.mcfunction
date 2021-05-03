scoreboard objectives add constants dummy
scoreboard players set zero constants 0
scoreboard players set one constants 1

scoreboard objectives add enabled dummy
scoreboard objectives add values dummy

# If generated = 0 (default, += 0 creates), run initialize
scoreboard players operation generated enabled += zero constants
execute if score generated enabled = zero constants run function generated:initialize
