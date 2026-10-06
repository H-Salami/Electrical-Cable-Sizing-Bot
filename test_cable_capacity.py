from bot.calculations.cable_capacity import select_cable


print("شروع تست...")
print()


result = select_cable(
    current=30,
    system_type="سه فاز",
    conductor="مس",
    insulation="PVC",
    installation="C",
    temperature=30,
    number_of_cables=1
)


print("نتیجه انتخاب کابل")
print("--------------------")

print(
    "سطح مقطع:",
    result["section"],
    "mm²"
)

print(
    "ظرفیت پایه:",
    result["base_capacity"],
    "A"
)

print(
    "ضریب دما:",
    result["temperature_factor"]
)

print(
    "ضریب گروه‌بندی:",
    result["grouping_factor"]
)

print(
    "ظرفیت نهایی:",
    round(
        result["corrected_capacity"],
        2
    ),
    "A"
)

print()
print("تست با موفقیت تمام شد.")