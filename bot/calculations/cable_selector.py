"""
انتخاب نهایی کابل

مراحل:
1- انتخاب کابل مناسب از نظر ظرفیت جریان
2- بررسی افت ولتاژ
3- در صورت نیاز افزایش سطح مقطع
"""


from bot.calculations.cable_capacity import (
    select_cable
)

from bot.calculations.cable_voltage_drop import (
    calculate_voltage_drop
)


# سطح مقاطع استاندارد
STANDARD_SECTIONS = [
    1.5,
    2.5,
    4,
    6,
    10,
    16,
    25,
    35,
    50,
    70,
    95,
    120,
    150,
    185,
    240,
    300
]


def select_final_cable(

    system_type,

    conductor,

    insulation,

    installation,

    temperature,

    cable_count,

    current,

    length,

    voltage,

    power_factor,

    voltage_drop_limit

):

    """
    انتخاب نهایی کابل

    مراحل:
    1- انتخاب کابل از نظر جریان
    2- بررسی افت ولتاژ
    3- افزایش سطح مقطع
    4- در صورت نیاز کابل موازی
    """



    # ---------------------------------------------
    # مرحله اول: یک کابل
    # ---------------------------------------------

    try:

        capacity_result = select_cable(

            current=current,

            conductor=conductor,

            insulation=insulation,

            installation=installation,

            temperature=temperature,

            system_type=system_type,

            number_of_cables=cable_count

        )


    except ValueError:

        capacity_result = None




    if capacity_result:


        selected_section = capacity_result["section"]


        voltage_result = calculate_voltage_drop(

            system_type=system_type,

            conductor=conductor,

            section=selected_section,

            current=current,

            length=length,

            voltage=voltage,

            power_factor=power_factor

        )


        if voltage_result:


            if voltage_result["drop_percent"] <= voltage_drop_limit:


                return {

                    "section": selected_section,

                    "parallel_count": 1,

                    "base_capacity":
                    capacity_result["base_capacity"],

                    "corrected_capacity":
                    capacity_result["corrected_capacity"],

                    "capacity":
                    capacity_result["corrected_capacity"],

                    "total_capacity":
                    capacity_result["corrected_capacity"],

                    "voltage_drop":
                    voltage_result["voltage_drop"],

                    "drop_percent":
                    voltage_result["drop_percent"],

                    "voltage_drop_percent":
                    voltage_result["drop_percent"]

                }




    # ---------------------------------------------
    # مرحله دوم: کابل موازی
    # ---------------------------------------------

    for parallel_count in range(2, 7):


        parallel_current = current / parallel_count



        try:


            capacity_result = select_cable(

                current=parallel_current,

                conductor=conductor,

                insulation=insulation,

                installation=installation,

                temperature=temperature,

                system_type=system_type,

                number_of_cables=cable_count

            )


        except ValueError:


            continue




        section = capacity_result["section"]




        voltage_result = calculate_voltage_drop(

            system_type=system_type,

            conductor=conductor,

            section=section,

            current=parallel_current,

            length=length,

            voltage=voltage,

            power_factor=power_factor

        )



        if voltage_result is None:

            continue




        if voltage_result["drop_percent"] <= voltage_drop_limit:

            # ---------------------------------------------
            # بررسی محدودیت کابل موازی
            # ---------------------------------------------

            engineering_warning = None


            if parallel_count >= 5:

              engineering_warning = (

               "جریان بسیار بالا است. "
               "استفاده از تعداد زیاد کابل موازی "
               "بررسی دقیق مسیر کابل‌کشی، "
               "حفاظت و تقسیم جریان را نیاز دارد."

            )


            return {


                "section": section,


                "parallel_count": parallel_count,


                "base_capacity":
                capacity_result["base_capacity"],


                "corrected_capacity":
                capacity_result["corrected_capacity"],


                "capacity":
                capacity_result["corrected_capacity"],


                "total_capacity":
                capacity_result["corrected_capacity"]
                *
                parallel_count,


                "single_capacity":
                capacity_result["corrected_capacity"],


                "voltage_drop":
                voltage_result["voltage_drop"],


                "drop_percent":
                voltage_result["drop_percent"],


                "voltage_drop_percent":
                voltage_result["drop_percent"],

                "engineering_warning": engineering_warning,

            }




    return None