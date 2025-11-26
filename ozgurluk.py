{\rtf1\ansi\ansicpg1254\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import date, timedelta\
import time\
\
# --- Sayfa Ayarlar\uc0\u305  ---\
st.set_page_config(\
    page_title="DHY \'d6zg\'fcrl\'fck Sayac\uc0\u305 ",\
    page_icon="\uc0\u55357 \u56650 \u65039 ",\
    layout="centered"\
)\
\
# --- Stil ve E\uc0\u287 lenceli Ba\u351 l\u305 k ---\
st.title("\uc0\u55357 \u56650 \u65039  DHY \'d6zg\'fcrl\'fck Takip\'e7isi")\
st.markdown("""\
*Devlet Hizmeti Y\'fck\'fcml\'fcl\'fc\uc0\u287 \'fc bitti\u287 inde sadece bir doktor de\u287 il, \
ayn\uc0\u305  zamanda bir \'f6zg\'fcrl\'fck sava\u351 \'e7\u305 s\u305  olacaks\u305 n!* """)\
\
st.divider()\
\
# --- Kenar \'c7ubu\uc0\u287 u (Veri Giri\u351 i) ---\
with st.sidebar:\
    st.header("\uc0\u9881 \u65039  Ayarlar")\
    \
    # Ba\uc0\u351 lang\u305 \'e7 Tarihi\
    start_date = st.date_input(\
        "DHY Ba\uc0\u351 lang\u305 \'e7 Tarihin",\
        value=date(2024, 1, 1)\
    )\
    \
    # Toplam S\'fcre (Varsay\uc0\u305 lan 550 g\'fcn)\
    total_service_days = st.number_input(\
        "Toplam Y\'fck\'fcml\'fcl\'fck (G\'fcn)", \
        min_value=1, \
        value=550\
    )\
    \
    st.info("\uc0\u55357 \u56481  Not: A\u351 a\u287 \u305 daki tabloya, **s\'fcreden say\u305 lmayan** (yani biti\u351  tarihini \'f6teleyen) rapor veya \'fccretsiz izinlerini girmelisin. Y\u305 ll\u305 k izinler genelde s\'fcreden say\u305 ld\u305 \u287 \u305  i\'e7in onlar\u305  girmene gerek yok.")\
\
# --- \uc0\u304 zin Y\'f6netimi (Tablo) ---\
st.subheader("\uc0\u55357 \u56541  S\'fcreyi Uzatan \u304 zinler / Raporlar")\
st.write("Hangi ay ne kadar 's\'fcreden say\uc0\u305 lmayan' g\'fcn kulland\u305 \u287 \u305 n\u305  buraya ekle:")\
\
# Ba\uc0\u351 lang\u305 \'e7 veri seti\
if 'leave_data' not in st.session_state:\
    st.session_state.leave_data = pd.DataFrame(\
        [\{"A\'e7\uc0\u305 klama": "\'d6rnek Rapor", "G\'fcn Say\u305 s\u305 ": 0\}],\
    )\
\
# Kullan\uc0\u305 c\u305 n\u305 n d\'fczenleyebilece\u287 i tablo\
edited_df = st.data_editor(\
    st.session_state.leave_data,\
    num_rows="dynamic",\
    column_config=\{\
        "A\'e7\uc0\u305 klama": st.column_config.TextColumn("Ay/A\'e7\u305 klama"),\
        "G\'fcn Say\uc0\u305 s\u305 ": st.column_config.NumberColumn("Eklenen G\'fcn", min_value=0, max_value=365, step=1),\
    \},\
    use_container_width=True\
)\
\
# --- Hesaplamalar ---\
total_extension_days = edited_df["G\'fcn Say\uc0\u305 s\u305 "].sum()\
real_target_days = total_service_days + total_extension_days\
finish_date = start_date + timedelta(days=int(real_target_days))\
today = date.today()\
\
# Ge\'e7en ve Kalan G\'fcnler\
days_passed = (today - start_date).days\
days_remaining = (finish_date - today).days\
\
# Y\'fczdelik Hesaplama\
if real_target_days > 0:\
    progress_percent = (days_passed / real_target_days)\
else:\
    progress_percent = 0\
\
# S\uc0\u305 n\u305 rland\u305 rma (Y\'fczde 0 ile 1 aras\u305 nda kalmal\u305 )\
progress_percent = max(0.0, min(1.0, progress_percent))\
\
# --- Ana Ekran G\'f6stergeleri ---\
\
st.divider()\
\
# Metrikleri G\'f6steren Kolonlar\
col1, col2, col3 = st.columns(3)\
\
with col1:\
    st.metric(label="\uc0\u9203  Toplam Ge\'e7en G\'fcn", value=f"\{days_passed\} G\'fcn")\
\
with col2:\
    st.metric(label="\uc0\u55357 \u57041  Uzatma (Rapor vb.)", value=f"+\{total_extension_days\} G\'fcn", delta_color="inverse")\
\
with col3:\
    st.metric(label="\uc0\u55357 \u56517  Tahmini \'d6zg\'fcrl\'fck", value=finish_date.strftime("%d.%m.%Y"))\
\
# --- Geri Say\uc0\u305 m ve \u304 lerleme \'c7ubu\u287 u ---\
\
st.subheader("\uc0\u55357 \u56960  \'d6zg\'fcrl\'fc\u287 e Giden Yol")\
\
if days_remaining <= 0:\
    st.success("\uc0\u55356 \u57225  TEBR\u304 KLER! DHY B\u304 TT\u304 ! ARTIK \'d6ZG\'dcRS\'dcN! \u55356 \u57225 ")\
    st.balloons()\
    st.image("https://media.giphy.com/media/dummy/giphy.gif") # Buraya e\uc0\u287 lenceli bir gif linki konabilir\
else:\
    # \uc0\u304 lerleme \'c7ubu\u287 u\
    st.progress(progress_percent)\
    st.caption(f"Yolun %\{progress_percent*100:.1f\}'ini tamamlad\uc0\u305 n.")\
    \
    # B\'fcy\'fck Geri Say\uc0\u305 m\
    st.markdown(f"""\
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">\
        <h2 style="color: #333;">\'d6zg\'fcrl\'fc\uc0\u287 e Son</h2>\
        <h1 style="color: #ff4b4b; font-size: 60px;">\{days_remaining\} G\'dcN</h1>\
        <p>Kald\uc0\u305 ...</p>\
    </div>\
    """, unsafe_allow_html=True)\
\
# --- Motivasyon K\'f6\uc0\u351 esi ---\
st.divider()\
st.subheader("\uc0\u55356 \u57263  Mevcut R\'fctben")\
\
if progress_percent < 0.20:\
    st.warning("R\'fctbe: **DHY \'c7\'f6mezi** - Daha yolun ba\uc0\u351 \u305 nday\u305 z, sab\u305 r...")\
elif progress_percent < 0.50:\
    st.info("R\'fctbe: **K\uc0\u305 demli Asistan Havas\u305 ** - Yolu yar\u305 lamaya az kald\u305 .")\
elif progress_percent < 0.80:\
    st.primary("R\'fctbe: **\uc0\u350 afak Sayar** - I\u351 \u305 k g\'f6r\'fcnd\'fc!")\
else:\
    st.success("R\'fctbe: **\'d6zg\'fcrl\'fck Sava\uc0\u351 \'e7\u305 s\u305 ** - Bavullar\u305  toplamaya ba\u351 la!")\
\
# --- E\uc0\u287 lenceli Bir Buton ---\
if st.button("Moralim Bozuk, Bana Motivasyon Ver"):\
    with st.spinner("Motivasyon y\'fckleniyor..."):\
        time.sleep(1.5)\
    st.toast("Unutma, en karanl\uc0\u305 k gece bile sabahla biter! \u55356 \u57093 ", icon="\u55357 \u56613 ")}