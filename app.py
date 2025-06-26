import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime

# -----------------------------------------------------------------------------
# Sayfa Konfigürasyonu
# -----------------------------------------------------------------------------
# Streamlit sayfasının temel ayarları. Sayfa başlığı, ikonu ve yerleşim düzeni belirlenir.
st.set_page_config(
    page_title="Satış Liderlik Tablosu",
    page_icon="🏆",
    layout="wide"  # Sayfanın tam genişlikte kullanılmasını sağlar.
)

# -----------------------------------------------------------------------------
# Google Apps Script'ten Veri Çekme Fonksiyonu
# -----------------------------------------------------------------------------
# Bu fonksiyon, Google E-Tablolar'daki verileri çeken Apps Script'e bağlanır.
# Streamlit'in @st.cache_data dekoratörü sayesinde, aynı filtrelerle tekrar
# veri çekildiğinde sonuçlar önbellekten alınır, bu da performansı artırır.
# Veri, 20 dakika (1200 saniye) boyunca önbellekte tutulur.

@st.cache_data(ttl=1200)
def fetch_data(month, year):
    """
    Belirtilen ay ve yıl için Google Apps Script'ten liderlik tablosu verilerini çeker.
    """
    # Google Apps Script Web Uygulaması URL'si (HTML kodundan alındı)
    url = f"https://script.google.com/macros/s/AKfycbwHjG2pWCFT3nZm2jfl1shZ5E6VV0wwoWiogJN-UH73iLDJ8iHpkQgM5jDR275anBnuEA/exec?month={month}&year={year}"
    try:
        response = requests.get(url, timeout=30)
        # HTTP isteği başarılı değilse hata fırlat
        response.raise_for_status()
        
        # Gelen JSON verisini bir Pandas DataFrame'e dönüştür
        data = response.json()
        if not data:
            return pd.DataFrame() # Veri yoksa boş DataFrame döndür

        df = pd.DataFrame(data)
        
        # 'totalCiro' sütununa göre verileri büyükten küçüğe sırala
        df = df.sort_values(by="totalCiro", ascending=False).reset_index(drop=True)
        # Sıralama numarasını (rank) ekle (1'den başlayarak)
        df['Sıra'] = df.index + 1
        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Veri çekilirken bir ağ hatası oluştu: {e}")
        return pd.DataFrame() # Hata durumunda boş DataFrame döndür
    except ValueError as e:
        # JSON parse hatası olursa
        st.error(f"Veri formatı hatalı (JSON bekleniyordu): {e}")
        st.info("Lütfen Google Apps Script'inizin doğru bir JSON dizisi döndürdüğünden emin olun.")
        return pd.DataFrame()


# -----------------------------------------------------------------------------
# Arayüz (UI) Oluşturma
# -----------------------------------------------------------------------------

# --- Başlık ve Logo ---
col1, col2 = st.columns([1, 4])
with col1:
    # Şirket logosu. Hata durumunda placeholder gösterilir.
    st.image("https://static.ticimax.cloud/32769/uploads/editoruploads/hedef-image/logo.png", width=150)
with col2:
    st.title("Satış Liderlik Tablosu")
    st.markdown("Şubelerin aylık ciro performanslarını takip edin.")

# --- Filtreleme Seçenekleri ---
st.sidebar.header("Filtreler")

# Ay ve yıl seçimi için listeler oluşturulur.
month_names = [
    'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
]
month_map = {name: i for i, name in enumerate(month_names)} # Ay ismini sayısal değere çevirir

current_year = datetime.now().year
current_month_name = month_names[datetime.now().month - 1]

# Sidebar üzerinde ay ve yıl seçimi için selectbox'lar
selected_month_name = st.sidebar.selectbox(
    "Ay Seçin",
    options=month_names,
    index=datetime.now().month - 1
)
selected_year = st.sidebar.selectbox(
    "Yıl Seçin",
    options=range(current_year, current_year - 5, -1)
)

# Seçilen ay ismini sayısal değere çevir
selected_month_index = month_map[selected_month_name]

# --- Verileri Çek ve Göster ---
# `st.spinner` ile veri yüklenirken kullanıcıya bilgi verilir.
with st.spinner(f"{selected_month_name} {selected_year} verileri yükleniyor..."):
    leaderboard_df = fetch_data(selected_month_index, selected_year)

# Veri başarıyla çekildiyse işlemlere devam et
if not leaderboard_df.empty:
    st.success(f"**{selected_month_name} {selected_year}** dönemi liderlik tablosu başarıyla yüklendi.")
    st.markdown("---")

    # --- TOP 3 Performans Kartları ---
    st.subheader("🏆 Ayın En İyi Performans Gösterenleri")
    top_3 = leaderboard_df.head(3)
    
    # st.columns ile 3'lü sütun yapısı oluşturulur
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    
    for i, row in top_3.iterrows():
        with cols[i]:
            # st.metric ile vurgulu ve ikonlu veri gösterimi yapılır
            st.metric(
                label=f"{medals[i]} {row['branch']}",
                value=f"{row['totalCiro']:,.2f} TL",
                help=f"Sıra: {row['Sıra']}"
            )

    st.markdown("---")

    # --- Liderlik Tablosu ve Grafik ---
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        # --- Diğer Şubeler Tablosu (4. sıradan itibaren) ---
        st.subheader("Genel Sıralama")
        other_branches = leaderboard_df.copy()
        
        # Tabloda gösterilecek sütunlar seçilir ve formatlanır
        display_cols = ['Sıra', 'branch', 'totalCiro', 'successfulSalesCount', 'saleRate']
        other_branches_display = other_branches[display_cols]
        other_branches_display = other_branches_display.rename(columns={
            'branch': 'Şube',
            'totalCiro': 'Toplam Ciro (TL)',
            'successfulSalesCount': 'Satış Sayısı',
            'saleRate': 'Satış Oranı (%)'
        })
        
        # st.dataframe ile interaktif bir tablo gösterilir
        st.dataframe(
            other_branches_display,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Toplam Ciro (TL)": st.column_config.NumberColumn(format="%.2f TL")
            }
        )

    with col2:
        # --- Şube Ciro Karşılaştırma Grafiği ---
        st.subheader("Şube Ciro Karşılaştırması")

        # Altair kütüphanesi ile interaktif bir çubuk grafik oluşturulur
        chart = alt.Chart(leaderboard_df).mark_bar().encode(
            x=alt.X('totalCiro:Q', title='Toplam Ciro (TL)'),
            y=alt.Y('branch:N', title='Şube', sort='-x'), # Cirosu en yüksek olan en üstte olacak şekilde sırala
            tooltip=[
                alt.Tooltip('branch', title='Şube'),
                alt.Tooltip('totalCiro', title='Toplam Ciro', format=',.2f TL'),
                alt.Tooltip('Sıra', title='Sıralama')
            ],
            color=alt.condition(
                # En yüksek ciroya sahip barı farklı bir renkle vurgula
                alt.datum.totalCiro == leaderboard_df['totalCiro'].max(),
                alt.value('orange'),  # Vurgu rengi
                alt.value('steelblue')   # Diğer barların rengi
            )
        ).properties(
            title=f"{selected_month_name} {selected_year} Ciro Dağılımı"
        ).interactive() # Grafiğin yakınlaştırılabilir/kaydırılabilir olmasını sağlar

        st.altair_chart(chart, use_container_width=True)

else:
    # Veri çekilemediyse veya boş ise kullanıcıya bilgi verilir
    st.warning(f"**{selected_month_name} {selected_year}** dönemi için gösterilecek veri bulunamadı.")
    st.info("Lütfen farklı bir ay/yıl seçin veya Google E-Tablonuzda ilgili dönem için veri olduğundan emin olun.")

# Son güncelleme zamanını göster
st.sidebar.info(f"Veriler en son {datetime.now().strftime('%d %B %Y, %H:%M:%S')} tarihinde kontrol edildi.")
