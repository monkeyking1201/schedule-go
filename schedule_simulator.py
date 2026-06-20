import streamlit as st
import streamlit.components.v1 as components
import os

# ── Google Sheets ──────────────────────────────────────────────────────────────
try:
    import gspread
    GS_AVAILABLE = True
except ImportError:
    GS_AVAILABLE = False

SHEET_ID = "1ewrFUQc1P3YfB3-h9kzuoOLvXcRiee4eLv_R6SBj5oI"

def get_gs_client():
    if os.path.exists("credentials.json"):
        return gspread.service_account(filename="credentials.json")
    else:
        creds_dict = dict(st.secrets["gcp_service_account"])
        return gspread.service_account_from_dict(creds_dict)
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="訓練排表模擬器", page_icon="", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp {
  font-family: 'Inter','Noto Sans TC',-apple-system,sans-serif !important;
  background: #F5F5F7 !important; color: #1d1d1f !important;
}
footer,#MainMenu,header { visibility:hidden !important; }
[data-testid="stToolbar"] { display:none !important; }
.block-container { padding:0 1rem 4rem !important; max-width:100% !important; }

.hero { padding:3.5rem 0 2rem; text-align:center; }
.hero-eyebrow { font-size:.78rem; font-weight:700; letter-spacing:.18em; color:#0071E3; text-transform:uppercase; margin-bottom:.7rem; }
.hero-title { font-size:3.8rem; font-weight:900; color:#1d1d1f; line-height:1.02; letter-spacing:-.04em; margin-bottom:.8rem; }
.hero-sub { font-size:1rem; font-weight:300; color:#86868B; }

.section-block { padding:1.4rem 0 .3rem; display:flex; align-items:baseline; gap:.8rem; }
.section-title { font-size:1.05rem; font-weight:700; color:#1d1d1f; letter-spacing:-.01em; }
.section-range { font-size:.76rem; color:#86868B; }
.section-divider { height:1px; background:#D2D2D7; margin-bottom:.15rem; }

.time-lbl {
  display:flex; align-items:center; justify-content:flex-end;
  padding-right:.8rem; height:120px;
  font-size:1.45rem; font-weight:800; color:#1d1d1f;
  letter-spacing:-.03em; line-height:1.2; text-align:right;
}

[data-testid="stSelectbox"] > label { display:none !important; }
[data-testid="stSelectbox"] > div { padding:0 !important; }
[data-testid="stSelectbox"] {
  background: #FFFFFF !important; border-radius: 16px !important;
  box-shadow: 0 1px 4px rgba(0,0,0,.05), 0 6px 18px rgba(0,0,0,.07) !important;
  overflow: visible !important; transition: box-shadow .2s, transform .15s !important;
  min-height: 120px !important; margin: 0 !important;
  border-left: 4px solid #E5E5EA !important;
  border-top: 1px solid rgba(0,0,0,.05) !important;
  border-right: 1px solid rgba(0,0,0,.05) !important;
  border-bottom: 1px solid rgba(0,0,0,.05) !important;
}
[data-testid="stSelectbox"]:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,.09), 0 18px 44px rgba(0,0,0,.1) !important;
  transform: translateY(-2px) !important;
}
[data-testid="stSelectbox"]:has(span:not([title="休息/空白"])) {
  border-left: 4px solid #0071E3 !important; background: #F5F9FF !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] { min-height:120px !important; }
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
  background: transparent !important; border: none !important; border-radius: 0 !important;
  min-height: 120px !important; padding: 0 .8rem !important; cursor: pointer !important;
  display: flex !important; align-items: center !important; justify-content: space-between !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child:focus-within {
  outline: 2.5px solid #0071E3 !important; outline-offset: -2px !important; border-radius: 14px !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] p {
  font-size: 2.6rem !important; font-weight: 900 !important;
  letter-spacing: -.04em !important; line-height: 1.1 !important; color: #0071E3 !important;
  white-space: normal !important; overflow: visible !important; text-overflow: clip !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span[title="休息/空白"],
[data-testid="stSelectbox"] [data-baseweb="select"] div[title="休息/空白"] {
  color: #D1D1D6 !important; font-weight: 300 !important;
  font-size: 1.1rem !important; letter-spacing: .01em !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] svg,
[data-testid="stSelectbox"] [data-baseweb="select"] svg * {
  fill: #C7C7CC !important; font-size: initial !important; font-weight: initial !important;
  color: initial !important; width: 18px !important; height: 18px !important;
  min-width:18px !important; flex-shrink:0 !important;
}

[data-baseweb="popover"] {
  background:#FFFFFF !important; border:none !important; border-radius:14px !important;
  box-shadow:0 10px 36px rgba(0,0,0,.15),0 2px 8px rgba(0,0,0,.07) !important; overflow:hidden !important;
}
[data-baseweb="popover"] * { color:#1d1d1f !important; }
[data-baseweb="menu"] { background:#FFFFFF !important; padding:8px !important; }
[role="listbox"] { background:#FFFFFF !important; }
[role="option"] {
  background:transparent !important; color:#1d1d1f !important;
  font-size:1.05rem !important; font-weight:400 !important;
  padding:12px 16px !important; border-radius:10px !important; margin:2px 0 !important;
}
[role="option"]:hover { background:#F2F7FF !important; color:#0071E3 !important; font-weight:600 !important; }
[role="option"][aria-selected="true"] {
  background:rgba(0,113,227,.09) !important; color:#0071E3 !important; font-weight:700 !important;
}

[data-testid="column"] { padding:0 .2rem !important; }
[data-testid="stHorizontalBlock"] { gap:0 !important; margin-bottom:.28rem !important; }

section[data-testid="stSidebar"] {
  background:#FFFFFF !important; border-right:1px solid #E5E5EA !important;
}
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] .stMarkdown h3 {
  font-size:1.6rem !important; font-weight:800 !important; color:#1d1d1f !important;
  letter-spacing:-.02em !important; margin-bottom:.6rem !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] .stMarkdown p {
  font-size:1.1rem !important; font-weight:500 !important;
  color:#1d1d1f !important; line-height:1.6 !important;
}
section[data-testid="stSidebar"] span {
  font-size:1.4rem !important; font-weight:800 !important;
  letter-spacing:-.01em !important; line-height:2 !important;
}
section[data-testid="stSidebar"] hr { border-color:#E5E5EA !important; }

.stButton > button {
  background:#0071E3 !important; color:#fff !important; border:none !important;
  border-radius:14px !important; font-family:'Inter','Noto Sans TC',sans-serif !important;
  font-size:1rem !important; font-weight:700 !important; padding:.9rem 2.5rem !important;
  box-shadow:0 3px 12px rgba(0,113,227,.28) !important;
  transition:background .2s,transform .15s,box-shadow .2s !important;
}
.stButton > button:hover {
  background:#0077ED !important; transform:translateY(-2px) !important;
  box-shadow:0 8px 28px rgba(0,113,227,.38) !important;
}
.db-btn > button {
  background: linear-gradient(135deg,#1DB954,#17A045) !important;
  box-shadow: 0 3px 12px rgba(29,185,84,.30) !important;
}
.db-btn > button:hover {
  background: linear-gradient(135deg,#1ED760,#1DB954) !important;
  box-shadow: 0 8px 24px rgba(29,185,84,.40) !important;
}

.result-card {
  background:#FFFFFF; border-radius:28px; padding:3rem 4rem; margin-top:3rem;
  box-shadow:0 4px 20px rgba(0,0,0,.04),0 24px 70px rgba(0,0,0,.07);
}
.result-eyebrow { font-size:.7rem; font-weight:700; letter-spacing:.16em; color:#0071E3; text-transform:uppercase; margin-bottom:.6rem; }
.result-title { font-size:1.8rem; font-weight:800; color:#1d1d1f; letter-spacing:-.025em; margin-bottom:.3rem; }
.result-sub { font-size:.85rem; color:#86868B; margin-bottom:2.5rem; }
.stat-row { display:flex; gap:1px; background:#E5E5EA; border-radius:18px; overflow:hidden; margin-bottom:3rem; }
.stat-cell { flex:1; background:#fff; padding:2rem 2rem 1.6rem; }
.stat-num { font-size:3.5rem; font-weight:800; letter-spacing:-.05em; line-height:1; margin-bottom:.4rem; }
.stat-lbl { font-size:.75rem; font-weight:500; color:#86868B; letter-spacing:.03em; }

.dist-section { margin-bottom:2.5rem; }
.dist-heading { font-size:.68rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; color:#86868B; margin-bottom:1.2rem; }
.stacked-bar { display:flex; height:24px; border-radius:12px; overflow:hidden; margin-bottom:1rem; gap:2px; }
.stacked-seg { transition:flex .4s; border-radius:4px; }
.legend-row { display:flex; flex-wrap:wrap; gap:.8rem 1.6rem; margin-bottom:2rem; }
.legend-item { display:flex; align-items:center; gap:.4rem; font-size:.82rem; font-weight:500; color:#1d1d1f; }
.legend-dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
.cat-bar-row { margin-bottom:1rem; }
.cat-bar-header { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:.35rem; }
.cat-bar-name { font-size:.9rem; font-weight:600; color:#1d1d1f; }
.cat-bar-info { font-size:.82rem; color:#86868B; }
.cat-bar-track { height:12px; background:#F0F0F3; border-radius:6px; overflow:hidden; }
.cat-bar-fill { height:100%; border-radius:6px; }

.cat-section { margin-bottom:2rem; }
.cat-heading { font-size:.66rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; padding-bottom:.6rem; border-bottom:1px solid #E5E5EA; margin-bottom:.8rem; }
.item-row { display:flex; justify-content:space-between; align-items:center; padding:.55rem 0; border-bottom:1px solid #F5F5F7; }
.item-row:last-child { border-bottom:none; }
.item-name { font-size:.9rem; font-weight:500; color:#1d1d1f; }
.item-right { display:flex; gap:1rem; align-items:center; }
.item-hrs { font-size:.9rem; font-weight:700; }
.item-pct { font-size:.78rem; font-weight:500; color:#86868B; min-width:3.2rem; text-align:right; }

@page { size: A4 portrait; margin: 6mm 5mm; }
@media print {
  section[data-testid="stSidebar"], header, footer,
  [data-testid="stToolbar"], [data-testid="stDecoration"],
  .stButton, iframe, .hero-eyebrow, .hero-sub, .result-card { display: none !important; }
  html, body, .stApp, .block-container {
    background: #ffffff !important; color: #000000 !important;
    margin: 0 !important; padding: 0 !important; width: 100% !important;
  }
  .hero { padding: .3rem 0 .2rem !important; }
  .hero-title { font-size: 1.6rem !important; color: #000000 !important; margin: 0 0 .2rem !important; text-align:center !important; }
  .section-block { padding: .25rem 0 .1rem !important; }
  .section-title { font-size: .9rem !important; font-weight: 800 !important; color: #000000 !important; }
  .section-range { font-size: .68rem !important; color: #444 !important; }
  .section-divider { background: #000000 !important; margin-bottom:.05rem !important; }
  .time-lbl { color: #000000 !important; font-size: .72rem !important; font-weight: 700 !important; height: 100px !important; padding-right: .35rem !important; }
  [data-testid="column"] { padding: 0 .05rem !important; }
  [data-testid="stHorizontalBlock"] { margin-bottom: .1rem !important; }
  [data-testid="stSelectbox"] {
    background: #ffffff !important; border: 1.2px solid #000000 !important;
    border-left: 1.2px solid #000000 !important; border-radius: 3px !important;
    box-shadow: none !important; transform: none !important;
    min-height: 100px !important; height: 100px !important; transition: none !important; width: 100% !important;
  }
  [data-testid="stSelectbox"] [data-baseweb="select"] { min-height: 100px !important; height:100px !important; }
  [data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
    min-height: 100px !important; height: 100px !important; padding: 4px 5px !important;
    display: flex !important; align-items: center !important; justify-content: center !important; overflow: visible !important;
  }
  [data-testid="stSelectbox"] [data-baseweb="select"] div,
  [data-testid="stSelectbox"] [data-baseweb="select"] span,
  [data-testid="stSelectbox"] [data-baseweb="select"] p {
    color: #000000 !important; font-size: .95rem !important; font-weight: 700 !important;
    letter-spacing: -.01em !important; line-height: 1.3 !important;
    white-space: normal !important; overflow: visible !important;
    text-overflow: clip !important; max-width: none !important; width: auto !important; text-align: center !important;
  }
  [data-testid="stSelectbox"] [data-baseweb="select"] span[title="休息/空白"],
  [data-testid="stSelectbox"] [data-baseweb="select"] div[title="休息/空白"] {
    color: #bbbbbb !important; font-weight: 400 !important; font-size: .72rem !important;
  }
  [data-testid="stSelectbox"] [data-baseweb="select"] svg { display: none !important; }
  .print-page-break { page-break-before: always !important; break-before: page !important; }
  [data-testid="stHorizontalBlock"] { page-break-inside: avoid !important; break-inside: avoid !important; }
}
</style>
""", unsafe_allow_html=True)

DAYS_ZH = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
OPTIONS  = ["休息/空白","下棋實戰","網棋對弈","打譜","AI 檢討","做題目","靜心研究","運動","閱讀","上課","吃飯","睡覺","自由時間"]
EMOJI    = {"下棋實戰":"♟","網棋對弈":"\U0001f310","打譜":"\U0001f4d6","AI 檢討":"\U0001f916","做題目":"✏","靜心研究":"◎","運動":"◉","閱讀":"□","上課":"✦","吃飯":"▷","睡覺":"◐","自由時間":"○","休息/空白":"—"}
CATMAP   = {"下棋實戰":"T","網棋對弈":"T","上課":"T","打譜":"R","AI 檢討":"R","做題目":"R","靜心研究":"R","運動":"K","閱讀":"K","吃飯":"O","睡覺":"O","自由時間":"O","休息/空白":"O"}
CAT_LBL  = {"T":"實戰訓練","R":"研究精進","K":"恢復調整","O":"生活其他"}
CAT_COL  = {"T":"#0071E3","R":"#34C759","K":"#AF52DE","O":"#86868B"}

GROUPS = [
    {"id":"mg","title":"早上","range":"07:00 - 12:00","slots":["07:00-08:00","08:00-09:00","09:00-10:00","10:00-11:00","11:00-12:00"],"page_break":False},
    {"id":"af","title":"下午","range":"12:00 - 18:00","slots":["12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00","17:00-18:00"],"page_break":True},
    {"id":"ev","title":"晚上","range":"18:00 - 22:00","slots":["18:00-19:00","19:00-20:00","20:00-21:00","21:00-22:00"],"page_break":True},
]
ALL_SLOTS = [s for g in GROUPS for s in g["slots"]]
SLOT_TO_PERIOD = {s: g["title"] for g in GROUPS for s in g["slots"]}

if "schedule" not in st.session_state:
    st.session_state.schedule = {(s,d):OPTIONS[0] for s in ALL_SLOTS for d in DAYS_ZH}

with st.sidebar:
    st.markdown("### 使用方式")
    st.markdown("點擊卡片選擇訓練項目。每格 = **1 小時**。完成後按統計。")
    st.divider()
    for cat,col in CAT_COL.items():
        st.markdown('<span style="color:'+col+';font-weight:800;font-size:1.4rem">● '+CAT_LBL[cat]+'</span>', unsafe_allow_html=True)
    st.divider()

    st.markdown("### 雲端大腦")
    student_name = st.text_input("學員姓名", value="陳映嘉")

    st.markdown('<div class="db-btn">', unsafe_allow_html=True)
    sync_btn = st.button("\U0001f9e0 將此課表同步至大腦資料庫", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if sync_btn:
        if not GS_AVAILABLE:
            st.error("請先安裝 gspread：pip install gspread google-auth")
        else:
            rows = []
            for day in DAYS_ZH:
                for slot in ALL_SLOTS:
                    val = st.session_state.schedule.get((slot, day), OPTIONS[0])
                    if val and val != OPTIONS[0]:
                        period = SLOT_TO_PERIOD[slot]
                        rows.append([student_name, day, period, slot, val])
            if not rows:
                st.warning("課表中尚無任何訓練項目，請先填寫課表。")
            else:
                try:
                    with st.spinner("正在寫入雲端大腦…"):
                        client = get_gs_client()
                        sh     = client.open_by_key(SHEET_ID)
                        ws     = sh.sheet1
                        ws.append_rows(rows, value_input_option="USER_ENTERED")
                    st.success("課表已成功建檔至雲端大腦！共寫入 "+str(len(rows))+" 筆紀錄。")
                except FileNotFoundError:
                    st.error("找不到憑證檔案：credentials.json")
                except Exception as e:
                    st.error("寫入失敗："+str(e))

st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Professional Training Scheduler</div>
  <div class="hero-title">七月暑期訓練排表</div>
  <div class="hero-sub">為職業棋士設計的訓練計劃工具 — 規劃每週課表，系統自動推算七月整月訓練量</div>
</div>""", unsafe_allow_html=True)

components.html("""
<style>
  body { margin:0; display:flex; justify-content:center; padding:.5rem 0; background:transparent; }
  button {
    display:inline-flex; align-items:center; gap:.5rem;
    background:#1d1d1f; color:#fff; border:none; border-radius:14px;
    font-family:'Noto Sans TC','Inter',sans-serif;
    font-size:1rem; font-weight:700; padding:.85rem 2.4rem; cursor:pointer;
    box-shadow:0 3px 12px rgba(0,0,0,.22); transition:background .18s, transform .15s;
  }
  button:hover { background:#333; transform:translateY(-2px); }
</style>
<button onclick="window.parent.print()">匯出 PDF / 列印課表</button>
""", height=66)

for g in GROUPS:
    pb_class = "print-page-break" if g["page_break"] else ""
    st.markdown(
        '<div class="section-block '+pb_class+'">'
        '<span class="section-title">'+g["title"]+'</span>'
        '<span class="section-range">'+g["range"]+'</span></div>'
        '<div class="section-divider"></div>', unsafe_allow_html=True)

    hdr = st.columns([1.8]+[2]*7)
    with hdr[0]: st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
    for i,d in enumerate(DAYS_ZH):
        with hdr[i+1]:
            st.markdown('<div style="text-align:center;font-size:.62rem;font-weight:700;letter-spacing:.1em;color:#86868B;text-transform:uppercase;padding:.15rem 0 .45rem">'+d+'</div>', unsafe_allow_html=True)

    for slot in g["slots"]:
        row = st.columns([1.8]+[2]*7)
        with row[0]:
            st.markdown('<div class="time-lbl">'+slot+'</div>', unsafe_allow_html=True)
        for i,day in enumerate(DAYS_ZH):
            with row[i+1]:
                cur = st.session_state.schedule.get((slot,day),OPTIONS[0])
                val = st.selectbox(label="", options=OPTIONS, index=OPTIONS.index(cur), key="s_"+slot+day, label_visibility="collapsed")
                st.session_state.schedule[(slot,day)] = val

    st.markdown('<div style="margin-bottom:.5rem"></div>', unsafe_allow_html=True)

_,mid,_ = st.columns([3,2,3])
with mid:
    go = st.button("生成七月訓練總量報告", use_container_width=True)

if go:
    counts = {}
    for (_s,_d),v in st.session_state.schedule.items():
        if v and v != OPTIONS[0]:
            counts[v] = counts.get(v,0)+1
    monthly = {k:v*4 for k,v in counts.items()}
    by_cat = {"T":[],"R":[],"K":[],"O":[]}
    for item,hrs in monthly.items():
        by_cat[CATMAP.get(item,"O")].append((item,hrs))

    total_core   = sum(h for c in ["T","R"] for _,h in by_cat[c])
    total_active = sum(h for c in ["T","R","K"] for _,h in by_cat[c])
    total_all    = sum(monthly.values())
    total_slots  = 15*7*4
    rest_hrs     = max(total_slots - total_all, 0)
    cat_hrs = {c: sum(h for _,h in by_cat[c]) for c in ["T","R","K","O"]}
    grand = sum(cat_hrs.values()) or 1

    stat_html = (
        '<div class="stat-row">'
        '<div class="stat-cell"><div class="stat-num" style="color:#0071E3">'+str(total_core)+'</div><div class="stat-lbl">核心棋藝時數 (hr)</div></div>'
        '<div class="stat-cell"><div class="stat-num" style="color:#34C759">'+str(total_active)+'</div><div class="stat-lbl">全部有效時數 (hr)</div></div>'
        '<div class="stat-cell"><div class="stat-num" style="color:#86868B">'+str(rest_hrs)+'</div><div class="stat-lbl">未使用時段 (hr)</div></div>'
        '</div>'
    )

    stacked_segs = ""
    for c in ["T","R","K","O"]:
        hrs = cat_hrs[c]
        if hrs == 0: continue
        pct = hrs / grand * 100
        stacked_segs += '<div class="stacked-seg" style="flex:'+str(round(pct,2))+';background:'+CAT_COL[c]+'"></div>'

    legend_items = ""
    for c in ["T","R","K","O"]:
        pct = cat_hrs[c] / grand * 100
        legend_items += '<div class="legend-item"><div class="legend-dot" style="background:'+CAT_COL[c]+'"></div>'+CAT_LBL[c]+' '+str(round(pct,1))+'%</div>'

    bar_rows = ""
    for c in ["T","R","K","O"]:
        hrs = cat_hrs[c]
        pct = hrs / grand * 100
        bar_rows += (
            '<div class="cat-bar-row">'
            '<div class="cat-bar-header">'
            '<span class="cat-bar-name" style="color:'+CAT_COL[c]+'">'+CAT_LBL[c]+'</span>'
            '<span class="cat-bar-info">'+str(hrs)+' hr  '+str(round(pct,1))+'%</span>'
            '</div>'
            '<div class="cat-bar-track">'
            '<div class="cat-bar-fill" style="width:'+str(round(pct,2))+'%;background:'+CAT_COL[c]+'"></div>'
            '</div></div>'
        )

    dist_html = (
        '<div class="dist-section">'
        '<div class="dist-heading">時間分布一覽</div>'
        '<div class="stacked-bar">'+stacked_segs+'</div>'
        '<div class="legend-row">'+legend_items+'</div>'
        +bar_rows+'</div>'
    )

    cat_html = ""
    for ckey in ["T","R","K","O"]:
        items = by_cat[ckey]
        if not items: continue
        ctot = sum(h for _,h in items)
        col  = CAT_COL[ckey]
        lbl  = CAT_LBL[ckey]
        rows_html = ""
        for item,hrs in sorted(items,key=lambda x:-x[1]):
            em = EMOJI.get(item,"")
            item_pct = hrs / grand * 100
            rows_html += (
                '<div class="item-row">'
                '<span class="item-name">'+em+'  '+item+'</span>'
                '<span class="item-right">'
                '<span class="item-pct">'+str(round(item_pct,1))+'%</span>'
                '<span class="item-hrs" style="color:'+col+'">'+str(hrs)+' hr</span>'
                '</span></div>'
            )
        ctot_pct = ctot / grand * 100
        cat_html += (
            '<div class="cat-section">'
            '<div class="cat-heading" style="color:'+col+'">'+lbl+' - '+str(ctot)+' hr - '+str(round(ctot_pct,1))+'%</div>'
            +rows_html+'</div>'
        )

    html = (
        '<div class="result-card">'
        '<div class="result-eyebrow">July Training Report</div>'
        '<div class="result-title">七月整月訓練預測</div>'
        '<div class="result-sub">以本週課表 x 4 計算，涵蓋 '+str(total_slots)+' 個總可用時段（07:00-22:00）</div>'
        +stat_html+dist_html+cat_html+'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
