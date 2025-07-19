import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi")

# CSS thêm background
st.markdown(
    """
    <style>
    .stApp {
        background: url('background.jpg');
        background-size: cover;
        background-position: center;
        color: #333333;
    }
    h1 {
        font-size: 36px !important;
        color: #2c3e50;
        text-align: center;
    }
    h2, h3, .stTextInput label, .stNumberInput label, 
    .stSelectbox label, .stRadio label, .stButton button {
        font-size: 22px !important;
        color: #34495e;
    }
    .stTextInput input, .stNumberInput input {
        font-size: 20px !important;
    }
    .stMarkdown p, .stAlert p {
        font-size: 20px !important;
    }
    .stButton button {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

username = st.text_input("👉 Nhập tên của bạn để bắt đầu:")

if username:
    filename = f"data_{username}.json"

    def load_data():
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_data(tu_dien):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tu_dien, f, ensure_ascii=False, indent=4)

    tu_dien = load_data()

    menu = ["Tính tiền lời", "Tính tiền nhập hàng", "Quản lý nợ", "Tính thuế", "Tính chi phí chuyến đi"]
    choice = st.sidebar.selectbox("📌 Chọn chức năng", menu)

    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)

    if choice == "Tính tiền lời":
        st.subheader("💰 Tính tiền lời khi bán hàng")
        thung = st.number_input("Số thùng bán", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * thung
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        thung_nhap = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính tổng tiền"):
            tong = thung_nhap * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    elif choice == "Tính thuế":
        st.subheader("🧾 Tính thuế thu nhập cá nhân")
        luong = st.number_input("Nhập mức lương/tháng (triệu đồng)", 0.0, step=0.1)

        if st.button("📊 Tính thuế"):
            giam_tru = 11  # triệu đồng
            thu_nhap_tinh_thue = max(luong - giam_tru, 0)

            # Hàm tính thuế lũy tiến
            def tinh_thue(thu_nhap):
                bac = [
                    (5, 0.05),
                    (5, 0.10),
                    (8, 0.15),
                    (14, 0.20),
                    (20, 0.25),
                    (28, 0.30),
                    (float('inf'), 0.35)
                ]
                thue = 0
                for muc, ty_le in bac:
                    if thu_nhap > muc:
                        thue += muc * ty_le
                        thu_nhap -= muc
                    else:
                        thue += thu_nhap * ty_le
                        break
                return thue

            so_thue = tinh_thue(thu_nhap_tinh_thue)
            thu_nhap_con_lai = luong - so_thue

            st.success(f"Thu nhập tính thuế: **{thu_nhap_tinh_thue:.2f} triệu đồng**")
            st.info(f"Số thuế phải nộp: **{so_thue:.2f} triệu đồng**")
            st.success(f"Sau thuế còn lại: **{thu_nhap_con_lai:.2f} triệu đồng**")

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        # Phần quản lý nợ cũ giữ nguyên như của bạn
    elif choice == "Tính chi phí chuyến đi":
        st.subheader("🚚 Tính toán lợi nhuận sau một chuyến xe đầu kéo")
    
        thu_duoc = st.number_input("Số tiền thu được từ chuyến hàng (triệu đồng)", 0.0, step=0.1)
        cuoc_xe = st.number_input("Chi phí cước xe / thuê xe (triệu đồng)", 0.0, step=0.1)
        xang_dau = st.number_input("Chi phí xăng dầu (triệu đồng)", 0.0, step=0.1)
        cau_duong = st.number_input("Phí cầu đường, bến bãi (triệu đồng)", 0.0, step=0.1)
        sua_chua = st.number_input("Chi phí sửa chữa, bảo dưỡng phát sinh (triệu đồng)", 0.0, step=0.1)
        an_uong = st.number_input("Chi phí ăn uống, sinh hoạt trên đường (triệu đồng)", 0.0, step=0.1)
   

        if st.button("✅ Tính lợi nhuận chuyến đi"):
            tong_chi_phi = cuoc_xe + xang_dau + cau_duong + sua_chua + an_uong 
            loi_nhuan = thu_duoc - tong_chi_phi
            st.info(f"👉 **Tổng chi phí chuyến đi:** {tong_chi_phi:.2f} triệu đồng")
            st.success(f"✅ **Lợi nhuận thực nhận sau chuyến đi:** {loi_nhuan:.2f} triệu đồng")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")






