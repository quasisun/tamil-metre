# tamil_metre_app.py  –  multi-metre Tamil visualiser
# © 2025  Svetlana Kreuzer   –   uses only std-lib + matplotlib + streamlit

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import re, unicodedata
from typing import List, Tuple

# ─── Tamil character classes ────────────────────────────────
KURIL  = 'அஇஉஎஒ'
NEDIL  = 'ஆஈஊஏஓஔ'
PULLI  = '்'
V_INV  = 'ைொோோௗ'
VOWELS = set(KURIL + NEDIL)

def is_nedil(ch):   return ch in NEDIL or ch in V_INV

# ─── syllable splitter (same as before) ─────────────────────
def split_tamil(txt: str) -> List[str]:
    s = unicodedata.normalize('NFC', txt.strip())
    out, buf = [], ''
    for ch in s:
        if ch.isspace():
            if buf: out.append(buf); buf = ''
            continue
        buf += ch
        if ch in VOWELS or ch == PULLI:
            out.append(buf); buf = ''
    if buf: out.append(buf)
    return out

# ─── nēr / nirai test ───────────────────────────────────────
def is_heavy(akṣ: str) -> bool:
    last = akṣ[-1]
    return last == PULLI or is_nedil(last)

def g_l(line: List[str]) -> str:
    return ''.join('g' if is_heavy(s) else 'l' for s in line)

# seer = mātrai sum (nirai=2, nēr=1)
def seer(line: List[str]) -> int:
    return sum(2 if is_heavy(s) else 1 for s in line)

# ─── metre detectors (rules from “Intro. to Tamil Prosody”) ─
def detect_venpa(seers: Tuple[int,int,int,int]) -> str|None:
    return {
        (4,4,3,4): 'Ciṟ-Veṉpā',
        (4,4,4,4): 'Kalippa Veṉpā',
        (3,4,3,4): 'Viruttappa Veṉpā',
        (3,4,4,4): 'Pā-Veṉpā'
    }.get(seers)

def detect_aciriyappa(seers: Tuple[int,int,int,int]) -> str|None:
    if all(s==8 for s in seers):
        return 'Āciriyappā (4+4 seer)'
    if all(s==7 for s in seers):
        return 'Āciriyappā (7 seer)'
    return None

def detect_kali(lines: List[List[str]], base_name:str|None) -> str|None:
    # Kali veṉpā = a veṉpā shape AND each aṭi ends in nirai
    if base_name and all(is_heavy(a[-1]) for a in lines):
        return 'Kaliṭtāḷai ' + base_name
    return None

def detect_vanci(seers):       # 6 seer each
    return 'Vañci pā'   if all(s==6 for s in seers) else None

def detect_kurinji(seers):     # 5 seer each
    return 'Kuṟiñci pā' if all(s==5 for s in seers) else None

def classify(lines: List[List[str]]) -> str|None:
    if len(lines)!=4: return None
    seers = tuple(seer(l) for l in lines)

    # priority chain
    ven  = detect_venpa(seers)
    kali = detect_kali(lines, ven)
    if ven  and not kali: return ven
    if kali:             return kali

    aci  = detect_aciriyappa(seers)
    if aci:               return aci
    vnc  = detect_vanci(seers)
    if vnc:               return vnc
    kur  = detect_kurinji(seers)
    return kur

# ─── drawing grid ───────────────────────────────────────────
def draw(lines):
    rows, cols = len(lines), max(len(r) for r in lines)
    fig, ax = plt.subplots(figsize=(cols*0.42, rows*0.42))
    ax.set(xlim=(0,cols), ylim=(0,rows)); ax.axis('off'); ax.set_aspect('equal')

    # cells
    for r,row in enumerate(lines):
        y = rows-1-r
        for c, syl in enumerate(row):
            h = is_heavy(syl)
            ax.add_patch(Rectangle((c,y),1,1,
                         facecolor='black' if h else 'white',
                         edgecolor='gray', lw=.8))
            ax.text(c+.5, y+.5, syl, ha='center', va='center',
                    fontsize=12, color='white' if h else 'black')

    # metre label
    tag = classify(lines)
    if tag:
        ax.set_title(tag, fontsize=11)

    st.pyplot(fig); plt.close(fig)

# ─── Streamlit UI ───────────────────────────────────────────
st.set_page_config(page_title='Tamil metre grid', layout='wide')
st.title('Tamil Metre Visualiser (nēr / nirai)')

st.markdown(
    'Paste **4** aṭi (lines). Black = nirai (heavy), white = nēr (light). '
    'App names Ciṟ-, Kalippa-, Viruttappa-, Pā-Veṉpā or Āciriyappā, Kali, '
    'Vañci, Kuṟiñci when the seer pattern matches classical rules.'
)

txt = st.text_area('Tamil input:', height=220)

if st.button('Show'):
    atis = [l.strip() for l in txt.splitlines() if l.strip()]
    if len(atis)!=4:
        st.error('Enter exactly four aṭi.')
    else:
        lines = [split_tamil(a) for a in atis]
        draw(lines)

st.markdown('<div style=\"text-align:center;font-size:0.8em\">'
            'App by Svetlana Kreuzer</div>', unsafe_allow_html=True)
