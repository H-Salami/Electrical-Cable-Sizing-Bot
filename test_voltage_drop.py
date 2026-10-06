from bot.calculations.cable_voltage_drop import (
    calculate_voltage_drop
)


print("شروع تست افت ولتاژ")


result = calculate_voltage_drop(

    system_type="سه فاز",

    conductor="مس",

    section=10,

    current=25,

    length=120,

    voltage=380,

    power_factor=0.9

)


print("--------------------")

print(
    "افت ولتاژ:",
    result["voltage_drop"],
    "V"
)

print(
    "درصد افت:",
    result["drop_percent"],
    "%"
)


print("--------------------")
print("تست تمام شد")