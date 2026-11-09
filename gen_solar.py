#!/usr/bin/env python3
"""Generate an animated solar-system SVG (SMIL, self-contained)."""
import random

W = H = 1000
CX = CY = 500
random.seed(42)

PLANETS = [
    # name, orbit r, body r, dur(s), c1, c2, extra
    ("水星", 88, 4.5, 7, "#d8cec2", "#6d635a", None, 0.00),
    ("金星", 124, 7.5, 11, "#f7e3b0", "#c9932f", None, 0.22),
    ("地球", 164, 8.5, 15, "#6cb7f5", "#17498f", "earth", 0.41),
    ("火星", 204, 6.0, 21, "#e08a5a", "#8c3b24", None, 0.63),
    ("木星", 296, 18.0, 34, "#ecd0a8", "#a76f42", "jupiter", 0.17),
    ("土星", 360, 15.0, 48, "#ead9a8", "#b98f52", "saturn", 0.52),
    ("天王星", 424, 11.0, 66, "#b7ecec", "#4fa7a8", None, 0.78),
    ("海王星", 468, 10.5, 84, "#7f9fe8", "#2f4fae", None, 0.90),
]

parts = []
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <radialGradient id="bg" cx="50%" cy="46%" r="78%">
    <stop offset="0%" stop-color="#131a33"/>
    <stop offset="52%" stop-color="#0a0e1e"/>
    <stop offset="100%" stop-color="#02030a"/>
  </radialGradient>
  <radialGradient id="neb1" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#5a4bd0" stop-opacity="0.16"/>
    <stop offset="60%" stop-color="#3b2f9e" stop-opacity="0.07"/>
    <stop offset="100%" stop-color="#3b2f9e" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="neb2" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#2f8fae" stop-opacity="0.13"/>
    <stop offset="65%" stop-color="#1f5f7a" stop-opacity="0.05"/>
    <stop offset="100%" stop-color="#1f5f7a" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="sunCore" cx="50%" cy="42%" r="58%">
    <stop offset="0%" stop-color="#fffdf2"/>
    <stop offset="42%" stop-color="#ffe27a"/>
    <stop offset="75%" stop-color="#ffb03a"/>
    <stop offset="100%" stop-color="#ff8a1e"/>
  </radialGradient>
  <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#ffd66b" stop-opacity="0.50"/>
    <stop offset="42%" stop-color="#ffab3d" stop-opacity="0.16"/>
    <stop offset="100%" stop-color="#ffab3d" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx="50%" cy="50%" r="72%">
    <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="72%" stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.55"/>
  </radialGradient>
  <linearGradient id="cometTail" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
    <stop offset="30%" stop-color="#aee6ff" stop-opacity="0.55"/>
    <stop offset="100%" stop-color="#6fb8ff" stop-opacity="0"/>
  </linearGradient>
  <filter id="sunBlur" x="-120%" y="-120%" width="340%" height="340%">
    <feGaussianBlur stdDeviation="10"/>
  </filter>
  <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="2.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="earthClip"><circle r="8.5"/></clipPath>
  <clipPath id="jupClip"><circle r="18"/></clipPath>
''')

for name, orbit, r, dur, c1, c2, extra, phase in PLANETS:
    pid = {"水星": "mercury", "金星": "venus", "地球": "earth", "火星": "mars",
           "木星": "jupiter", "土星": "saturn", "天王星": "uranus", "海王星": "neptune"}[name]
    parts.append(f'''  <radialGradient id="{pid}G" cx="38%" cy="32%" r="72%">
    <stop offset="0%" stop-color="{c1}"/>
    <stop offset="100%" stop-color="{c2}"/>
  </radialGradient>
''')

parts.append('</defs>\n')

parts.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>\n')
parts.append('<ellipse cx="265" cy="235" rx="330" ry="250" fill="url(#neb1)"/>\n')
parts.append('<ellipse cx="760" cy="710" rx="360" ry="280" fill="url(#neb2)"/>\n')

# starfield
parts.append('<g id="stars">\n')
for _ in range(170):
    x = random.uniform(0, W)
    y = random.uniform(0, H)
    r = random.uniform(0.5, 1.6)
    base = random.uniform(0.25, 0.9)
    dur = random.uniform(2.2, 6.5)
    begin = -random.uniform(0, dur)
    color = random.choice(["#ffffff", "#dfe9ff", "#bcd2ff", "#fff4d6"])
    parts.append(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{color}" opacity="{base:.2f}">'
        f'<animate attributeName="opacity" values="{base:.2f};{min(1.0, base+0.5):.2f};{base:.2f}" '
        f'dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></circle>\n'
    )
parts.append('</g>\n')

# orbit rings
parts.append('<g id="orbits" fill="none" stroke="#8fb3e0" stroke-opacity="0.30" stroke-width="1" stroke-dasharray="1 7" stroke-linecap="round">\n')
for name, orbit, r, dur, c1, c2, extra, phase in PLANETS:
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="{orbit}"/>\n')
parts.append('</g>\n')

# asteroid belt
parts.append('<g id="belt" transform="translate(500 500)">\n')
parts.append('<animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="120s" repeatCount="indefinite" additive="replace"/>\n')
for _ in range(110):
    ang = random.uniform(0, 6.28318)
    rad = random.uniform(228, 258)
    import math
    x = rad * math.cos(ang)
    y = rad * math.sin(ang)
    rr = random.uniform(0.6, 1.4)
    op = random.uniform(0.25, 0.7)
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.2f}" fill="#a89f8d" opacity="{op:.2f}"/>\n')
parts.append('</g>\n')

# planets
for name, orbit, r, dur, c1, c2, extra, phase in PLANETS:
    pid = {"水星": "mercury", "金星": "venus", "地球": "earth", "火星": "mars",
           "木星": "jupiter", "土星": "saturn", "天王星": "uranus", "海王星": "neptune"}[name]
    parts.append(f'''<g transform="translate({CX} {CY})">
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="{dur}s" begin="-{dur*phase:.1f}s" repeatCount="indefinite"/>
    <g transform="translate({orbit} 0)">
''')
    if extra == "saturn":
        parts.append(f'''      <g transform="rotate(-18)">
        <ellipse rx="{r*1.75:.1f}" ry="{r*0.42:.1f}" fill="none" stroke="#d9c48c" stroke-opacity="0.75" stroke-width="2.2"/>
        <ellipse rx="{r*1.45:.1f}" ry="{r*0.32:.1f}" fill="none" stroke="#b99a5e" stroke-opacity="0.55" stroke-width="1.2"/>
      </g>
''')
    parts.append(f'      <circle r="{r}" fill="url(#{pid}G)"/>\n')
    if extra == "earth":
        parts.append(f'''      <g clip-path="url(#earthClip)" opacity="0.85">
        <path d="M -6 -6 q 4 -2 6 1 q 2 3 -1 5 q -4 2 -5 -1 z" fill="#57a85f"/>
        <path d="M 2 2 q 4 -1 5 2 q 1 4 -3 4 q -3 0 -2 -6 z" fill="#4b9455"/>
      </g>
      <circle r="{r+1.2:.1f}" fill="none" stroke="#8fd0ff" stroke-opacity="0.35" stroke-width="1"/>
''')
    if extra == "jupiter":
        parts.append(f'''      <g clip-path="url(#jupClip)" opacity="0.65">
        <path d="M -20 -8 q 20 4 40 0 l 0 3 q -20 4 -40 0 z" fill="#b07a4c"/>
        <path d="M -20 2 q 20 3 40 0 l 0 2.6 q -20 4 -40 0 z" fill="#8d5a34"/>
        <path d="M -20 9 q 20 2 40 0 l 0 2 q -20 3 -40 0 z" fill="#c78e57"/>
        <ellipse cx="6" cy="4" rx="4" ry="2.4" fill="#d8a06a" opacity="0.9"/>
      </g>
''')
    parts.append(f'''      <g>
        <animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="{dur}s" begin="-{dur*phase:.1f}s" repeatCount="indefinite"/>
        <text y="{r+15:.1f}" text-anchor="middle" font-family="'Droid Sans Fallback','Noto Sans CJK SC',sans-serif" font-size="10.5" fill="#94a8cf" letter-spacing="2" opacity="0.9">{name}</text>
      </g>
    </g>
  </g>
</g>
''')

# sun
parts.append(f'''<g id="sun">
  <circle cx="{CX}" cy="{CY}" r="118" fill="url(#sunGlow)">
    <animate attributeName="r" values="112;124;112" dur="6s" repeatCount="indefinite"/>
  </circle>
  <g opacity="0.55">
    <animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" dur="80s" repeatCount="indefinite"/>
''')
import math
for k in range(28):
    ang = k * (360 / 28)
    ln = 8 + (k % 3) * 3
    rad = 46
    x1 = CX + rad * math.cos(math.radians(ang))
    y1 = CY + rad * math.sin(math.radians(ang))
    x2 = CX + (rad + ln) * math.cos(math.radians(ang))
    y2 = CY + (rad + ln) * math.sin(math.radians(ang))
    parts.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ffcf6e" stroke-width="1.2" stroke-linecap="round"/>\n')
parts.append('''  </g>
  <circle cx="500" cy="500" r="58" fill="#ffb03a" opacity="0.35" filter="url(#sunBlur)">
    <animate attributeName="opacity" values="0.28;0.45;0.28" dur="5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="500" cy="500" r="40" fill="url(#sunCore)" filter="url(#softGlow)">
    <animate attributeName="r" values="39.4;40.8;39.4" dur="5s" repeatCount="indefinite"/>
  </circle>
</g>
''')

# comet
parts.append('''<g id="comet">
  <animateMotion dur="26s" repeatCount="indefinite" rotate="auto"
      path="M 1120 110 Q 520 -40 -90 290"/>
  <g opacity="0">
    <animate attributeName="opacity" values="0;0.95;0.95;0" keyTimes="0;0.08;0.86;1" dur="26s" repeatCount="indefinite"/>
    <path d="M 0 0 Q -40 -3 -110 -1.5 Q -55 2.2 0 0 Z" fill="url(#cometTail)"/>
    <circle r="3" fill="#ffffff" filter="url(#softGlow)"/>
  </g>
</g>
''')

parts.append(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>\n')
parts.append(f'''<text x="{CX}" y="{H-34}" text-anchor="middle" font-family="'Droid Sans Fallback','Noto Sans CJK SC',sans-serif" font-size="12" fill="#5f6f96" letter-spacing="7" opacity="0.85">S O L A R&#160;&#160;S Y S T E M</text>
</svg>
''')

svg = "".join(parts)
with open("/data/agent-memory/solar_system.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("written", len(svg), "bytes")
