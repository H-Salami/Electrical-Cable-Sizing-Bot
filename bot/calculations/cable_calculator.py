import math


def calculate_current(
    system_type,
    voltage,
    power,
    power_unit,
    power_factor
):
    """
    محاسبه جریان بار

    تک فاز:
        I = P / (V × PF)

    سه فاز:
        I = P / (√3 × V × PF)

    power_unit:
        وات
        کیلووات
    """

    # تبدیل توان به وات
    if power_unit == "کیلووات":
        power_watt = power * 1000

    else:
        power_watt = power

    # بررسی ضریب توان
    if power_factor <= 0 or power_factor > 1:
        raise ValueError(
            "ضریب توان باید بین صفر و یک باشد."
        )

    # محاسبه جریان
    if system_type == "تک فاز":

        current = (
            power_watt
            / (voltage * power_factor)
        )

    elif system_type == "سه فاز":

        current = (
            power_watt
            / (
                math.sqrt(3)
                * voltage
                * power_factor
            )
        )

    else:

        raise ValueError(
            "نوع سیستم برق نامعتبر است."
        )

    return current
