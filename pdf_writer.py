import reportlab.rl_config
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import config

reportlab.rl_config.warnOnMissingFontGlyphs = 0

HEIGHT = A4[1]
print(A4)

FONT_NAME = 'OsnovaPro'
FONT_NAME_LIGHT = 'OsnovaProLight'

pdfmetrics.registerFont(TTFont(FONT_NAME, 'OsnovaPro.ttf'))
pdfmetrics.registerFont(TTFont(FONT_NAME_LIGHT, 'OsnovaProLight.ttf'))


def create_multipage_pdf(filename, participants_list, trainer_name, training_name, date, place):
    pdf_config = config['pdf'] if 'pdf' in config else dict()
    mid_width = A4[0] / 2
    c = Canvas(filename, pagesize=A4, bottomup=1)
    for participant in participants_list:
        create_page(c, pdf_config, mid_width, participant, training_name, trainer_name, date, place)
        c.showPage()

    c.save()


def create_pdf(filename, trainee_name, trainer_name, training_name, date, place):
    pdf_config = config['pdf'] if 'pdf' in config else dict()
    mid_width = A4[0] / 2
    c = Canvas(filename, pagesize=A4, bottomup=0)
    create_page(c, pdf_config, mid_width, trainee_name, training_name, trainer_name, date, place)

    c.save()


def draw_quotes(c, pdf_config):
    quote_y = int(pdf_config['quote_y'])
    right_quote_x = int(pdf_config['right_quote_x'])
    left_quote_x = int(pdf_config['left_quote_x'])
    quote_width = int(pdf_config['quote_width'])
    quote_height = int(pdf_config['quote_height'])
    c.drawImage("./quote-right.png", right_quote_x, quote_y, quote_width, quote_height, mask='auto')
    c.drawImage("./quote-left.png", left_quote_x, quote_y, quote_width, quote_height, mask='auto')


def draw_logo(c, pdf_config, mid_width):
    logo_height = int(pdf_config['logo_height'])
    logo_width = int(pdf_config['logo_width'])
    logo_y = int(pdf_config['logo_y'])
    logo_x = int(mid_width - logo_width / 2)
    c.drawImage("./logo.png", logo_x, logo_y, logo_width, logo_height, mask='auto')


def create_page(c, pdf_config, mid_width, trainee_name, training_name, trainer_name, date, place):
    print_supplementary_text(c, pdf_config, mid_width)
    print_trainee_name(c, pdf_config, mid_width, trainee_name)
    print_training_title(c, pdf_config, mid_width, training_name)
    print_date_and_place(c, pdf_config, mid_width, date, place)
    print_trainer_name(c, pdf_config, trainer_name)
    draw_logo(c, pdf_config, mid_width)
    draw_quotes(c, pdf_config)


def print_supplementary_text(c, pdf_config, mid_width):
    r = int(pdf_config['blue_color_r'])
    g = int(pdf_config['blue_color_g'])
    b = int(pdf_config['blue_color_b'])
    font_size = int(pdf_config['supplementary_font_size'])
    first_line_y = int(pdf_config['supplementary_first_line_y'])
    second_line_y = int(pdf_config['supplementary_second_line_y'])

    c.setFont(FONT_NAME_LIGHT, font_size)
    c.setFillColorRGB(r / 256, g / 256, b / 256)
    c.drawCentredString(mid_width, first_line_y, 'подтверждает, что')
    c.drawCentredString(mid_width, second_line_y, 'прошёл (-ла) обучение на тренинге')


def print_trainee_name(c, pdf_config, mid_width, trainee_name):
    font_size = int(pdf_config['trainee_font_size'])
    text_y = int(pdf_config['trainee_line_y'])

    c.setFont(FONT_NAME, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    c.drawCentredString(mid_width, text_y, trainee_name)


def print_training_title(c, pdf_config, mid_width, training_title):
    font_size = int(pdf_config['training_font_size'])
    text_mid_y = int(pdf_config['training_mid_y'])
    line_height = int(pdf_config['training_line_height'])

    c.setFont(FONT_NAME, font_size)
    c.setFillColorRGB(0.0, 0.0, 0.0)
    training_name_lines = [l.strip() for l in training_title.split('\n') if l.strip() != '']
    start_top = text_mid_y + (len(training_name_lines) - 1) / 2 * line_height  # TODO: +
    line_top = start_top
    for line in training_name_lines:
        c.drawCentredString(mid_width, line_top, line)
        line_top -= line_height


def print_date_and_place(c, pdf_config, mid_width, date, place):
    font_size = int(pdf_config['training_place_date_font_size'])
    text_y = int(pdf_config['training_place_date_y'])
    line_height = int(pdf_config['training_place_date_line_height'])
    c.setFont(FONT_NAME, font_size)
    c.drawCentredString(mid_width, text_y, date)
    c.drawCentredString(mid_width, text_y - line_height, place)


def print_trainer_name(c, pdf_config, trainer_name):
    font_size = int(pdf_config['trainer_font_size'])
    left = int(pdf_config['trainer_line_x'])
    top = int(pdf_config['trainer_line_y'])
    line_height = int(pdf_config['trainer_line_height'])
    signature_line_gap = int(pdf_config['trainer_signature_line_gap'])
    signature_line_length = int(pdf_config['trainer_signature_line_length'])

    c.setFont(FONT_NAME_LIGHT, font_size)
    c.drawString(left, top, 'Бизнес-тренер:')
    second_line_y = top - line_height
    t = c.beginText(left, second_line_y)
    t.textOut(trainer_name)
    new_x, _ = t.getCursor()
    c.drawText(t)

    signature_line_x = new_x + signature_line_gap
    p = c.beginPath()
    p.moveTo(signature_line_x, second_line_y - 0.2)
    p.lineTo(signature_line_x + signature_line_length, second_line_y + 0.2)
    c.setLineWidth(0.5)
    c.drawPath(p)
