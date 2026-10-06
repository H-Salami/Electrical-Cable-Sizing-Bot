from reports.pdf_report import create_cable_report


print("شروع تست ساخت PDF")
print("--------------------")


data = {

    "system_type": "سه فاز",

    "voltage": 380,

    "calculated_current": 32,

    "power_factor": 0.9,

    "conductor": "مس",

    "insulation": "PVC",

    "installation": "C"

}


result = {

    "section": 10,

    "corrected_capacity": 32,

    "drop_percent": 2.94

}


file = create_cable_report(

    data,

    result

)


print(
    "فایل PDF ساخته شد:"
)

print(file)


print("--------------------")
print("تست پایان یافت")