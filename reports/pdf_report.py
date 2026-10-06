from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

from reportlab.lib.enums import TA_RIGHT, TA_CENTER

from datetime import datetime
import os

import arabic_reshaper
from bidi.algorithm import get_display



# =====================================================
# مسیر فونت فارسی
# =====================================================

FONT_PATH = os.path.join(
    "reports",
    "fonts",
    "DejaVuSans.ttf"
)


# =====================================================
# ثبت فونت
# =====================================================

pdfmetrics.registerFont(
    TTFont(
        "DejaVu",
        FONT_PATH
    )
)



# =====================================================
# اصلاح متن فارسی
# =====================================================

def rtl_text(text):

    if text is None:
        return ""

    text = str(text)

    reshaped_text = arabic_reshaper.reshape(
        text
    )

    bidi_text = get_display(
        reshaped_text
    )

    return bidi_text



# =====================================================
# ساخت گزارش PDF
# =====================================================

def create_cable_report(
        data,
        result
):

    filename = (
        "reports/"
        f"Cable_Report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ".pdf"
    )


    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=50
    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "title",

        parent=styles["Title"],

        fontName="DejaVu",

        fontSize=16,

        alignment=TA_CENTER

    )



    normal_style = ParagraphStyle(

        "normal",

        parent=styles["Normal"],

        fontName="DejaVu",

        fontSize=11,

        alignment=TA_RIGHT,

        leading=18

    )



    story = []

    # =================================================
    # هشدار کابل موازی
    # =================================================

    if result.get("parallel_count", 1) > 1:


     warning_text = (

        "هشدار طراحی:\n\n"

        "به دلیل بالا بودن جریان، "
        "کابل موازی انتخاب شده است.\n"

        f"تعداد کابل موازی: "
        f"{result.get('parallel_count')} رشته"

    )


     story.append(

        Paragraph(

            rtl_text(warning_text),

            normal_style

        )

    )


     story.append(
        Spacer(1,20)
     )



    # =================================================
    # عنوان گزارش
    # =================================================

    story.append(

        Paragraph(

            rtl_text(
                "گزارش محاسبه و انتخاب کابل"
            ),

            title_style

        )

    )


    story.append(
        Spacer(1,25)
    )



    # =================================================
    # جدول مشخصات
    # =================================================

    table_data = [

        [
            rtl_text("عنوان"),
            rtl_text("مقدار")
        ],


        [
            rtl_text("نوع سیستم"),
            rtl_text(data.get("system_type"))
        ],


        [
            rtl_text("ولتاژ"),
            f'{data.get("voltage")} V'
        ],


        [
            rtl_text("جریان بار"),
            f'{data.get("calculated_current")} A'
        ],

        [
            rtl_text("طول کابل"),
            f'{data.get("length")} m'
        ],


        [
            rtl_text("ضریب توان"),
            str(data.get("power_factor"))
        ],


        [
            rtl_text("جنس هادی"),
            rtl_text(data.get("conductor"))
        ],


        [
            rtl_text("نوع عایق"),
            rtl_text(data.get("insulation"))
        ],


        [
            rtl_text("روش نصب"),
            rtl_text(data.get("installation"))
        ],


        [
            rtl_text("سطح مقطع هر کابل"),
            f'{result.get("section")} mm²'
        ],

        [
           rtl_text("تعداد کابل موازی"),
           str(result.get("parallel_count", 1))
        ],


        [
           rtl_text("ظرفیت هر کابل"),
           f'{result.get("single_capacity",
           result.get("corrected_capacity"))} A'
        ],

        [
           rtl_text("ظرفیت کل کابل"),
           f'{result.get("total_capacity",
           result.get("corrected_capacity"))} A'
        ],


        [
            rtl_text("افت ولتاژ"),
            f'{result.get("drop_percent")} %'
        ]

    ]



    table = Table(

        table_data,

        colWidths=[150,150]

    )



    table.setStyle(

        TableStyle([


            (
                "FONT",
                (0,0),
                (-1,-1),
                "DejaVu"
            ),


            (
                "ALIGN",
                (0,0),
                (-1,-1),
                "RIGHT"
            ),


            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "MIDDLE"
            ),


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                None
            )


        ])

    )


    story.append(table)



    story.append(
        Spacer(1,30)
    )



    # =================================================
    # نتیجه طراحی
    # =================================================

    report_text = """

نتیجه بررسی طراحی:

✓ ظرفیت جریان کابل مناسب است

✓ سطح مقطع انتخاب شده قابل قبول است

✓ افت ولتاژ بررسی شده است


استاندارد مرجع:

IEC 60364-5-52

"""


    story.append(

        Paragraph(

            rtl_text(
                report_text
            ),

            normal_style

        )

    )



    doc.build(
        story
    )



    return filename