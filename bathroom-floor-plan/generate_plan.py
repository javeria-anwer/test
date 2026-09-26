"""Generates the 66" x 66" bathroom renovation floor plan as SVG.

All geometry is in inches (interior clear room = 66 x 66) and scaled to px.
Run: python3 generate_plan.py  -> writes bathroom_floor_plan.svg
"""
import math

S = 8.0            # px per inch
OX, OY = 150, 230  # px position of interior top-left corner
EXT = 4.5          # existing outer wall thickness (drawn outside the 66" room)
PART = 4.0         # new partition thickness
ROOM = 66.0

# Toilet enclosure (clear inside): x 0..30, full depth to the south wall
TW, TD = 30.0, 66.0
# Toilet door opening in vertical partition (x 30..34)
TDOOR_Y0, TDOOR_Y1 = 26.0, 48.0          # 22" opening
TLEAF = 21.0
# External step (washroom side)
STEP_X0, STEP_X1 = TW + PART, TW + PART + 10.0   # 10" tread
# Washbasin (wall hung, north wall)
BAS_X0, BAS_X1, BAS_D = 45.0, 63.0, 15.0
# Entrance door opening in south wall
EDOOR_X0, EDOOR_X1 = 38.0, 64.0          # 26" opening
ELEAF = 25.0

def X(v): return OX + v * S
def Y(v): return OY + v * S
def L(v): return v * S

out = []
def add(s): out.append(s)

def rect(x0, y0, x1, y1, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    add(f'<rect x="{X(x0):.1f}" y="{Y(y0):.1f}" width="{L(x1-x0):.1f}" height="{L(y1-y0):.1f}" {attrs}/>')

def line(x0, y0, x1, y1, **kw):
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    add(f'<line x1="{X(x0):.1f}" y1="{Y(y0):.1f}" x2="{X(x1):.1f}" y2="{Y(y1):.1f}" {attrs}/>')

def text(x, y, s, size=13, weight="normal", anchor="middle", fill="#1f2a44", raw=False, rotate=None, style=""):
    px, py = (x, y) if raw else (X(x), Y(y))
    rot = f' transform="rotate({rotate} {px:.1f} {py:.1f})"' if rotate else ""
    add(f'<text x="{px:.1f}" y="{py:.1f}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}"{rot} style="{style}">{s}</text>')

def dim_h(x0, x1, y, label, off_label=-6, size=12, ext_from=None):
    """Horizontal dimension line at plan-y `y` (inches)."""
    line(x0, y, x1, y, stroke="#1f2a44", stroke_width=1)
    for xx in (x0, x1):
        add(f'<line x1="{X(xx)-4:.1f}" y1="{Y(y)+4:.1f}" x2="{X(xx)+4:.1f}" y2="{Y(y)-4:.1f}" stroke="#1f2a44" stroke-width="1.4"/>')
        if ext_from is not None:
            line(xx, ext_from, xx, y + (1 if y > ext_from else -1), stroke="#8a93a6", stroke_width=0.7, stroke_dasharray="3 2")
    text((x0 + x1) / 2, y + off_label / S, label, size=size)

def dim_v(y0, y1, x, label, size=12, ext_from=None, side=-1):
    line(x, y0, x, y1, stroke="#1f2a44", stroke_width=1)
    for yy in (y0, y1):
        add(f'<line x1="{X(x)-4:.1f}" y1="{Y(yy)+4:.1f}" x2="{X(x)+4:.1f}" y2="{Y(yy)-4:.1f}" stroke="#1f2a44" stroke-width="1.4"/>')
        if ext_from is not None:
            line(ext_from, yy, x + (1 if x > ext_from else -1), yy, stroke="#8a93a6", stroke_width=0.7, stroke_dasharray="3 2")
    cx, cy = X(x) + side * 7, Y((y0 + y1) / 2)
    text(cx, cy, label, size=size, raw=True, rotate=-90)

W, H = 1460, 1060
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="Segoe UI, Helvetica, Arial, sans-serif">')
add('''<defs>
  <pattern id="raised" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="10" height="10" fill="#efe4cf"/>
    <line x1="0" y1="0" x2="0" y2="10" stroke="#c9b48a" stroke-width="1.2"/>
  </pattern>
  <pattern id="partition" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="6" height="6" fill="#6b6f78"/>
    <line x1="0" y1="0" x2="0" y2="6" stroke="#3a3d44" stroke-width="1.5"/>
  </pattern>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#b5541c"/>
  </marker>
</defs>''')
add(f'<rect width="{W}" height="{H}" fill="#fbfbf9"/>')

# Title
text(40, 44, "BATHROOM RENOVATION — PROPOSED FLOOR PLAN", size=24, weight="700", anchor="start", raw=True)
text(40, 70, 'Interior clear size 66" × 66" (5\'-6" × 5\'-6")  ·  Scale approx. 1" = 8 px  ·  All dimensions in inches, approximate — verify on site',
     size=13, anchor="start", raw=True, fill="#4a5470")

# ---------- floors ----------
rect(0, 0, ROOM, ROOM, fill="#e9e7e1")                      # washroom floor
# 12" tile grid in washroom
for i in range(1, 6):
    v = i * 12
    line(v, 0, v, ROOM, stroke="#d6d3cb", stroke_width=0.8)
    line(0, v, ROOM, v, stroke="#d6d3cb", stroke_width=0.8)
# raised toilet platform (+14")
rect(0, 0, TW, TD, fill="url(#raised)")
add(f'<rect x="{X(0):.1f}" y="{Y(0):.1f}" width="{L(TW):.1f}" height="{L(TD):.1f}" fill="none" '
    f'stroke="#9c7b3c" stroke-width="1.5" stroke-dasharray="7 4"/>')

# ---------- existing outer walls ----------
wall = dict(fill="#2c2f36")
rect(-EXT, -EXT, ROOM + EXT, 0, **wall)                      # north
rect(-EXT, 0, 0, ROOM + EXT, **wall)                         # west
rect(ROOM, 0, ROOM + EXT, ROOM + EXT, **wall)                # east
rect(-EXT, ROOM, EDOOR_X0, ROOM + EXT, **wall)               # south, left of door
rect(EDOOR_X1, ROOM, ROOM, ROOM + EXT, **wall)               # south, right of door

# ---------- new partition walls ----------
pw = dict(fill="url(#partition)", stroke="#2c2f36", stroke_width=1)
rect(TW, 0, TW + PART, TDOOR_Y0, **pw)                       # vertical, above toilet door
rect(TW, TDOOR_Y1, TW + PART, ROOM, **pw)                    # vertical, below toilet door to south wall
# raised threshold inside the toilet door opening (+14")
rect(TW, TDOOR_Y0, TW + PART, TDOOR_Y1, fill="url(#raised)", stroke="#9c7b3c", stroke_width=1)

# ---------- steps ----------
rect(STEP_X0, TDOOR_Y0, STEP_X1, TDOOR_Y1, fill="#d9c7a3", stroke="#6e5626", stroke_width=1.6)
# nosing line + riser line
line(STEP_X1 - 1, TDOOR_Y0, STEP_X1 - 1, TDOOR_Y1, stroke="#6e5626", stroke_width=0.8, stroke_dasharray="3 2")
line(STEP_X0 + 0.3, TDOOR_Y0, STEP_X0 + 0.3, TDOOR_Y1, stroke="#6e5626", stroke_width=2)
# UP arrow from washroom floor, across the step, into the toilet
add(f'<line x1="{X(STEP_X1 + 6):.1f}" y1="{Y(40):.1f}" x2="{X(TW - 4):.1f}" y2="{Y(40):.1f}" '
    f'stroke="#b5541c" stroke-width="2" marker-end="url(#arrow)"/>')
add(f'<circle cx="{X(STEP_X1 + 6):.1f}" cy="{Y(40):.1f}" r="3.5" fill="#b5541c"/>')
text(STEP_X1 + 3.5, 39.0, "UP", size=11, weight="700", fill="#b5541c", anchor="start")
text((STEP_X0 + STEP_X1) / 2, 30.2, "STEP 1", size=10.5, weight="700", fill="#4a3a17")
text((STEP_X0 + STEP_X1) / 2, 32.2, '+7"', size=10.5, fill="#4a3a17")
text(TW + PART / 2, 30.5, "2", size=10.5, weight="700", fill="#4a3a17")

# ---------- toilet door (opens INTO the raised toilet, away from the steps) ----------
hx, hy = TW, TDOOR_Y1 - 0.75
# door leaf in open position (stands clear of the bowl)
rect(hx - TLEAF, hy - 1.4, hx, hy, fill="#c8894a", stroke="#6e4a22", stroke_width=1)
# swing arc from closed (vertical, in the opening) to open
add(f'<path d="M {X(hx):.1f} {Y(hy - TLEAF):.1f} A {L(TLEAF):.1f} {L(TLEAF):.1f} 0 0 0 {X(hx - TLEAF):.1f} {Y(hy):.1f}" '
    f'fill="none" stroke="#6e4a22" stroke-width="1" stroke-dasharray="5 4"/>')
add(f'<circle cx="{X(hx):.1f}" cy="{Y(hy):.1f}" r="4" fill="#2c2f36"/>')   # hinge

# ---------- commode (compact, wall-to-front ~26") ----------
cx = TW / 2
rect(cx - 8, 0.4, cx + 8, 7.4, fill="#ffffff", stroke="#5c6270", stroke_width=1.3, rx=5)       # cistern 16" x 7"
add(f'<circle cx="{X(cx):.1f}" cy="{Y(3.9):.1f}" r="5" fill="none" stroke="#5c6270"/>')          # flush button
add(f'<ellipse cx="{X(cx):.1f}" cy="{Y(16.9):.1f}" rx="{L(7.25):.1f}" ry="{L(9.1):.1f}" fill="#ffffff" stroke="#5c6270" stroke-width="1.3"/>')
add(f'<ellipse cx="{X(cx):.1f}" cy="{Y(17.6):.1f}" rx="{L(5.0):.1f}" ry="{L(6.6):.1f}" fill="#f1f3f6" stroke="#8b92a1" stroke-width="1"/>')
# seated zone in front of commode
rect(cx - 10, 26, cx + 10, 45.3, fill="none", stroke="#3d7a57", stroke_width=1, stroke_dasharray="4 3")

# ---------- washbasin (wall hung, 18" wide) ----------
rect(BAS_X0, 0, BAS_X1, BAS_D, fill="#ffffff", stroke="#5c6270", stroke_width=1.4, rx=10)
add(f'<ellipse cx="{X((BAS_X0 + BAS_X1)/2):.1f}" cy="{Y(8.6):.1f}" rx="{L(6.6):.1f}" ry="{L(4.8):.1f}" fill="#eef1f5" stroke="#8b92a1"/>')
add(f'<circle cx="{X((BAS_X0 + BAS_X1)/2):.1f}" cy="{Y(9.3):.1f}" r="3" fill="#8b92a1"/>')
rect((BAS_X0 + BAS_X1)/2 - 0.6, 0.6, (BAS_X0 + BAS_X1)/2 + 0.6, 4.2, fill="#9aa1ae")                 # tap
# user standing zone in front of basin
rect(BAS_X0 - 1, BAS_D, BAS_X1 + 1, BAS_D + 18, fill="none", stroke="#3d7a57", stroke_width=1, stroke_dasharray="4 3")

# ---------- entrance door (opens inward, leaf parks against east wall) ----------
ex, ey = EDOOR_X1 - 0.5, ROOM
rect(ex - 1.4, ey - ELEAF, ex, ey, fill="#c8894a", stroke="#6e4a22", stroke_width=1)
add(f'<path d="M {X(ex - ELEAF):.1f} {Y(ey):.1f} A {L(ELEAF):.1f} {L(ELEAF):.1f} 0 0 1 {X(ex):.1f} {Y(ey - ELEAF):.1f}" '
    f'fill="none" stroke="#6e4a22" stroke-width="1" stroke-dasharray="5 4"/>')
add(f'<circle cx="{X(ex):.1f}" cy="{Y(ey):.1f}" r="4" fill="#2c2f36"/>')
# door frame jambs
rect(EDOOR_X0, ROOM, EDOOR_X0 + 0.8, ROOM + EXT, fill="#c8894a")
rect(EDOOR_X1 - 0.8, ROOM, EDOOR_X1, ROOM + EXT, fill="#c8894a")

# ---------- floor trap (under the wall-hung basin) + towel rail on partition ----------
TRX, TRY = (BAS_X0 + BAS_X1) / 2, 13.9
add(f'<rect x="{X(TRX)-7:.1f}" y="{Y(TRY)-7:.1f}" width="14" height="14" fill="#c4c8cf" fill-opacity="0.6" stroke="#5c6270" stroke-dasharray="3 2"/>')
for d in (-3, 0, 3):
    add(f'<line x1="{X(TRX)-5:.1f}" y1="{Y(TRY)+d:.1f}" x2="{X(TRX)+5:.1f}" y2="{Y(TRY)+d:.1f}" stroke="#5c6270" stroke-width="0.8"/>')
rect(TW + PART - 0.2, 57, TW + PART + 1.4, 65, fill="#b9bec7", stroke="#5c6270", stroke_width=0.8)   # towel rail

# ---------- labels ----------
text(15, 34.0, "TOILET", size=15, weight="700")
text(15, 36.3, "(raised floor +14\")", size=10.5, fill="#6e5626")
text(15, 38.6, "access only from washroom", size=10, fill="#4a5470")
text(15, 10.6, "COMMODE", size=10.5, weight="700", fill="#1f2a44")
text(15, 44.3, "seated zone", size=9.5, fill="#3d7a57")
text(54, 20.6, "WASHBASIN", size=11.5, weight="700")
text(54, 22.6, 'wall-hung', size=10, fill="#4a5470")
text(55, 29.0, "WASHROOM", size=15, weight="700")
text(55, 31.3, "floor ±0", size=10.5, fill="#4a5470")
text(54, 24.4, "floor trap below basin", size=9.5, fill="#4a5470")
text(TW + PART + 3.2, 61, "towel rail", size=9.5, fill="#4a5470", rotate=-90)

# steps label with leader
add(f'<line x1="{X(39):.1f}" y1="{Y(48):.1f}" x2="{X(44):.1f}" y2="{Y(53.3):.1f}" stroke="#b5541c" stroke-width="1.2"/>')
add(f'<rect x="{X(38.5):.1f}" y="{Y(53.3):.1f}" width="{L(16.8):.1f}" height="{L(3.2):.1f}" fill="#fff4ea" stroke="#b5541c" rx="3"/>')
text(46.9, 55.5, "STEPS TO TOILET", size=10.5, weight="700", fill="#b5541c")

# clear walking space
add(f'<line x1="{X(STEP_X1):.1f}" y1="{Y(36):.1f}" x2="{X(ROOM):.1f}" y2="{Y(36):.1f}" stroke="#3d7a57" stroke-width="1.2" '
    f'marker-start="url(#arrow)" marker-end="url(#arrow)" style="color:#3d7a57"/>')
text((STEP_X1 + ROOM) / 2, 35.1, '22" CLEAR', size=10.5, weight="700", fill="#3d7a57")

# entrance
add(f'<path d="M {X(51)-14:.1f} {Y(ROOM+EXT)+80:.1f} L {X(51):.1f} {Y(ROOM+EXT)+62:.1f} L {X(51)+14:.1f} {Y(ROOM+EXT)+80:.1f} z" fill="#1f2a44"/>')
text(51, ROOM + EXT + 12.3, "ENTRANCE", size=15, weight="700")
text(51, ROOM + EXT + 14.4, "single door into washroom", size=10.5, fill="#4a5470")

# ---------- dimensions ----------
# top chain: 30 | 4 | 32  and overall 66
dim_h(0, TW, -9, '30" toilet (clear)', ext_from=-EXT)
dim_h(TW, TW + PART, -9, '4"', size=10)
dim_h(TW + PART, ROOM, -9, '32" washroom', ext_from=-EXT)
dim_h(0, ROOM, -16, '66" (5\'-6") INTERIOR CLEAR', size=13)
# basin width
dim_h(BAS_X0, BAS_X1, 17.0, '18"', size=10.5, off_label=-4)
# left chain: 48 | 4 | 14
dim_v(0, TD, -9, '66" toilet depth (full)', ext_from=-EXT)
dim_v(0, ROOM, -16, '66" (5\'-6") INTERIOR CLEAR', size=13)
# right chain: toilet door + step location
dim_v(0, BAS_D, ROOM + 9, '15"', size=10.5, ext_from=ROOM + EXT, side=1)
dim_v(TDOOR_Y0, TDOOR_Y1, ROOM + 9, '22" toilet door', size=10.5, ext_from=ROOM + EXT, side=1)
dim_v(0, ROOM, ROOM + 16, '66" (5\'-6")', size=13, side=1)
# bottom chain: 38 | 26 | 2
dim_h(0, EDOOR_X0, ROOM + 9, '38"', size=10.5, off_label=-4)
dim_h(EDOOR_X0, EDOOR_X1, ROOM + 9, '26" entrance door', size=10.5, off_label=-4)
# step tread dimension
dim_h(STEP_X0, STEP_X1, 24.0 - 0.5, "", size=9)
text((STEP_X0 + STEP_X1) / 2, 22.6, '10"', size=10)

# ---------- north arrow ----------
nx, ny = 700, 930
add(f'<path d="M {nx} {ny-34} L {nx+13} {ny+8} L {nx} {ny} L {nx-13} {ny+8} z" fill="#1f2a44"/>')
text(nx, ny + 28, "N", size=16, weight="700", raw=True)

# ---------- right panel ----------
PX, PY, PW = 850, 110, 580
add(f'<rect x="{PX}" y="{PY}" width="{PW}" height="560" fill="#ffffff" stroke="#c9cdd6" rx="6"/>')
yy = PY + 34
def ptxt(s, size=12.5, weight="normal", fill="#1f2a44", dy=20, indent=0):
    global yy
    text(PX + 22 + indent, yy, s, size=size, weight=weight, fill=fill, anchor="start", raw=True)
    yy += dy
ptxt("KEY DIMENSIONS (approx.)", size=15, weight="700", dy=26)
rows = [
    ("Overall bathroom (interior clear)", '66" × 66"  (5\'-6" × 5\'-6")'),
    ("Toilet enclosure (clear, raised)", '30" W × 66" D (full depth)'),
    ("New partition wall", '4" thick (block + plaster)'),
    ("Toilet door", '22" opening, 21" leaf, opens inward'),
    ("Main entrance door", '26" opening, opens inward'),
    ("Washbasin (wall-hung)", '18" W × 15" proj., floor trap below'),
    ("Compact commode", '15" W × 26" D (wall to bowl front)'),
    ("Steps to toilet", '2 risers × 7" = +14"; tread 10" × 22"'),
    ("Clear walk beside step", '22" min.'),
    ("Clear in front of commode", '40" to south wall (≈20" to open door)'),
    ("Clear floor in front of basin", '51" deep (basin front to entrance)'),
]
for k, v in rows:
    text(PX + 22, yy, k, size=12.5, anchor="start", raw=True, fill="#4a5470")
    text(PX + 285, yy, v, size=12.5, anchor="start", raw=True, weight="600")
    yy += 21
yy += 10
add(f'<line x1="{PX+20}" y1="{yy-12}" x2="{PX+PW-20}" y2="{yy-12}" stroke="#e1e4ea"/>')
ptxt("DESIGN NOTES", size=15, weight="700", dy=24)
notes = [
    "Old Asian/squatting WC removed; one compact floor-mounted commode.",
    "Existing raised toilet floor retained (+14\" approx. — match site level).",
    "Solid 4\" partition; toilet has NO external door — entered only from",
    "   inside the washroom through the door on its RIGHT side.",
    "Step 1 (+7\") sits in the washroom; step 2 (+14\") is the raised",
    "   threshold in the partition, level with the toilet floor.",
    "Toilet door swings INTO the raised toilet so it never sweeps the steps;",
    "   open leaf stands clear of the bowl; enclosure runs to the south wall.",
    "Washbasin on the top (north) wall, in line of sight from entrance.",
    "Entrance door leaf parks against the east wall, clearing step 1 by ~1\".",
]
for n in notes:
    ptxt(n, size=12, fill="#2f3850", dy=19)

# ---------- step section inset ----------
SX, SY = 850, 700
add(f'<rect x="{SX}" y="{SY}" width="{PW}" height="330" fill="#ffffff" stroke="#c9cdd6" rx="6"/>')
text(SX + 22, SY + 30, "SECTION A–A THROUGH STEPS (looking north)", size=15, weight="700", anchor="start", raw=True)
k = 6.0   # px per inch in section
base_y = SY + 280
x_room_r = SX + 540    # east wall face of washroom (x=66) on the right
def sx(v): return x_room_r - (ROOM - v) * k
# floor line washroom
add(f'<line x1="{sx(STEP_X1):.1f}" y1="{base_y}" x2="{sx(ROOM):.1f}" y2="{base_y}" stroke="#2c2f36" stroke-width="2"/>')
# solids: step 1, threshold, toilet platform
pts = [
    (sx(ROOM), base_y), (sx(STEP_X1), base_y), (sx(STEP_X1), base_y - 7*k),
    (sx(STEP_X0), base_y - 7*k), (sx(STEP_X0), base_y - 14*k),
    (sx(0), base_y - 14*k), (sx(0), base_y + 12), (sx(ROOM), base_y + 12)
]
add('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '" fill="#d9c7a3" stroke="#6e5626" stroke-width="1.5"/>')
# partition above threshold (door head) and outer walls
add(f'<rect x="{sx(TW):.1f}" y="{base_y - 14*k - 95}" width="{PART*k:.1f}" height="18" fill="url(#partition)" stroke="#2c2f36"/>')
add(f'<rect x="{sx(0) - EXT*k:.1f}" y="{SY + 45}" width="{EXT*k:.1f}" height="{base_y + 12 - SY - 45:.1f}" fill="#2c2f36"/>')
add(f'<rect x="{sx(ROOM):.1f}" y="{SY + 45}" width="{EXT*k:.1f}" height="{base_y + 12 - SY - 45:.1f}" fill="#2c2f36"/>')
# door leaf (open, inside toilet) hint
add(f'<line x1="{sx(TW):.1f}" y1="{base_y - 14*k - 77}" x2="{sx(TW):.1f}" y2="{base_y - 14*k}" stroke="#c8894a" stroke-width="1" stroke-dasharray="4 3"/>')
text(sx(TW) - 6, base_y - 14*k - 45, "toilet door", size=10, anchor="end", raw=True, fill="#6e4a22")
# commode silhouette
cxs = sx(0)
add(f'<rect x="{cxs + 2:.1f}" y="{base_y - 14*k - 75}" width="{7*k:.1f}" height="44" fill="#fff" stroke="#5c6270" rx="3"/>')
add(f'<path d="M {cxs + 2:.1f} {base_y - 14*k - 31} L {cxs + 26*k:.1f} {base_y - 14*k - 31} Q {cxs + 26*k:.1f} {base_y - 14*k - 10} {cxs + 18*k:.1f} {base_y - 14*k - 6} '
    f'L {cxs + 14*k:.1f} {base_y - 14*k} L {cxs + 6*k:.1f} {base_y - 14*k} L {cxs + 2:.1f} {base_y - 14*k - 31} z" fill="#fff" stroke="#5c6270"/>')
# labels
text(sx(15), base_y - 14*k + 24, "TOILET FLOOR +14\"", size=11, weight="700", raw=True, fill="#4a3a17")
text(sx((STEP_X0 + STEP_X1)/2), base_y - 7*k + 16, "STEP 1", size=10.5, weight="700", raw=True, fill="#4a3a17")
text(sx(TW + PART/2), base_y - 14*k + 16, "2", size=10.5, weight="700", raw=True, fill="#4a3a17")
text(sx(56), base_y - 10, "WASHROOM ±0", size=11, weight="700", raw=True, fill="#1f2a44")
# riser dims (just in front of each riser)
for (y0, y1, xr) in ((0, 7, STEP_X1), (7, 14, STEP_X0)):
    xx = sx(xr) + 9
    add(f'<line x1="{xx:.1f}" y1="{base_y - y0*k:.1f}" x2="{xx:.1f}" y2="{base_y - y1*k:.1f}" stroke="#b5541c" stroke-width="1"/>')
    for yv in (y0, y1):
        add(f'<line x1="{xx-4:.1f}" y1="{base_y - yv*k:.1f}" x2="{xx+4:.1f}" y2="{base_y - yv*k:.1f}" stroke="#b5541c" stroke-width="1"/>')
    text(xx + 6, base_y - (y0 + y1) / 2 * k + 4, '7"', size=10.5, anchor="start", raw=True, fill="#b5541c", weight="700")
text(sx(ROOM) - 8, SY + 62, 'Riser 7" · tread 10" · width 22"', size=11, anchor="end", raw=True, fill="#4a5470")
text(sx(ROOM) - 8, SY + 78, "Non-slip tile on treads; grab handle on door jamb advised", size=11, anchor="end", raw=True, fill="#4a5470")

# legend
LX, LY = 40, 1000
items = [("#2c2f36", "Existing wall", None), ("url(#partition)", 'New 4" partition', None),
         ("url(#raised)", "Raised toilet floor (+14\")", None), ("#d9c7a3", "Step 1 (+7\")", None)]
for i, (f, lab, _) in enumerate(items):
    x0 = LX + i * 180
    add(f'<rect x="{x0}" y="{LY}" width="22" height="14" fill="{f}" stroke="#2c2f36" stroke-width="0.8"/>')
    text(x0 + 30, LY + 12, lab, size=11.5, anchor="start", raw=True, fill="#2f3850")
add(f'<rect x="{LX}" y="{LY + 26}" width="22" height="14" fill="none" stroke="#3d7a57" stroke-dasharray="4 3"/>')
text(LX + 30, LY + 38, "Clear use zone", size=11.5, anchor="start", raw=True, fill="#2f3850")
add(f'<path d="M {LX+180} {LY+40} A 16 16 0 0 1 {LX+196} {LY+24}" fill="none" stroke="#6e4a22" stroke-dasharray="4 3"/>')
add(f'<circle cx="{LX+196}" cy="{LY+40}" r="3.5" fill="#2c2f36"/>')
text(LX + 210, LY + 38, "Door swing / hinge", size=11.5, anchor="start", raw=True, fill="#2f3850")

add('</svg>')

with open("bathroom_floor_plan.svg", "w") as f:
    f.write("\n".join(out))
print("wrote bathroom_floor_plan.svg")
