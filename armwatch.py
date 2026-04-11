

"""
I hate ts :sob:
"""

import time
import sys
import math
from PIL import Image, ImageDraw, ImageFont
sys.path.append("..")
from lib import LCD_1inch28




disp = LCD_1inch28.LCD_1inch28()
disp.Init()
disp.clear()
disp.bl_DutyCycle(55)
W, H = disp.width, disp.height  
CX, CY = W // 2, H // 2         
R = 108                          




BG_OUTER   = (10,  10,  20)   
BG_FACE    = (15,  15,  28)   
ACCENT     = (0,   255, 160)  
ACCENT_DIM = (0,   80,  50)   
PURPLE     = (110, 100, 255)  
PURPLE_DIM = (30,  28,  70)   
ORANGE     = (255, 140, 60)   
BLUE       = (80,  170, 255)  
WHITE      = (255, 255, 255)  
GREY_MID   = (120, 118, 155)  
GREY_DIM   = (50,  48,  75)   





def try_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Thin.ttf",
]
FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]

def first_font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

font_time   = first_font(FONT_PATHS, 44)      
font_date   = first_font(FONT_PATHS, 10)      
font_value  = first_font(FONT_PATHS, 20)      
font_label  = first_font(FONT_PATHS_BOLD, 7)  
font_brand  = first_font(FONT_PATHS_BOLD, 7)  





def draw_circle_bg(draw):
    """Fill outer bezel and inner face."""
    draw.ellipse((0, 0, W, H), fill=BG_OUTER)
    draw.ellipse((W//2 - R, H//2 - R, W//2 + R, H//2 + R), fill=BG_FACE)


def draw_bezel_ticks(draw):
    """Draw 12 subtle tick marks around the bezel."""
    outer = 118
    inner_long  = 110
    inner_short = 113
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        is_major = (i % 5 == 0)
        inner_r = inner_long if is_major else inner_short
        x1 = CX + outer * math.cos(angle)
        y1 = CY + outer * math.sin(angle)
        x2 = CX + inner_r * math.cos(angle)
        y2 = CY + inner_r * math.sin(angle)
        alpha = 90 if is_major else 35
        color = tuple(int(c * alpha / 255) for c in ACCENT)
        if is_major:
            draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
        else:
            draw.line([(x1, y1), (x2, y2)], fill=(40, 40, 60), width=1)


def draw_arc(draw, cx, cy, r, start_deg, end_deg, color, width=5):
    """
    Draw an arc using small line segments for smooth rendering.
    start_deg/end_deg: clockwise from 12 o'clock.
    """
    steps = 120
    start_rad = math.radians(start_deg - 90)
    end_rad   = math.radians(end_deg - 90)
    sweep = end_rad - start_rad

    pts = []
    for i in range(steps + 1):
        angle = start_rad + sweep * (i / steps)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        pts.append((x, y))

    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=color, width=width)

    
    x0, y0 = pts[0]
    xn, yn = pts[-1]
    draw.ellipse((x0-width//2, y0-width//2, x0+width//2, y0+width//2), fill=color)
    draw.ellipse((xn-width//2, yn-width//2, xn+width//2, yn+width//2), fill=color)


def draw_complication_arcs(draw, insulin_pct, glucose_pct):
    """
    Insulin arc: left side  (210° → 330°)
    Glucose arc: right side (210° → 330°, mirrored via flip)
    """
    arc_r   = 95
    arc_start = 148  
    arc_end   = 212

    
    
    
    draw_arc(draw, CX, CY, arc_r, 328, 390+60, PURPLE_DIM, width=4)   
    fill_end = 328 + (60) * insulin_pct
    if insulin_pct > 0:
        draw_arc(draw, CX, CY, arc_r, 328, fill_end, PURPLE, width=4) 

    
    draw_arc(draw, CX, CY, arc_r, 150, 212, ACCENT_DIM, width=4)   
    fill_end_g = 150 + 62 * glucose_pct
    if glucose_pct > 0:
        draw_arc(draw, CX, CY, arc_r, 150, fill_end_g, ACCENT, width=4)


def centered_text(draw, text, cx, cy, font, color):
    """Draw text centered on (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=color)


def draw_complication(draw, cx, cy, label, value, unit, label_color, value_color, unit_color):
    """Render a 3-line complication: LABEL / value / unit."""
    
    lb = draw.textbbox((0, 0), label, font=font_label)
    lw = lb[2] - lb[0]
    draw.text((cx - lw // 2, cy - 18), label, font=font_label, fill=label_color)

    
    vb = draw.textbbox((0, 0), value, font=font_value)
    vw = vb[2] - vb[0]
    draw.text((cx - vw // 2, cy - 4), value, font=font_value, fill=value_color)

    
    ub = draw.textbbox((0, 0), unit, font=font_label)
    uw = ub[2] - ub[0]
    draw.text((cx - uw // 2, cy + 16), unit, font=font_label, fill=unit_color)






def get_data():
    return {
        "insulin": 120,      
        "insulin_max": 150,
        "glucose": 98,       
        "glucose_low": 70,
        "glucose_high": 180,
        "temp": 36.5,        
        "water_ago_h": 2,    
    }





while True:
    img  = Image.new("RGB", (W, H), BG_OUTER)
    draw = ImageDraw.Draw(img)

    data = get_data()

    
    insulin_pct = min(data["insulin"] / data["insulin_max"], 1.0)
    glucose_range = data["glucose_high"] - data["glucose_low"]
    glucose_pct   = min(max((data["glucose"] - data["glucose_low"]) / glucose_range, 0), 1.0)

    
    draw_circle_bg(draw)

    
    draw_bezel_ticks(draw)

    
    draw.ellipse(
        (CX - R, CY - R, CX + R, CY + R),
        outline=(25, 25, 50), width=1
    )

    
    draw_complication_arcs(draw, insulin_pct, glucose_pct)

    
    brand = "NEXUS"
    bb = draw.textbbox((0, 0), brand, font=font_brand)
    bw = bb[2] - bb[0]
    
    sx = CX - 14
    for ch in brand:
        draw.text((sx, CY - 46), ch, font=font_brand, fill=(0, 100, 65))
        sx += 6

    
    t_str = time.strftime("%H:%M")
    centered_text(draw, t_str, CX, CY - 5, font_time, WHITE)

    
    draw.line([(CX - 28, CY + 20), (CX + 28, CY + 20)], fill=GREY_DIM, width=1)

    
    date_str = time.strftime("%a %d").upper()
    centered_text(draw, date_str, CX, CY + 30, font_date, GREY_MID)

    
    
    draw_complication(draw,
        cx=72, cy=76,
        label="INSULIN",
        value=str(data["insulin"]),
        unit="UNITS",
        label_color=(80, 70, 200),
        value_color=(160, 155, 255),
        unit_color=(50, 45, 130),
    )

    
    draw_complication(draw,
        cx=168, cy=76,
        label="GLUCOSE",
        value=str(data["glucose"]),
        unit="MG/DL",
        label_color=(0, 140, 90),
        value_color=ACCENT,
        unit_color=(0, 80, 55),
    )

    
    temp_str = f"{data['temp']:.1f}"
    draw_complication(draw,
        cx=72, cy=166,
        label="TEMP",
        value=temp_str,
        unit="°C",
        label_color=(180, 90, 30),
        value_color=ORANGE,
        unit_color=(120, 55, 15),
    )

    
    water_str = f"{data['water_ago_h']}h"
    draw_complication(draw,
        cx=168, cy=166,
        label="WATER",
        value=water_str,
        unit="AGO",
        label_color=(30, 90, 180),
        value_color=BLUE,
        unit_color=(20, 55, 120),
    )

    
    draw.ellipse((CX-2, CY+7, CX+2, CY+11), fill=ACCENT)

    
    disp.ShowImage(img.rotate(180))
    time.sleep(1)
