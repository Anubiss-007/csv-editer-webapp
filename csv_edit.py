import streamlit as st
import pandas as pd
from io import StringIO

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="CSV Column Selector & Exporter",
    layout="centered"
)

st.title("✂️ CSV Editor")
st.markdown("1️⃣อัปโหลดไฟล์ CSV ->  2️⃣เลือกคอลัมน์ที่ต้องการ และตั้งชื่อไฟล์  ->  3️⃣กดดาวน์โหลดไฟล์ใหม่")

# ฟังก์ชันสำหรับแปลง DataFrame เป็น CSV String เพื่อดาวน์โหลด
@st.cache_data
def convert_df_to_csv(df):
    # Important: The 'index=False' prevents pandas from writing the DataFrame index to the CSV file.
    # .encode('utf-8') is used to ensure compatibility with Thai/special characters
    return df.to_csv(index=False).encode('utf-8')

# --- ส่วนของการอัปโหลดไฟล์ ---
st.subheader("📌 1.อัปโหลดไฟล์ CSV ของคุณ")
uploaded_file = st.file_uploader("Browse files", type=["csv"], label_visibility="collapsed")


# --- การประมวลผลข้อมูลเมื่อมีการอัปโหลดไฟล์แล้ว ---
if uploaded_file is not None:
    # อ่านไฟล์ CSV ที่อัปโหลดด้วย Pandas
    try:
        # ใช้อ่านไฟล์จาก FileUploader
        df = pd.read_csv(uploaded_file)
        
        st.subheader("📌 2.เลือกคอลัมน์และตั้งค่าไฟล์ส่งออก")

        # 2.1 ส่วนของการเลือกคอลัมน์ (st.multiselect)
        all_columns = df.columns.tolist()
        
        selected_columns = st.multiselect(
            "เลือกคอลัมน์ที่ต้องการเก็บไว้:",
            all_columns,
            default=all_columns # เลือกทั้งหมดเป็นค่าเริ่มต้น
        )
        
        # 2.2 ช่องกรอกชื่อไฟล์ (st.text_input)
        default_filename = f"exported_{uploaded_file.name.replace('.csv', '')}.csv"
        export_filename = st.text_input(
            "ตั้งชื่อไฟล์ CSV สำหรับดาวน์โหลด:", 
            value=default_filename
        )

        st.divider()
        
        if selected_columns:
            # สร้าง DataFrame ใหม่ที่มีเฉพาะคอลัมน์ที่เลือก
            df_selected = df[selected_columns]
            
            st.subheader("ตัวอย่างข้อมูลที่เลือก📊")
            st.dataframe(df_selected)
            
            # --- ส่วนของการดาวน์โหลดไฟล์ ---
            csv_to_download = convert_df_to_csv(df_selected)
            
            st.subheader("📌 3.ดาวน์โหลดไฟล์")
            st.download_button(
                label="คลิกเพื่อดาวน์โหลดไฟล์ CSV",
                data=csv_to_download,
                # ใช้ชื่อไฟล์ที่ผู้ใช้กำหนด
                file_name=export_filename,
                mime='text/csv',
                use_container_width=True,
                help="ไฟล์จะถูกดาวน์โหลดด้วยชื่อที่คุณระบุ",
                type="primary"
            )
        else:
            st.warning("กรุณาเลือกอย่างน้อยหนึ่งคอลัมน์เพื่อดูตัวอย่างและดาวน์โหลด")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")