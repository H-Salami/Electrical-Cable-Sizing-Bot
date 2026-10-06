from bot.calculations.cable_selector import (
    select_final_cable
)



print("شروع تست انتخاب کابل")
print("--------------------")


result = select_final_cable(

    system_type="سه فاز",

    conductor="مس",

    insulation="PVC",

    installation="C",

    temperature=30,

    cable_count=1,

    current=32,

    length=120,

    voltage=380,

    power_factor=0.9,

    voltage_drop_limit=3

)



if result:

    print(
        "سطح مقطع:",
        result["section"],
        "mm²"
    )

    print(
        "ظرفیت کابل:",
        result["corrected_capacity"],
        "A"
    )

    print(
        "افت ولتاژ:",
        result["drop_percent"],
        "%"
    )


else:

    print(
        "کابل مناسب پیدا نشد"
    )


print("--------------------")
print("تست پایان یافت")