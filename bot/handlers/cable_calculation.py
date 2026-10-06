from aiogram import Router, F

from aiogram.types import (
    Message,
    CallbackQuery
)

from aiogram.fsm.context import FSMContext


from bot.states.cable_states import (
    CableCalculation
)


from bot.calculations.cable_calculator import (
    calculate_current
)


from bot.calculations.cable_selector import (
    select_final_cable
)


from reports.pdf_report import (
    create_cable_report
)


from bot.keyboards.cable_menu import (

    system_type_keyboard,

    voltage_keyboard,

    input_type_keyboard,

    power_unit_keyboard,

    power_factor_keyboard,

    conductor_keyboard,

    insulation_keyboard,

    installation_keyboard,

    temperature_keyboard,

    grouping_keyboard,

    voltage_drop_keyboard

)
from aiogram.types import FSInputFile

from bot.keyboards.main_menu import (
    main_menu
)



router = Router()



# =====================================================
# شروع محاسبه کابل
# =====================================================


@router.message(
    F.text == "⚡ محاسبه سطح مقطع کابل"
)
async def start_cable_calculation(

        message: Message,

        state: FSMContext

):


    await state.clear()



    await message.answer(

        "⚡ محاسبه سطح مقطع کابل\n\n"
        "نوع سیستم برق را انتخاب کنید:",

        reply_markup=system_type_keyboard()

    )



    await state.set_state(

        CableCalculation.system_type

    )




# =====================================================
# انتخاب نوع سیستم
# =====================================================


@router.callback_query(

    CableCalculation.system_type,

    F.data.startswith("system_")

)

async def select_system_type(

        callback: CallbackQuery,

        state: FSMContext

):


    if callback.data == "system_single":

        system = "تک فاز"


    elif callback.data == "system_three":

        system = "سه فاز"


    else:

        await callback.answer()

        return




    await state.update_data(

        system_type=system

    )



    await callback.message.edit_text(

        f"نوع سیستم: {system}\n\n"
        "ولتاژ سیستم را انتخاب کنید:",

        reply_markup=voltage_keyboard()

    )



    await state.set_state(

        CableCalculation.voltage

    )


    await callback.answer()





# =====================================================
# انتخاب ولتاژ
# =====================================================


@router.callback_query(

    CableCalculation.voltage,

    F.data.startswith("voltage_")

)

async def select_voltage(

        callback: CallbackQuery,

        state: FSMContext

):


    voltage = float(

        callback.data.replace(

            "voltage_",

            ""

        )

    )



    await state.update_data(

        voltage=voltage

    )



    await callback.message.edit_text(

        f"ولتاژ انتخاب شده: {voltage:.0f} V\n\n"
        "روش ورود اطلاعات بار را انتخاب کنید:",

        reply_markup=input_type_keyboard()

    )



    await state.set_state(

        CableCalculation.input_type

    )


    await callback.answer()




# =====================================================
# انتخاب ورود توان
# =====================================================


@router.callback_query(

    CableCalculation.input_type,

    F.data == "input_power"

)

async def select_power_input(

        callback: CallbackQuery,

        state: FSMContext

):


    await state.update_data(

        input_type="power"

    )



    await callback.message.edit_text(

        "واحد توان را انتخاب کنید:",

        reply_markup=power_unit_keyboard()

    )



    await state.set_state(

        CableCalculation.power

    )


    await callback.answer()




# =====================================================
# انتخاب واحد توان
# =====================================================


@router.callback_query(

    CableCalculation.power,

    F.data.startswith("power_unit_")

)

async def select_power_unit(

        callback: CallbackQuery,

        state: FSMContext

):


    if callback.data == "power_unit_w":

        unit = "وات"


    else:

        unit = "کیلووات"




    await state.update_data(

        power_unit=unit

    )



    await callback.message.edit_text(

        f"واحد توان: {unit}\n\n"
        "توان مصرفی را وارد کنید.\n\n"
        "مثال:\n"
        "15",

    )



    await callback.answer()




# =====================================================
# دریافت توان
# =====================================================


@router.message(

    CableCalculation.power

)

async def get_power(

        message: Message,

        state: FSMContext

):


    data = await state.get_data()



    if data.get("power_unit") is None:


        await message.answer(

            "ابتدا واحد توان را انتخاب کنید."

        )

        return




    try:


        power = float(

            message.text.replace(

                ",",

                "."

            )

        )



        if power <= 0:

            raise ValueError



    except:


        await message.answer(

            "❌ مقدار توان صحیح نیست."

        )

        return




    await state.update_data(

        power=power

    )



    await message.answer(

        "ضریب توان را انتخاب کنید:",

        reply_markup=power_factor_keyboard()

    )



    await state.set_state(

        CableCalculation.power_factor

    )





# =====================================================
# انتخاب ورود جریان
# =====================================================


@router.callback_query(

    CableCalculation.input_type,

    F.data == "input_current"

)

async def select_current_input(

        callback: CallbackQuery,

        state: FSMContext

):


    await state.update_data(

        input_type="current"

    )



    await callback.message.edit_text(

        "جریان بار را بر حسب آمپر وارد کنید:",

    )



    await state.set_state(

        CableCalculation.current

    )



    await callback.answer()
    # =====================================================
# دریافت جریان
# =====================================================


@router.message(

    CableCalculation.current

)

async def get_current(

        message: Message,

        state: FSMContext

):


    try:


        current = float(

            message.text.replace(

                ",",

                "."

            )

        )


        if current <= 0:

            raise ValueError



    except:


        await message.answer(

            "❌ مقدار جریان صحیح نیست.\n"
            "مثال:\n"
            "32"

        )

        return




    await state.update_data(

        current=current

    )



    await message.answer(

        "ضریب توان (Cos φ) را انتخاب کنید:",

        reply_markup=power_factor_keyboard()

    )



    await state.set_state(

        CableCalculation.power_factor

    )





# =====================================================
# انتخاب ضریب توان
# =====================================================


@router.callback_query(

    CableCalculation.power_factor,

    F.data.startswith("pf_")

)

async def select_power_factor(

        callback: CallbackQuery,

        state: FSMContext

):


    pf = float(

        callback.data.replace(

            "pf_",

            ""

        )

    )



    await state.update_data(

        power_factor=pf

    )



    await callback.message.edit_text(

        f"ضریب توان: {pf:.2f}\n\n"
        "طول کابل را بر حسب متر وارد کنید.\n"
        "مثال:\n"
        "120"

    )



    await state.set_state(

        CableCalculation.length

    )


    await callback.answer()




# =====================================================
# دریافت طول کابل
# =====================================================


@router.message(

    CableCalculation.length

)

async def get_length(

        message: Message,

        state: FSMContext

):


    try:


        length = float(

            message.text.replace(

                ",",

                "."

            )

        )



        if length <= 0:

            raise ValueError



    except:


        await message.answer(

            "❌ طول کابل صحیح نیست."

        )

        return




    await state.update_data(

        length=length

    )



    await message.answer(

        "جنس هادی کابل را انتخاب کنید:",

        reply_markup=conductor_keyboard()

    )



    await state.set_state(

        CableCalculation.conductor

    )





# =====================================================
# انتخاب جنس هادی
# =====================================================


@router.callback_query(

    CableCalculation.conductor,

    F.data.startswith("conductor_")

)

async def select_conductor(

        callback: CallbackQuery,

        state: FSMContext

):


    if callback.data == "conductor_copper":

        conductor = "مس"


    else:

        conductor = "آلومینیوم"




    await state.update_data(

        conductor=conductor

    )



    await callback.message.edit_text(

        f"جنس هادی: {conductor}\n\n"
        "نوع عایق را انتخاب کنید:",

        reply_markup=insulation_keyboard()

    )



    await state.set_state(

        CableCalculation.insulation

    )


    await callback.answer()




# =====================================================
# انتخاب عایق
# =====================================================


@router.callback_query(

    CableCalculation.insulation,

    F.data.startswith("insulation_")

)

async def select_insulation(

        callback: CallbackQuery,

        state: FSMContext

):


    if callback.data == "insulation_pvc":

        insulation = "PVC"


    else:

        insulation = "XLPE"




    await state.update_data(

        insulation=insulation

    )



    await callback.message.edit_text(

         f"نوع عایق: {insulation}\n\n"

         "روش نصب کابل را انتخاب کنید:\n\n"

         "A1 🔹 کابل تک رشته یا چند رشته داخل لوله در دیوار عایق شده\n"
         "A2 🔹 کابل داخل لوله در دیوار یا مصالح ساختمانی\n\n"

         "B1 🔹 کابل داخل لوله روی دیوار یا سطح نصب شده\n"
          "B2 🔹 کابل چند رشته داخل لوله یا کانال روی سطح\n\n"

         "C 🔹 کابل روی دیوار، سقف یا سطح ثابت با گردش هوا\n\n"

         "D 🔹 کابل دفن شده در زمین\n\n"

         "E 🔹 کابل در هوای آزاد با فاصله از سطوح و امکان خنک شدن\n\n"

         "F 🔹 کابل روی سینی کابل یا نردبان کابل\n\n"

         "لطفاً روش نصب را انتخاب کنید:",

        reply_markup=installation_keyboard()

    )



    await state.set_state(

        CableCalculation.installation

    )


    await callback.answer()




# =====================================================
# انتخاب روش نصب
# =====================================================


@router.callback_query(

    CableCalculation.installation,

    F.data.startswith("installation_")

)

async def select_installation(

        callback: CallbackQuery,

        state: FSMContext

):


    installation = callback.data.replace(

        "installation_",

        ""

    )



    await state.update_data(

        installation=installation

    )



    await callback.message.edit_text(

        f"روش نصب: {installation}\n\n"
        "دمای محیط را انتخاب کنید:",

        reply_markup=temperature_keyboard()

    )



    await state.set_state(

        CableCalculation.temperature

    )


    await callback.answer()




# =====================================================
# انتخاب دمای محیط
# =====================================================


@router.callback_query(

    CableCalculation.temperature,

    F.data.startswith("temperature_")

)

async def select_temperature(

        callback: CallbackQuery,

        state: FSMContext

):


    temperature = int(

        callback.data.replace(

            "temperature_",

            ""

        )

    )



    await state.update_data(

        temperature=temperature

    )



    await callback.message.edit_text(

        f"دمای محیط: {temperature} °C\n\n"
        "تعداد کابل‌های گروه را انتخاب کنید:",

        reply_markup=grouping_keyboard()

    )



    await state.set_state(

        CableCalculation.cable_count

    )


    await callback.answer()
    # =====================================================
# انتخاب تعداد کابل گروه
# =====================================================


@router.callback_query(

    CableCalculation.cable_count,

    F.data.startswith("grouping_")

)

async def select_grouping(

        callback: CallbackQuery,

        state: FSMContext

):


    cable_count = int(

        callback.data.replace(

            "grouping_",

            ""

        )

    )



    await state.update_data(

        cable_count=cable_count

    )



    await callback.message.edit_text(

        f"تعداد کابل گروه: {cable_count}\n\n"
        "حد مجاز افت ولتاژ را انتخاب کنید:",

        reply_markup=voltage_drop_keyboard()

    )



    await state.set_state(

        CableCalculation.voltage_drop

    )


    await callback.answer()





# =====================================================
# محاسبه نهایی کابل
# =====================================================


@router.callback_query(

    CableCalculation.voltage_drop,

    F.data.startswith("drop_")

)

async def calculate_final_cable(

        callback: CallbackQuery,

        state: FSMContext

):


    drop = float(

        callback.data.replace(

            "drop_",

            ""

        )

    )
    print(
     "Voltage Drop Limit =",
    drop
    )


    await state.update_data(

        voltage_drop=drop

    )



    data = await state.get_data()



    # ---------------------------------------------
    # محاسبه جریان
    # ---------------------------------------------


    if data.get("input_type") == "power":



        current = calculate_current(

            system_type=data.get(
                "system_type"
            ),

            voltage=data.get(
                "voltage"
            ),

            power=data.get(
                "power"
            ),

            power_unit=data.get(
                "power_unit"
            ),

            power_factor=data.get(
                "power_factor"
            )

        )


    else:


        current = data.get(

            "current"

        )




    await state.update_data(

        calculated_current=current

    )



    # دریافت دوباره اطلاعات

    data = await state.get_data()





    # ---------------------------------------------
    # انتخاب کابل
    # ---------------------------------------------


    cable_result = select_final_cable(

        current=current,

        system_type=data.get(
            "system_type"
        ),

        conductor=data.get(
            "conductor"
        ),

        insulation=data.get(
            "insulation"
        ),

        installation=data.get(
            "installation"
        ),

        temperature=data.get(
            "temperature"
        ),

        cable_count=data.get(
            "cable_count"
        ),

        voltage=data.get(
            "voltage"
        ),

        length=data.get(
            "length"
        ),
                power_factor=data.get(
            "power_factor"
        ),

        voltage_drop_limit=data.get(
            "voltage_drop"
        ),

    
    )



    if cable_result is None:


        await callback.message.edit_text(

        "❌ انتخاب کابل امکان‌پذیر نیست.\n\n"

        "جریان طراحی خارج از محدوده کابل‌های استاندارد موجود است.\n\n"

        "راهکارهای پیشنهادی:\n"

        "• استفاده از باس‌داکت\n"

        "• افزایش سطح ولتاژ سیستم\n"

        "• نزدیک‌تر کردن نقطه توزیع برق به مصرف‌کننده\n"

        "• بررسی طراحی چند مسیر کابل موازی"

      )


        await state.clear()

    
        from bot.keyboards.main_menu import (
         main_menu
        )


        await callback.message.answer(

         "🏠 بازگشت به منوی اصلی",

         reply_markup=main_menu()

        )


        await callback.answer()


        return





    await state.update_data(

        cable_result=cable_result

    )

    # ---------------------------------------------
    # هشدار کابل موازی
    # ---------------------------------------------

    parallel_warning = ""
    engineering_warning = ""

    if cable_result.get("engineering_warning"):

        engineering_warning = (

        "⚠️ توصیه مهندسی:\n\n"

        f"{cable_result['engineering_warning']}\n\n"

    )

    if cable_result.get("parallel_count", 1) > 1:

     parallel_warning = (

        "⚠️ هشدار طراحی:\n\n"

        "به دلیل بالا بودن جریان، "
        "استفاده از کابل‌های موازی پیشنهاد شده است.\n\n"

        f"تعداد کابل موازی: "
        f"{cable_result['parallel_count']} رشته\n\n"

    )




    # ---------------------------------------------
    # ساخت متن خلاصه
    # ---------------------------------------------


    result_text = (

        "✅ محاسبه کابل با موفقیت انجام شد\n\n"

        "━━━━━━━━━━━━━━\n"
        "📌 نتیجه انتخاب کابل\n"
        "━━━━━━━━━━━━━━\n\n"

        f"{parallel_warning}"
        f"{engineering_warning}"

        f"جریان طراحی: "
        f"{current:.2f} A\n\n"

        f"سطح مقطع هر کابل: "
        f"{cable_result['section']} mm²\n\n"

        f"تعداد کابل موازی: "
        f"{cable_result.get('parallel_count',1)} رشته\n\n"

        f"ظرفیت کل کابل: "
        f"{cable_result.get('total_capacity',
        cable_result['corrected_capacity']):.1f} A\n\n"

        f"افت ولتاژ: "
        f"{cable_result['voltage_drop']:.2f} V\n\n"

        "━━━━━━━━━━━━━━\n"

        "📄 گزارش PDF آماده است."

    )



    await callback.message.edit_text(

        result_text

    )




    # ---------------------------------------------
    # ساخت PDF
    # ---------------------------------------------


    pdf_file = create_cable_report(

        data=data,

        result=cable_result

    )




    # ---------------------------------------------
    # ارسال PDF
    # ---------------------------------------------


    document = FSInputFile(
     pdf_file
    )


     
    await callback.message.answer_document(

      document=document,

      caption=(

        "📄 گزارش مهندسی محاسبه کابل\n"
        "ساخته شده توسط CableBot"

      )

    )



    await state.clear()


    from bot.keyboards.main_menu import (
      main_menu
    )


    await callback.message.answer(

    "🏠 بازگشت به منوی اصلی",

    reply_markup=main_menu()

    )


    await callback.answer()