# tamil_venpa_app.py
# Tamil Veṉpā Visualiser  —  nēr / nirai grid
# (c) 2025  Svetlana Kreuzer

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import re, unicodedata
from typing import List

# ───── Tamil character classes ───────────────────────────
KURIL  = 'அஇஉஎஒ'                  # short vowels = 1 mātrai
NEDIL  = 'ஆஈஊஏஓஔ'                # long vowels = 2 mātrai
PULLI  = '்'                        # virāma sign (consonant ending)
V_INV  = 'ைொோோௗ'                  # composite long vowels, treat as nedil

VOWELS = set(KURIL + NEDIL)

# ───── helper predicates ────────────────────────────────
def is_nedil(ch: str) -> bool:
    return ch in NEDIL or ch in V_INV

# ───── syllable (“akṣaram”) splitter ────────────────────

def split_tamil(text: str) -> List[str]:
    """Very light-weight syllable splitter good enough for Veṉpā."""
    s = unicodedata.normalize('NFC', text.strip())
    out, buf = [], ''
    for ch in s:
        if ch.isspace():
            if buf:
                out.append(buf)
                buf = ''
            continue
        buf += ch
        # break if current code‑point ends a syllable
        if ch in VOWELS or ch == PULLI:
            out.append(buf)
            buf = ''
    if buf:
        out.append(buf)
    return out

# ───── guru / laghu analogue: nirai / nēr ───────────────

def is_heavy(akṣ: str) -> bool:
    last = akṣ[-1]
    return last == PULLI or is_nedil(last)

# ───── Veṉpā templates (seer counts per aṭi) ────────────
VENPA_SHAPES = {
    (4, 4, 3, 4): 'Ciṟ‑Veṉpā  (4‑4‑3‑4)',
    (4, 4, 4, 4): 'Kalippa     (4‑4‑4‑4)',
    (3, 4, 3, 4): 'Viruttappa  (3‑4‑3‑4)',
    (3, 4, 4, 4): 'Pā‑Veṉpā   (3‑4‑4‑4)'
}

def seer_count(aṭi: List[str]) -> int:
    """1 mātrai for light, 2 for heavy."""
    return sum(2 if is_heavy(s) else 1 for s in aṭi)

# ───── grid drawing ─────────────────────────────────────

def draw(lines: List[List[str]]):
    rows, cols = len(lines), max(len(r) for r in lines)
    fig, ax = plt.subplots(figsize=(cols * 0.45, rows * 0.45))
    ax.set(xlim=(0, cols), ylim=(0, rows))
    ax.axis('off')
    ax.set_aspect('equal')

    # draw cells and glyphs
    for r, row in enumerate(lines):
        y = rows - 1 - r
        for c, ak in enumerate(row):
            heavy = is_heavy(ak)
            ax.add_patch(Rectangle((c, y), 1, 1,
                         facecolor='black' if heavy else 'white',
                         edgecolor='gray', zorder=1))
            ax.text(c + 0.5, y + 0.5, ak, fontsize=12,
                    ha='center', va='center',
                    color='white' if heavy else 'black', zorder=2)

    # pattern highlight
    counts = tuple(seer_count(r) for r in lines)
    label = VENPA_SHAPES.get(counts)
    if label:
        for r in range(rows):
            y = rows - 1 - r
            ax.add_patch(Rectangle((0, y), 1, 1,
                         facecolor='#FFB347', alpha=0.45, zorder=3))
        ax.set_title(label, fontsize=11)

    st.pyplot(fig)
    plt.close(fig)

# ───── Streamlit UI ────────────────────────────────────
st.set_page_config(page_title='Veṉpā Meter', layout='wide')

st.title('Tamil Veṉpā Visualiser')

st.markdown(
    '*Paste exactly four **aṭi** (one per line). Black = nirai (heavy), '
    'white = nēr (light). 4‑4‑3‑4 etc. shapes auto‑highlight.*'
)

txt = st.text_area('Tamil input:', height=200)

if st.button('Show'):
    atis = [l.strip() for l in txt.splitlines() if l.strip()]
    if len(atis) != 4:
        st.error('A Veṉpā has exactly **4** aṭi.')
    else:
        lines = [split_tamil(a) for a in atis]
        draw(lines)

st.markdown(
    '<div style="text-align:center; font-size:0.85em; margin-top:1em;">'
    'App by Svetlana Kreuzer</div>', unsafe_allow_html=True
)
