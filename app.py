import streamlit as st
import streamlit.components.v1 as components
import os

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
# height=None, içeriğin yüksekliğine göre otomatik ayarlanmasını sağlar.
# width="100%" parametresi kaldırıldı, Streamlit varsayılan olarak tam genişliği kullanır.
components.html(html_content, height=None, scrolling=True)

# Streamlit uygulamanızın altında hata ayıklama veya bilgi mesajları gösterebilirsiniz
# st.sidebar.header("Uygulama Bilgisi")
# st.sidebar.write("Bu uygulama, Google Sheets verilerini kullanarak dinamik bir liderlik tablosu görüntüler.")
# st.sidebar.write("Apps Script URL'inizin doğru ve erişilebilir olduğundan emin olun.")
