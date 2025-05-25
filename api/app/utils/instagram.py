import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


def apply_bottom_to_top_fade(image):
    width, height = image.size
    gradient = Image.new('L', (1, height))
    for y in range(height):
        opacity = int(255 * (y / (height - 1)))
        gradient.putpixel((0, y), opacity)
    alpha_mask = gradient.resize((width, height))
    black_overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    black_overlay.putalpha(alpha_mask)
    return Image.alpha_composite(image.convert('RGBA'), black_overlay).convert('RGB')


def draw_rounded_rect(draw, rect, r, fill, round_tl=True, round_tr=True, round_br=True, round_bl=True):
    x0, y0, x1, y1 = rect

    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)

    if round_tl:
        draw.pieslice([x0, y0, x0+2*r, y0+2*r], 180, 270, fill=fill)
    else:
        draw.rectangle([x0, y0, x0+r, y0+r], fill=fill)
    if round_tr:
        draw.pieslice([x1-2*r, y0, x1, y0+2*r], 270, 360, fill=fill)
    else:
        draw.rectangle([x1-r, y0, x1, y0+r], fill=fill)
    if round_br:
        draw.pieslice([x1-2*r, y1-2*r, x1, y1], 0, 90, fill=fill)
    else:
        draw.rectangle([x1-r, y1-r, x1, y1], fill=fill)
    if round_bl:
        draw.pieslice([x0, y1-2*r, x0+2*r, y1], 90, 180, fill=fill)
    else:
        draw.rectangle([x0, y1-r, x0+r, y1], fill=fill)


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ''
    for w in words:
        test = (current + ' ' + w).strip()
        w_box = draw.textbbox((0, 0), test, font=font)
        if w_box[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

def generate_instagram_story(*, background, path):
    W, H = 1080, 1920

    bg = ImageOps.fit(Image.open(background).convert('RGB'), (W, H))
    bg = apply_bottom_to_top_fade(bg)
    bg.save(path)

def generate_instagram_poll(*, question, answers, background, path):
    W, H = 1080, 1920

    bg = ImageOps.fit(Image.open(background).convert('RGB'), (W, H))
    bg = apply_bottom_to_top_fade(bg)
    draw = ImageDraw.Draw(bg)

    pad = 150
    poll_w = W - 2 * pad
    qy = 1300

    for qs in range(40, 19, -1):
        q_font = ImageFont.truetype('DejaVuSans.ttf', qs)
        q_lines = wrap_text(draw, question, q_font, poll_w - 40)

        line_h = sum(draw.textbbox((0, 0), ln, font=q_font)[3] for ln in q_lines)
        total_h = line_h + (len(q_lines)-1)*10 + 60  # 60 for top/bottom padding
        if total_h <= 300:  # allocate max 300px height for question
            break

    q_box = (pad, qy, pad+poll_w, qy+total_h)
    draw_rounded_rect(draw, q_box, r=40, fill='#000000',
                      round_tl=True, round_tr=True, round_br=False, round_bl=False)

    y = qy + 30
    for ln in q_lines:
        w = draw.textbbox((0, 0), ln, font=q_font)[2]
        x = pad + (poll_w - w)//2
        draw.text((x, y), ln, font=q_font, fill='#FFFFFF')
        y += draw.textbbox((0, 0), ln, font=q_font)[3] + 10

    a_font = ImageFont.truetype('DejaVuSans.ttf', 30)
    btn_h = 100
    for i, ans in enumerate(answers):
        y0 = q_box[3] + i*btn_h
        box = (pad, y0, pad+poll_w, y0+btn_h)
        last = (i == len(answers)-1)
        draw_rounded_rect(draw, box, r=30, fill='#F0F0F0',
                          round_tl=False, round_tr=False, round_br=last, round_bl=last)
        bb = draw.textbbox((0, 0), ans, font=a_font)
        x = pad + (poll_w - bb[2])//2
        y = y0 + (btn_h - bb[3])//2
        draw.text((x, y), ans, font=a_font, fill='#000000')
        if not last:
            draw.line([(pad, y0+btn_h), (pad+poll_w, y0+btn_h)], fill='#C6C6C6', width=5)

    def arrow(pos):
        x, y = pos
        for dx in (-30, +30):
            draw.line([(x, y), (x+dx, y+20)], fill='white', width=5)

    arrow((W//2, H-70))
    arrow((W//2, H-90))

    bg.save(path)
