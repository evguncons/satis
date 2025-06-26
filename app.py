import streamlit as st
import streamlit.components.v1 as components
import os

# -----------------------------------------------------------------------------
# Sayfa Konfigürasyonu
# -----------------------------------------------------------------------------
# Streamlit sayfasının temel ayarları. Sayfa başlığı, ikonu ve yerleşim düzeni belirlenir.
st.set_page_config(
    page_title="Satış Liderlik Tablosu",
    page_icon="🏆",
    layout="wide"  # HTML içeriğinin tam genişlikte görüntülenmesini sağlar.
)

# -----------------------------------------------------------------------------
# Custom CSS to Remove Padding and Make it Full Screen
# -----------------------------------------------------------------------------
# Bu CSS kodu, Streamlit'in ana konteynerindeki varsayılan kenar boşluklarını
# (padding) kaldırarak HTML içeriğinin tüm ekranı kaplamasını sağlar.
# Bu sayede "çerçeve" görünümü ortadan kalkar.
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HTML Dosyasını Okuma ve Gösterme
# -----------------------------------------------------------------------------
# Bu bölüm, `app.py` ile aynı dizinde bulunan 'index.html' dosyasını bulur,
# içeriğini okur ve Streamlit'in `components.html` özelliğini kullanarak
# ekranda görüntüler.

# HTML dosyasının yolu (app.py ile aynı dizinde olduğu varsayılır)
html_file_path = os.path.join(os.path.dirname(__file__), 'index.html')

try:
    # HTML dosyasını UTF-8 kodlamasıyla oku
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_code = f.read()

    # HTML içeriğini Streamlit bileşeni olarak göster.
    # `height` parametresi, içeriğin dikeyde ne kadar yer kaplayacağını belirler.
    # `scrolling=True`, içerik sığmazsa kaydırma çubuğu eklenmesini sağlar.
    components.html(html_code, height=1200, scrolling=True)

except FileNotFoundError:
    # `index.html` dosyası bulunamazsa kullanıcıya bilgilendirici bir hata mesajı gösterilir.
    st.error(f"HATA: '{html_file_path}' konumunda `index.html` dosyası bulunamadı.")
    st.warning(
        "Lütfen aşağıdaki adımları kontrol edin:\n"
        "1. Canvas'taki HTML kodunun tamamını kopyalayıp `index.html` adıyla kaydettiğinizden emin olun.\n"
        "2. `index.html` dosyasının `app.py` dosyasıyla aynı klasörde olduğundan emin olun."
    )
except Exception as e:
    st.error(f"HTML dosyası okunurken beklenmedik bir hata oluştu: {e}")
