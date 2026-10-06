from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================================================
# نوع سیستم
# =========================================================

def system_type_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚡ تک فاز",
                    callback_data="system_single"
                ),
                InlineKeyboardButton(
                    text="⚡ سه فاز",
                    callback_data="system_three"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# ولتاژ
# =========================================================

def voltage_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="220 V",
                    callback_data="voltage_220"
                ),
                InlineKeyboardButton(
                    text="380 V",
                    callback_data="voltage_380"
                ),
                InlineKeyboardButton(
                    text="400 V",
                    callback_data="voltage_400"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# روش ورود توان
# =========================================================

def input_type_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔌 توان",
                    callback_data="input_power"
                ),
                InlineKeyboardButton(
                    text="⚡ جریان",
                    callback_data="input_current"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# واحد توان
# =========================================================

def power_unit_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="W وات",
                    callback_data="power_unit_w"
                ),
                InlineKeyboardButton(
                    text="kW کیلووات",
                    callback_data="power_unit_kw"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# ضریب توان
# =========================================================

def power_factor_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="0.80",
                    callback_data="pf_0.80"
                ),
                InlineKeyboardButton(
                    text="0.85",
                    callback_data="pf_0.85"
                ),
                InlineKeyboardButton(
                    text="0.90",
                    callback_data="pf_0.90"
                )
            ],
            [
                InlineKeyboardButton(
                    text="0.95",
                    callback_data="pf_0.95"
                ),
                InlineKeyboardButton(
                    text="1.00",
                    callback_data="pf_1.00"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# جنس هادی
# =========================================================

def conductor_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟠 مس",
                    callback_data="conductor_copper"
                ),
                InlineKeyboardButton(
                    text="⚪ آلومینیوم",
                    callback_data="conductor_aluminum"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# نوع عایق
# =========================================================

def insulation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="PVC",
                    callback_data="insulation_pvc"
                ),
                InlineKeyboardButton(
                    text="XLPE",
                    callback_data="insulation_xlpe"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# روش نصب
# =========================================================

def installation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="A1",
                    callback_data="installation_A1"
                ),
                InlineKeyboardButton(
                    text="A2",
                    callback_data="installation_A2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="B1",
                    callback_data="installation_B1"
                ),
                InlineKeyboardButton(
                    text="B2",
                    callback_data="installation_B2"
                )
            ],
            [
                InlineKeyboardButton(
                    text="C",
                    callback_data="installation_C"
                ),
                InlineKeyboardButton(
                    text="D",
                    callback_data="installation_D"
                )
            ],
            [
                InlineKeyboardButton(
                    text="E",
                    callback_data="installation_E"
                ),
                InlineKeyboardButton(
                    text="F",
                    callback_data="installation_F"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )


# =========================================================
# دمای محیط
# =========================================================

def temperature_keyboard():

    temperatures = [
        "25",
        "30",
        "35",
        "40",
        "45",
        "50"
    ]

    buttons = []

    for i in range(0, len(temperatures), 3):

        row = []

        for temperature in temperatures[i:i + 3]:

            row.append(
                InlineKeyboardButton(
                    text=f"{temperature} °C",
                    callback_data=f"temperature_{temperature}"
                )
            )

        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text="❌ انصراف",
            callback_data="cancel_calculation"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# تعداد کابل‌های گروه
# =========================================================

def grouping_keyboard():

    buttons = []

    numbers = list(range(1, 13))

    for i in range(0, len(numbers), 4):

        row = []

        for number in numbers[i:i + 4]:

            row.append(
                InlineKeyboardButton(
                    text=str(number),
                    callback_data=f"grouping_{number}"
                )
            )

        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text="❌ انصراف",
            callback_data="cancel_calculation"
        )
    ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


# =========================================================
# افت ولتاژ مجاز
# =========================================================

def voltage_drop_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="2 %",
                    callback_data="drop_2"
                ),
                InlineKeyboardButton(
                    text="3 %",
                    callback_data="drop_3"
                ),
                InlineKeyboardButton(
                    text="5 %",
                    callback_data="drop_5"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ انصراف",
                    callback_data="cancel_calculation"
                )
            ]
        ]
    )