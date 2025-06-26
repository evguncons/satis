import streamlit as st
import streamlit.components.v1 as components
import os

# Sayfa düzenini geniş (wide) olarak ayarla
st.set_page_config(layout="wide")

# HTML dosyasının yolu
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

# HTML dosyasını oku
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
except FileNotFoundError:
    st.error(f"Hata: '{html_file_path}' dosyası bulunamadı. Lütfen 'index.html' dosyasının 'app.py' ile aynı klasörde olduğundan emin olun.")
    html_content = "<html><body><h1>Hata: index.html bulunamadı!</h1></body></body></html>"
except Exception as e:
    st.error(f"HTML dosyasını okurken bir hata oluştu: {e}")
    html_content = f"<html><body><h1>Hata: {e}</h1></body></html>"

# Streamlit'in varsayılan padding'ini kaldırmak ve scroll sorununu çözmek için özel CSS enjekte ediyoruz.
st.markdown("""
    <style>
        /* Streamlit'in ana blok konteynerindeki padding'i sıfırla */
        .block-container {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        /* Rapor görünümündeki ana konteyner için de padding'i sıfırla */
        .reportview-container .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        /* Streamlit'in genel ana div'leri için padding'i sıfırla */
        /* Bu seçiciler Streamlit versiyonlarına göre değişebilir, ancak en yaygın olanları hedefler */
        .css-fg4lnf, .st-emotion-cache-18ni7ap { 
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin: 0 !important;
        }
        /* Streamlit'in üst başlığını gizle */
        header.st-emotion-cache-c69x0g.e1t1953018, .st-emotion-cache-z5rd0y { 
            display: none !important;
            height: 0px !important;
        }
        /* HTML içeriğinin (iframe içindeki) kaydırma çubuklarını gizleme kuralını kaldırıyorum */
        /* Bu sayede içerik gerektiğinde kendi içinde kaydırılabilir. */
        /* html {
            overflow: hidden !important;
        } */ /* Bu satır kaldırıldı */
    </style>
    """, unsafe_allow_html=True)

# HTML içeriğini Streamlit'te göster
# height parametresi daha büyük bir değere ayarlandı (örn. 1500 piksel)
# Bu, içeriğin başlangıçta kırpılmasını önler ve mobil kaydırma sorununu iyileştirir.
# scrolling=True, içeriğin bu yüksekliği aşması durumunda kaydırma çubuklarını etkinleştirir.
components.html(html_content, height=1500, scrolling=True) 

# Streamlit uygulamanızın altında hata ayıklama veya bilgi mesajları gösterebilirsiniz
# st.sidebar.header("Uygulama Bilgisi")
# st.sidebar.write("Bu uygulama, Google Sheets verilerini kullanarak dinamik bir liderlik tablosu görüntüler.")
# st.sidebar.write("Apps Script URL'inizin doğru ve erişilebilir olduğundan emin olun.")
