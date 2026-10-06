from aiogram.fsm.state import State, StatesGroup


class CableCalculation(StatesGroup):

    # نوع سیستم
    system_type = State()

    # ولتاژ
    voltage = State()

    # روش ورود بار
    input_type = State()

    # توان
    power = State()

    # جریان
    current = State()

    # ضریب توان
    power_factor = State()

    # طول کابل
    length = State()

    # جنس هادی
    conductor = State()

    # نوع عایق
    insulation = State()

    # روش نصب
    installation = State()

    # دمای محیط
    temperature = State()

    # تعداد کابل
    cable_count = State()

    # افت ولتاژ مجاز
    voltage_drop = State()