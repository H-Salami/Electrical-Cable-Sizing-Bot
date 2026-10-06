# =========================================================
# محاسبه ظرفیت جریان کابل و انتخاب سطح مقطع
# =========================================================

from bot.calculations.cable_capacity_data import (
    STANDARD_SECTIONS,
    BASE_CAPACITY,
    TEMPERATURE_FACTORS,
    GROUPING_FACTORS
)


# =========================================================
# تعداد هادی‌های حامل جریان
# =========================================================

def get_loaded_conductors(system_type):
    """
    تعیین تعداد هادی‌های حامل جریان

    تک فاز:
        دو هادی حامل جریان

    سه فاز:
        سه هادی حامل جریان
    """

    if system_type == "تک فاز":
        return 2

    if system_type == "سه فاز":
        return 3

    raise ValueError("نوع سیستم نامعتبر است.")


# =========================================================
# ضریب دمای محیط
# =========================================================

def get_temperature_factor(
    insulation,
    temperature
):
    """
    دریافت ضریب اصلاح دمای محیط.

    مثال:
        PVC در 40 درجه → ضریب 0.87
        XLPE در 40 درجه → ضریب 0.91
    """

    factors = TEMPERATURE_FACTORS.get(insulation)

    if not factors:
        raise ValueError("نوع عایق نامعتبر است.")

    factor = factors.get(temperature)

    if factor is None:
        raise ValueError(
            "دمای انتخاب‌شده در جدول وجود ندارد."
        )

    return factor


# =========================================================
# ضریب گروه‌بندی
# =========================================================

def get_grouping_factor(number_of_cables):
    """
    دریافت ضریب کاهش ظرفیت به دلیل گروه‌بندی کابل‌ها.
    """

    factor = GROUPING_FACTORS.get(
        number_of_cables
    )

    if factor is None:
        raise ValueError(
            "تعداد کابل‌های گروه نامعتبر است."
        )

    return factor


# =========================================================
# ظرفیت پایه کابل
# =========================================================

def get_base_capacity(
    section,
    conductor,
    insulation,
    installation,
    loaded_conductors
):
    """
    دریافت ظرفیت پایه کابل از جدول.

    section:
        سطح مقطع کابل

    conductor:
        مس یا آلومینیوم

    insulation:
        PVC یا XLPE

    installation:
        روش نصب

    loaded_conductors:
        تعداد هادی‌های حامل جریان
    """

    try:
        capacity = BASE_CAPACITY[
            conductor
        ][
            insulation
        ][
            loaded_conductors
        ][
            installation
        ][
            section
        ]

    except KeyError:
        raise ValueError(
            "ترکیب مشخصات کابل در جدول موجود نیست."
        )

    return capacity


# =========================================================
# ظرفیت اصلاح‌شده
# =========================================================

def calculate_corrected_capacity(
    base_capacity,
    temperature_factor,
    grouping_factor
):
    """
    محاسبه ظرفیت واقعی کابل پس از اعمال ضرایب اصلاحی.

    Iz = Iz_base × Ft × Fg
    """

    return (
        base_capacity
        * temperature_factor
        * grouping_factor
    )


# =========================================================
# انتخاب کابل مناسب
# =========================================================

def select_cable(
    current,
    system_type,
    conductor,
    insulation,
    installation,
    temperature,
    number_of_cables
):
    """
    انتخاب کوچک‌ترین کابل مناسب برای جریان موردنظر.

    خروجی شامل:
        سطح مقطع
        ظرفیت پایه
        ضریب دما
        ضریب گروه‌بندی
        ظرفیت نهایی
    """

    # تعداد هادی‌های حامل جریان
    loaded_conductors = get_loaded_conductors(
        system_type
    )

    # ضریب دما
    temperature_factor = get_temperature_factor(
        insulation,
        temperature
    )

    # ضریب گروه‌بندی
    grouping_factor = get_grouping_factor(
        number_of_cables
    )

    # بررسی سطح مقاطع از کوچک به بزرگ
    for section in STANDARD_SECTIONS:

        base_capacity = get_base_capacity(
            section=section,
            conductor=conductor,
            insulation=insulation,
            installation=installation,
            loaded_conductors=loaded_conductors
        )

        corrected_capacity = (
            calculate_corrected_capacity(
                base_capacity,
                temperature_factor,
                grouping_factor
            )
        )

        # اولین کابل مناسب را انتخاب می‌کنیم
        if corrected_capacity >= current:

            return {
                "section": section,
                "base_capacity": base_capacity,
                "temperature_factor":
                    temperature_factor,
                "grouping_factor":
                    grouping_factor,
                "corrected_capacity":
                    corrected_capacity,
                "loaded_conductors":
                    loaded_conductors
            }

    # اگر هیچ سطح مقطعی مناسب نبود
    raise ValueError(
        "هیچ سطح مقطع استانداردی "
        "برای این جریان کافی نیست."
    )