{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Ven\uc0\u817 p\u257  Meter Visualiser  \'96  Tamil n\u275 r / nirai\
# (c) 2025  Svetlana Kreuzer\
\
import streamlit as st\
import matplotlib.pyplot as plt\
from matplotlib.patches import Rectangle, Patch\
import re, unicodedata\
from typing import List\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  1.  Tamil basics \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
KURIL  = '\uc0\u2949 \u2951 \u2953 \u2958 \u2962 '                    # 1 m\u257 trai\
NEDIL  = '\uc0\u2950 \u2952 \u2954 \u2959 \u2963 \u2964 '                  # 2 m\u257 trai\
PULLI  = '\uc0\u3021 '                         # vir\u257 ma sign\
V_INV  = '\uc0\u3016 \u3018 \u3019 \u3019 \u3031 '                   # \'93ai\'94, \'93o\'94, \'93\u333 \'94, etc. (nedil)\
\
def is_vowel(ch):     return ch in KURIL + NEDIL\
def is_kuril(ch):     return ch in KURIL\
def is_nedil(ch):     return ch in NEDIL + V_INV\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  2.  very small tokenizer \u8594  ak\u7779 aram list \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def split_tamil(text: str) -> List[str]:\
    """Crude ak\uc0\u7779 aram splitter (enough for Ven\u817 p\u257 )."""\
    s = unicodedata.normalize('NFC', text.strip())\
    out, buf = [], ''\
    for ch in s:\
        if ch == ' ':\
            if buf: out.append(buf); buf = ''\
            continue\
        buf += ch\
        if is_vowel(ch) or ch == PULLI:\
            out.append(buf); buf = ''\
    if buf: out.append(buf)\
    return out\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  3.  n\u275 r / nirai test (m\u257 trai count) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def is_heavy(ak\uc0\u7779 : str) -> bool:\
    """nirai = 2 m\uc0\u257 trai; n\u275 r = 1 m\u257 trai."""\
    core = ak\uc0\u7779 [-1]                 # last code-point \u10132  vowel or pulli\
    if core == PULLI:              # consonant-ending => heavy\
        return True\
    if is_nedil(core):             # long vowel \uc0\u8658  heavy\
        return True\
    return False                   # short open syllable = light (n\uc0\u275 r)\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  4.  Ven\u817 p\u257  templates  (seer counts per a\u7789 i) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
VENPA_SHAPES = \{\
    (4, 4, 3, 4): 'CI\uc0\u7774 _VEN\u817 P\u256  (4-4-3-4)',      # common ven\u817 p\u257 \
    (4, 4, 4, 4): 'KALIPPA (4-4-4-4)',\
    (3, 4, 3, 4): 'VIRUTTAPA (3-4-3-4)',\
    (3, 4, 4, 4): 'P\uc0\u256  VEN\u817 P\u256  (3-4-4-4)'\
\}\
\
def seer_count(a\uc0\u7789 i: List[str]) -> int:\
    """Tamil seer = count of n\uc0\u275 r + nirai (each nirai = 2 m\u257 trai)."""\
    return sum(2 if is_heavy(s) else 1 for s in a\uc0\u7789 i)\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  5.  draw grid \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
def draw(lines: List[List[str]]):\
    rows, cols = len(lines), max(len(r) for r in lines)\
    fig, ax = plt.subplots(figsize=(cols*0.45, rows*0.45))\
    ax.set(xlim=(0, cols), ylim=(0, rows)); ax.axis('off'); ax.set_aspect('equal')\
\
    # cells + Tamil glyph\
    for r, row in enumerate(lines):\
        y = rows-1-r\
        for c, ak in enumerate(row):\
            heavy = is_heavy(ak)\
            ax.add_patch(Rectangle((c,y),1,1,\
                         facecolor='black' if heavy else 'white',\
                         edgecolor='gray', zorder=1))\
            ax.text(c+0.5, y+0.5, ak, fontsize=12,\
                    color='white' if heavy else 'black',\
                    ha='center', va='center', zorder=2)\
\
    # seer-count and pattern fill\
    counts = tuple(seer_count(r) for r in lines)\
    label  = VENPA_SHAPES.get(counts)\
    if label:\
        # fill first seer (first ak\uc0\u7779 aram) of every a\u7789 i\
        for r,row in enumerate(lines):\
            y = rows-1-r\
            ax.add_patch(Rectangle((0,y),1,1,\
                         facecolor='#FFB347', alpha=0.45, zorder=3))\
        ax.set_title(label, fontsize=11)\
\
    st.pyplot(fig); plt.close(fig)\
\
# \uc0\u9472 \u9472 \u9472 \u9472 \u9472  6.  Streamlit UI \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
st.set_page_config(page_title='Ven\uc0\u817 p\u257  Meter', layout='wide')\
st.title('Tamil Ven\uc0\u817 p\u257  Visualizer')\
\
st.markdown(\
    '*Paste Tamil Ven\uc0\u817 p\u257  (one **a\u7789 i** / line). '\
    'Black = nirai (heavy), white = n\uc0\u275 r (light). '\
    'Pattern highlight appears for 4-4-3-4 etc.*'\
)\
\
txt = st.text_area('Tamil input:', height=200)\
if st.button('Show'):\
    atis = [l.strip() for l in txt.splitlines() if l.strip()]\
    if len(atis) != 4:\
        st.error('A Ven\uc0\u817 p\u257  must have exactly **4** a\u7789 i.')\
    else:\
        lines = [split_tamil(l) for l in atis]\
        draw(lines)\
\
st.markdown(\
    '<div style="text-align:center; font-size:0.85em; margin-top:1em;">'\
    'App by Svetlana Kreuzer</div>', unsafe_allow_html=True\
)\
}