import streamlit as st
import pandas as pd
from datetime import date, timedelta
import time

# --- Sayfa Ayarları ---
st.set_page_config(
    page_title="DHY Özgürlük Sayacı",
    page_icon="🕊️",
    layout="centered"
)

# --- Stil ve Eğlenceli Başlık ---
st.title("🕊️ DHY Özgürlük Takipçisi")
st.markdown("""
*Devlet Hizmeti Yükümlülüğü bittiğinde sadece bir doktor değil, 
aynı zamanda bir özgürlük savaşçısı olacaksın!* """)

st.divider()

# --- Kenar Çubuğu (Veri Girişi) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    
    # Başlangıç Tarihi
    start_date = st.date_input(
        "DHY Başlangıç Tarihin",
        value=date(2024, 1, 1)
    )
    
    # Toplam Süre (Varsayılan 550 gün)
    total_service_days = st.number_input(
        "Toplam Yükümlülük (Gün)", 
        min_value=1, 
        value=550
    )
    
    st.info("💡 Not: Aşağıdaki tabloya, **süreden sayılmayan** (yani bitiş tarihini öteleyen) rapor veya ücretsiz izinlerini girmelisin. Yıllık izinler genelde süreden sayıldığı için onları girmene gerek yok.")

# --- İzin Yönetimi (Tablo) ---
st.subheader("📝 Süreyi Uzatan İzinler / Raporlar")
st.write("Hangi ay ne kadar 'süreden sayılmayan' gün kullandığını buraya ekle:")

# Başlangıç veri seti
if 'leave_data' not in st.session_state:
    st.session_state.leave_data = pd.DataFrame(
        [{"Açıklama": "Örnek Rapor", "Gün Sayısı": 0}],
    )

# Kullanıcının düzenleyebileceği tablo
edited_df = st.data_editor(
    st.session_state.leave_data,
    num_rows="dynamic",
    column_config={
        "Açıklama": st.column_config.TextColumn("Ay/Açıklama"),
        "Gün Sayısı": st.column_config.NumberColumn("Eklenen Gün", min_value=0, max_value=365, step=1),
    },
    use_container_width=True
)

# --- Hesaplamalar ---
total_extension_days = edited_df["Gün Sayısı"].sum()
real_target_days = total_service_days + total_extension_days
finish_date = start_date + timedelta(days=int(real_target_days))
today = date.today()

# Geçen ve Kalan Günler
days_passed = (today - start_date).days
days_remaining = (finish_date - today).days

# Yüzdelik Hesaplama
if real_target_days > 0:
    progress_percent = (days_passed / real_target_days)
else:
    progress_percent = 0

# Sınırlandırma (Yüzde 0 ile 1 arasında kalmalı)
progress_percent = max(0.0, min(1.0, progress_percent))

# --- Ana Ekran Göstergeleri ---

st.divider()

# Metrikleri Gösteren Kolonlar
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="⏳ Toplam Geçen Gün", value=f"{days_passed} Gün")

with col2:
    st.metric(label="🛑 Uzatma (Rapor vb.)", value=f"+{total_extension_days} Gün", delta_color="inverse")

with col3:
    st.metric(label="📅 Tahmini Özgürlük", value=finish_date.strftime("%d.%m.%Y"))

# --- Geri Sayım ve İlerleme Çubuğu ---

st.subheader("🚀 Özgürlüğe Giden Yol")

if days_remaining <= 0:
    st.success("🎉 TEBRİKLER! DHY BİTTİ! ARTIK ÖZGÜRSÜN! 🎉")
    st.balloons()
    st.image("https://media.giphy.com/media/dummy/giphy.gif") 
else:
    # İlerleme Çubuğu
    st.progress(progress_percent)
    st.caption(f"Yolun %{progress_percent*100:.1f}'ini tamamladın.")
    
    # Büyük Geri Sayım
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
        <h2 style="color: #333;">Özgürlüğe Son</h2>
        <h1 style="color: #ff4b4b; font-size: 60px;">{days_remaining} GÜN</h1>
        <p>Kaldı...</p>
    </div>
    """, unsafe_allow_html=True)

# --- Motivasyon Köşesi ---
st.divider()
st.subheader("🎯 Mevcut Rütben")

if progress_percent < 0.20:
    st.warning("Rütbe: **DHY Çömezi** - Daha yolun başındayız, sabır...")
elif progress_percent < 0.50:
    st.info("Rütbe: **Kıdemli Asistan Havası** - Yolu yarılamaya az kaldı.")
elif progress_percent < 0.80:
    st.primary("Rütbe: **Şafak Sayar** - Işık göründü!")
else:
    st.success("Rütbe: **Özgürlük Savaşçısı** - Bavulları toplamaya başla!")

# --- Eğlenceli Bir Buton ---
if st.button("Moralim Bozuk, Bana Motivasyon Ver"):
    with st.spinner("Motivasyon yükleniyor..."):
        time.sleep(1.5)
    st.toast("Unutma, en karanlık gece bile sabahla biter! 🌅", icon="🔥")
