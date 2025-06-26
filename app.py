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
    html_content = "<html><body><h1>Hata: index.html bulunamadı!</h1></body></html>"
except Exception as e:
    st.error(f"HTML dosyasını okurken bir hata oluştu: {e}")
    html_content = f"<html><body><h1>Hata: {e}</h1></body></html>"

# HTML içeriğini Streamlit'te göster
# height parametresi daha büyük bir değere ayarlandı (örn. 1200 piksel),
# bu sayede içeriğin kırpılması önlenir.
# scrolling=True, içeriğin bu yüksekliği aşması durumunda kaydırma çubuklarını etkinleştirir.
# Streamlit'in varsayılan padding'ini kaldırmak için özel CSS enjekte edebiliriz.
st.markdown("""
    <style>
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
        .reportview-container .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }
        /* Streamlit'in ana div'leri için padding'i sıfırla */
        /* Bu seçiciler Streamlit versiyonlarına göre değişebilir, ancak en yaygın olanları hedefler */
        .css-fg4lnf, .st-emotion-cache-18ni7ap { /* Genel Streamlit konteynerleri */
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin: 0 !important;
        }
        header.st-emotion-cache-c69x0g.e1t1953018, .st-emotion-cache-z5rd0y { /* Streamlit header */
            display: none !important;
            height: 0px !important;
        }
        /* html elementinin scrollbarını gizle, iframe'in kendisi scroll etsin */
        html {
            overflow: hidden !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Yüksekliği artırıldı
components.html(html_content, height=1200, scrolling=True) 

# Streamlit uygulamanızın altında hata ayıklama veya bilgi mesajları gösterebilirsiniz
# st.sidebar.header("Uygulama Bilgisi")
# st.sidebar.write("Bu uygulama, Google Sheets verilerini kullanarak dinamik bir liderlik tablosu görüntüler.")
# st.sidebar.write("Apps Script URL'inizin doğru ve erişilebilir olduğundan emin olun.")
