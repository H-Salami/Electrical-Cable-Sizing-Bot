"""
تست کامل CableBot بدون تلگرام

مراحل:
1- محاسبه جریان
2- انتخاب کابل
3- بررسی افت ولتاژ
4- ساخت گزارش PDF
"""


from bot.calculations.cable_calculator import (
    calculate_current
)


from bot.calculations.cable_selector import (
    select_final_cable
)


from reports.pdf_report import (
    create_cable_report
)



# =====================================================
# اطلاعات ورودی تست
# =====================================================


data = {


    # مشخصات سیستم

    "system_type": "سه فاز",

    "voltage": 400,


    # توان مصرفی

    "power": 35000,

    "power_unit": "وات",


    # ضریب توان

    "power_factor": 0.85,


    # طول کابل

    "length": 120,


    # مشخصات کابل

    "conductor": "مس",

    "insulation": "XLPE",


    # روش نصب

    "installation": "tray",


    # دمای محیط

    "temperature": 30,


    # تعداد کابل در گروه

    "cable_count": 1,


    # حد مجاز افت ولتاژ

    "voltage_drop": 3.0

}



print(
    "شروع تست کامل CableBot"
)

print(
    "----------------------------"
)



# =====================================================
# محاسبه جریان
# =====================================================


current = calculate_current(

    system_type=data["system_type"],

    voltage=data["voltage"],

    power=data["power"],

    power_unit=data["power_unit"],

    power_factor=data["power_factor"]

)



data["calculated_current"] = current



print(
    f"جریان طراحی: {current:.2f} A"
)



# =====================================================
# انتخاب کابل
# =====================================================


result = select_final_cable(

    current=current,

    system_type=data["system_type"],

    conductor=data["conductor"],

    insulation=data["insulation"],

    installation=data["installation"],

    temperature=data["temperature"],

    cable_count=data["cable_count"],

    voltage=data["voltage"],

    length=data["length"],

    power_factor=data["power_factor"],

    voltage_drop_limit=data["voltage_drop"]

)



if result is None:

    print(
        "❌ کابل مناسب پیدا نشد"
    )

    exit()



print()
print(
    "نتیجه انتخاب کابل"
)

print(
    "----------------------------"
)


print(
    f"سطح مقطع: {result['section']} mm²"
)


print(
    f"ظرفیت کابل: {result['capacity']:.1f} A"
)


print(
    f"افت ولتاژ: {result['voltage_drop_percent']:.2f} %"
)



# =====================================================
# ساخت PDF
# =====================================================


pdf = create_cable_report(

    data=data,

    result=result

)



print()
print(
    "PDF ساخته شد:"
)


print(
    pdf
)


print(
    "----------------------------"
)


print(
    "تست پایان یافت"
)