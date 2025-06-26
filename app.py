import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --------------------------------------------------------------------------------
# Sayfa Yapılandırması ve Stil
# --------------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Satış Liderlik Tablosu")

# Streamlit arayüzünü özelleştirmek için CSS kodları
# Bu, gradyan arka planı ve özel kart stillerini uygulamamızı sağlar.
def local_css():
    st.markdown("""
        <style>
            /* Streamlit'in ana bloğunun arka planını özelleştir */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            /* Sayfanın kendisine gradyan arka planı uygula */
            body {
                background: linear-gradient(135deg, #6a0dad 0%, #00008b 100%);
                background-attachment: fixed;
                color: white; /* Varsayılan metin rengi */
            }
            /* Streamlit bileşenlerinin renklerini daha okunabilir yap */
            h1, h2, h3, p, .stDataFrame, .stSelectbox, .stButton {
                color: white !important;
            }
            .stDataFrame {
                color: #333; /* DataFrame içeriği için koyu renk */
            }
            
            /* Başlık stili */
            h1 {
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }

            /* Top 3 Kart Stilleri */
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
                text-align: center;
                transition: transform 0.3s ease-in-out;
                position: relative;
                color: #333;
                border: none;
            }
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"]:hover {
                transform: translateY(-5px);
            }

            /* Özel sınıflar için CSS */
            .rank-1-card {
                background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%); /* Altın */
                transform: translateY(-20px);
                z-index: 10;
            }
            .rank-2-card {
                background: linear-gradient(135deg, #c0c0c0 0%, #808080 100%); /* Gümüş */
                 transform: translateY(-10px);
            }
            .rank-3-card {
                background: linear-gradient(135deg, #cd7f32 0%, #a0522d 100%); /* Bronz */
            }
            .card-name {
                font-weight: 700;
                font-size: 1.2rem;
                margin-bottom: 5px;
            }
            .card-score {
                font-weight: 800;
                font-size: 1.4rem;
            }
             .card-rank-badge {
                position: absolute;
                top: 10px;
                left: 15px;
                font-size: 1.2rem;
                font-weight: 900;
                color: rgba(0,0,0,0.4);
            }
            .crown-icon {
                font-size: 3rem;
                margin-bottom: 10px;
                color: rgba(255, 255, 255, 0.9);
            }
            .stButton>button {
                width: 100%;
                margin-top: 15px;
                border: 2px solid rgba(0,0,0,0.3);
                background-color: rgba(255,255,255,0.2);
                color: white;
            }
            .stButton>button:hover {
                 background-color: rgba(255,255,255,0.4);
                 color: black;
                 border-color: black;
            }
        </style>
        <!-- Font Awesome ikonları için link -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------
# Veri Çekme Fonksiyonu
# --------------------------------------------------------------------------------

# Google Apps Script'ten verileri çeker ve önbelleğe alır.
# ttl=1200 saniye (20 dakika) sonra önbellek temizlenir ve veri yeniden çekilir.
@st.cache_data(ttl=1200)
def fetch_leaderboard_data(month, year):
    """
    Belirtilen ay ve yıl için Google Apps Script'ten liderlik tablosu verilerini çeker.
    """
    # KENDİ GOOGLE APPS SCRIPT WEB UYGULAMANIZIN URL'SİNİ BURAYA YAPIŞTIRIN
    url = f"https://script.google.com/macros/s/AKfycbwHjG2pWCFT3nZm2jfl1shZ5E6VV0wwoWiogJN-UH73iLDJ8iHpkQgM5jDR275anBnuEA/exec?month={month}&year={year}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        data = response.json()
        if not isinstance(data, list):
            return pd.DataFrame(), "Hata: Veri formatı beklenildiği gibi değil."
        
        # Verileri DataFrame'e dönüştür ve sırala
        df = pd.DataFrame(data)
        if 'totalCiro' in df.columns:
            df = df.sort_values(by="totalCiro", ascending=False).reset_index(drop=True)
            return df, None
        else:
            return pd.DataFrame(), "Hata: Veride 'totalCiro' sütunu bulunamadı."
            
    except requests.exceptions.RequestException as e:
        return pd.DataFrame(), f"Ağ Hatası: Veriler çekilemedi. {e}"
    except ValueError:
        return pd.DataFrame(), "JSON Hatası: Sunucudan gelen yanıt ayrıştırılamadı."

# --------------------------------------------------------------------------------
# Yardımcı Fonksiyonlar ve Ana Arayüz
# --------------------------------------------------------------------------------

def show_branch_details_modal(branch_data):
    """
    Seçilen şubenin detaylarını gösteren bir modal pencere oluşturur.
    """
    modal = st.modal(f"Şube Detayları: {branch_data.get('branch', 'N/A')}")
    with modal:
        ciro = branch_data.get('totalCiro', 0)
        sales_count = branch_data.get('successfulSalesCount', 0)
        call_count = branch_data.get('totalCalls', 0)
        sale_rate = branch_data.get('saleRate', 0)
        avg_ciro = branch_data.get('averageCiro', 0)

        st.markdown(f"**Toplam Ciro:** {ciro:,.2f} TL")
        st.markdown(f"**Başarılı Satış Sayısı:** {sales_count} Adet")
        st.markdown(f"**Toplam Arama Sayısı:** {call_count} Adet")
        st.markdown(f"**Başarılı Satış Oranı:** {sale_rate}%")
        st.markdown(f"**Ortalama Satış Cirosu:** {avg_ciro:,.2f} TL")

# --- ANA UYGULAMA ---

local_css()

# Logo ve Başlık
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(
        "https://static.ticimax.cloud/32769/uploads/editoruploads/hedef-image/logo.png",
        use_column_width=True
    )
st.title("Satış Liderlik Tablosu")

# Filtreleme Kontrolleri
month_names = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
current_year = datetime.now().year
current_month_index = datetime.now().month - 1

filter_cols = st.columns(3)
with filter_cols[0]:
    selected_month_name = st.selectbox("Ay Seçin", month_names, index=current_month_index)
with filter_cols[1]:
    selected_year = st.selectbox("Yıl Seçin", range(current_year, current_year - 5, -1))
with filter_cols[2]:
    st.write("") # Boşluk için
    st.write("") # Boşluk için
    apply_filter = st.button("Filtrele", use_container_width=True)

# Seçilen ayın sayısal değerini bul
selected_month_index = month_names.index(selected_month_name)

# Verileri çek ve göster
with st.spinner('Liderlik tablosu verileri yükleniyor...'):
    df, error_message = fetch_leaderboard_data(selected_month_index, selected_year)

if error_message:
    st.error(error_message)
elif df.empty:
    st.warning("Seçili dönem için veri bulunamadı.")
else:
    st.success(f"**{selected_month_name} {selected_year}** dönemi verileri başarıyla yüklendi.")
    
    # TOP 3 ŞUBELERİ GÖSTER
    st.header("🏆 Ayın Liderleri 🏆")
    top_3 = df.head(3)
    top_3_cols = st.columns(3)

    rank_map = {0: 2, 1: 1, 2: 3} # 2., 1., 3. olarak sıralamak için
    
    # Kartları oluştururken kullanılacak sıra
    display_order = [1, 0, 2] # 2. kart, 1. kart, 3. kart

    for i, col_index in enumerate(display_order):
        if i < len(top_3):
            branch_data = top_3.iloc[i]
            rank = i + 1
            
            # Kart CSS sınıfını belirle
            if rank == 1:
                card_class = "rank-1-card"
                icon = '<i class="fa-solid fa-crown crown-icon"></i>'
            elif rank == 2:
                card_class = "rank-2-card"
                icon = '<i class="fa-solid fa-medal crown-icon"></i>'
            else:
                card_class = "rank-3-card"
                icon = '<i class="fa-solid fa-award crown-icon"></i>'

            with top_3_cols[col_index]:
                 # Kartın tüm içeriğini tek bir container'a alıp, ona özel class atıyoruz.
                with st.container():
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    st.markdown(f'<span class="card-rank-badge">{rank}</span>', unsafe_allow_html=True)
                    st.markdown(icon, unsafe_allow_html=True)
                    st.markdown(f"<div class='card-name'>{branch_data['branch']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card-score'>{branch_data['totalCiro']:,.2f} TL</div>", unsafe_allow_html=True)
                    
                    if st.button("Detayları Gör", key=f"details_{rank}"):
                        show_branch_details_modal(branch_data)
                    st.markdown('</div>', unsafe_allow_html=True)


    st.header("Genel Sıralama")
    
    # Grafiği göster
    st.subheader("Şube Ciro Karşılaştırması")
    chart_data = df[['branch', 'totalCiro']].set_index('branch')
    st.bar_chart(chart_data, height=400)

    # Geriye kalan şubelerin tablosunu göster
    st.subheader("Tüm Şubeler")
    remaining_branches = df.copy()
    remaining_branches.index = remaining_branches.index + 1 # Sıralamayı 1'den başlat
    st.dataframe(remaining_branches[['branch', 'totalCiro']].rename(columns={'branch': 'Şube Adı', 'totalCiro': 'Toplam Ciro'}))

    st.info(f"Son veri güncelleme zamanı: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

