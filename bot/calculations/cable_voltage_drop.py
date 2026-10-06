"""
محاسبه افت ولتاژ کابل

واحدها:
جریان: A
طول: متر
مقاومت و راکتانس: Ω/km
ولتاژ: V
"""


import math

from bot.calculations.cable_voltage_data import (
    get_resistance,
    get_reactance
)



# =========================================================
# محاسبه افت ولتاژ
# =========================================================

def calculate_voltage_drop(
    system_type,
    conductor,
    section,
    current,
    length,
    voltage,
    power_factor
):
    """
    محاسبه افت ولتاژ کابل

    system_type:
        تک فاز
        سه فاز

    conductor:
        مس
        آلومینیوم

    section:
        سطح مقطع mm²

    current:
        جریان آمپر

    length:
        طول کابل متر

    voltage:
        ولتاژ سیستم

    power_factor:
        cos φ
    """


    # مقاومت کابل
    resistance = get_resistance(
        conductor,
        section
    )


    # راکتانس کابل
    reactance = get_reactance(
        section
    )


    if resistance is None:
        return None


    # تبدیل طول به کیلومتر

    length_km = length / 1000


    # محاسبه sinφ

    sin_phi = math.sqrt(
        1 - power_factor ** 2
    )


    # بخش امپدانس

    impedance_factor = (
        resistance * power_factor
        +
        reactance * sin_phi
    )


    # تک فاز

    if system_type == "تک فاز":

        delta_v = (
            2
            *
            current
            *
            length_km
            *
            impedance_factor
        )


    # سه فاز

    else:

        delta_v = (
            math.sqrt(3)
            *
            current
            *
            length_km
            *
            impedance_factor
        )


    # درصد افت ولتاژ

    drop_percent = (
        delta_v
        /
        voltage
        *
        100
    )


    return {

        "voltage_drop": round(
            delta_v,
            2
        ),

        "drop_percent": round(
            drop_percent,
            2
        )
    }