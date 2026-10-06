from bot.calculations.cable_voltage_data import (
    get_resistance,
    get_reactance
)


print("شروع تست...")


r = get_resistance(
    "مس",
    10
)

x = get_reactance(
    10
)


print("--------------------")
print("مقاومت کابل:")
print(r, "Ω/km")

print()

print("راکتانس کابل:")
print(x, "Ω/km")


print()
print("تست تمام شد.")