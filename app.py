import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Kişisel Finans ve Bütçe Yönetimi",
    page_icon="💸",
    initial_sidebar_state="expanded"
)

st.title(":green[Kişisel Finans ve Bütçe Yönetimi]")
st.write("Gelir ve giderlerinizi takip edin, bütçenizi yönetin.")
st.header("Gelir ve Gider Ekle")

# Gelir ekleme formu
with st.form("gelir_formu"):
    st.write("Gelir Ekle")
    gelir_kaynak = st.selectbox("Gelir Kaynağı Seçiniz:", ["Maaş", "Kira", "Diğer"])
    gelir_miktar = st.number_input("Gelir Miktarı", min_value=0)
    gelir_tarih = st.date_input("Gelir Tarihi")
    gelir_submit = st.form_submit_button("Gelir Ekle")

    if gelir_submit:
        st.session_state.gelir_listesi = st.session_state.get("gelir_listesi", [])
        st.session_state.gelir_listesi.append({"Kaynak": gelir_kaynak, "Miktar": gelir_miktar, "Tarih": gelir_tarih})
        st.success("Gelir başarıyla eklendi!")

# Gider ekleme formu
with st.form("gider_formu"):
    st.write("Gider Ekle")
    gider_kategori = st.selectbox("Gider Seçiniz:", ["Gıda", "Eğlence", "Alışveriş", "Seyahat", "Diğer"])
    gider_miktar = st.number_input("Gider Miktarı", min_value=0)
    gider_tarih = st.date_input("Gider Tarihi")
    gider_submit = st.form_submit_button("Gider Ekle")

    if gider_submit:
        st.session_state.gider_listesi = st.session_state.get("gider_listesi", [])
        st.session_state.gider_listesi.append(
            {"Kategori": gider_kategori, "Miktar": gider_miktar, "Tarih": gider_tarih})
        st.success("Gider başarıyla eklendi!")

# Gelir ve gider verilerini gösterme
st.header("Gelir ve Gider Verileri")

if "gelir_listesi" in st.session_state:
    st.subheader("Gelirler")
    df_gelir = pd.DataFrame(st.session_state.gelir_listesi)
    st.table(df_gelir)
else:
    st.info("Henüz gelir eklenmedi.")

if "gider_listesi" in st.session_state:
    st.subheader("Giderler")
    df_gider = pd.DataFrame(st.session_state.gider_listesi)
    st.table(df_gider)
else:
    st.info("Henüz gider eklenmedi.")

# Gelir ve gider analizi
st.header("Gelir ve Gider Analizi")

if "gelir_listesi" in st.session_state and "gider_listesi" in st.session_state:
    df_gelir = pd.DataFrame(st.session_state.gelir_listesi)
    df_gider = pd.DataFrame(st.session_state.gider_listesi)

    if not df_gelir.empty and not df_gider.empty:
        # Gelir ve gider verilerini birleştir
        df_gelir["Tarih"] = pd.to_datetime(df_gelir["Tarih"])
        df_gider["Tarih"] = pd.to_datetime(df_gider["Tarih"])

        # Gelir ve gider miktarlarını birleştir
        df_gelir["Tür"] = "Gelir"
        df_gider["Tür"] = "Gider"
        df = pd.concat([df_gelir, df_gider])

        # Toplam gelir ve gider hesapla
        toplam_gelir = df_gelir["Miktar"].sum()
        toplam_gider = df_gider["Miktar"].sum()

        # Pasta grafiği için veri hazırla
        labels = ["Gelir", "Gider"]
        sizes = [toplam_gelir, toplam_gider]
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)  # Pencere dışına çıkar

        # Pasta grafiği oluştur
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Daireyi daire olarak görüntüle
        plt.title("Toplam Gelir ve Gider Dağılımı")
        st.pyplot(fig1)
    else:
        st.info("Gelir veya gider verisi bulunamadı.")


