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
        st.subheader("💵 Tính thuế thu nhập cá nhân (TNCN) và thuế bán hàng")

        tab_thue = st.radio("Chọn loại thuế", ["TNCN (tiền lương)", "Thuế bán hàng"])

        elif choice == "Tính thuế":
    st.subheader("💵 Tính thuế theo quy định năm 2025")

    tab = st.radio("Chọn loại thuế", ["TNCN (tiền lương)", "Thuế định kỳ chuyển khoản cá nhân", "Thuế bán hàng (GTGT)"])

    if tab == "TNCN (tiền lương)":
        luong = st.number_input("Nhập tổng thu nhập (triệu đồng/tháng)", 0.0, step=0.1)
        phu_thuoc = st.number_input("Số người phụ thuộc", 0, step=1)
        hop_dong = st.checkbox("Hợp đồng ≥3 tháng?")
        if st.button("Tính thuế"):
            giam_tru = 11 + phu_thuoc * 4.4
            tntt = max(luong - giam_tru, 0)
            if not hop_dong:
                thue = luong * 0.10
            else:
                # ứng dụng biểu thuế rút gọn
                t = tntt
                if t <=5: thue = 0.05*t
                elif t<=10: thue = 0.10*t -0.25
                elif t<=18: thue = 0.15*t -0.75
                elif t<=32: thue = 0.20*t -1.65
                elif t<=52: thue = 0.25*t -3.25
                elif t<=80: thue = 0.30*t -5.85
                else: thue = 0.35*t -9.85
            con_lai = luong - thue
            st.info(f"TNTT: {tntt:.2f} triệu"); st.info(f"Thuế TNCN: {thue:.2f} triệu")
            st.success(f"Sau thuế còn lại: {con_lai:.2f} triệu")

    elif tab == "Thuế định kỳ chuyển khoản cá nhân":
        st.markdown("- Nếu chuyển khoản cho vay, tặng, kiều hối,... không phải nộp thuế.")
        st.markdown("- Nếu dùng tài khoản cá nhân **kinh doanh/doanh thu >100 triệu/năm**, phải nộp thuế.")
        st.info("Bạn có hoạt động kinh doanh / nhận chuyển khoản doanh thu hàng năm >100 triệu không?")
        kinh_doanh = st.checkbox("✅ Có")
        if kinh_doanh:
            tong = st.number_input("Tổng doanh thu năm (triệu đồng)", 0.0, step=0.1)
            if st.button("Tính thuế kinh doanh"):
                thue_gtgt = tong * 0.10
                thue_tncn = tong * 0.01  # giả sử tạm tính 1%
                st.success(f"Thuế GTGT: {thue_gtgt:.2f} triệu")
                st.success(f"Thuế TNCN (ước tính): {thue_tncn:.2f} triệu")
        elif tab_thue == "Thuế bán hàng":
            st.markdown("Ví dụ tô bún, phở, tạp hóa,... thường chịu thuế GTGT ~10%")
            hang = st.selectbox("Chọn loại hàng bán", ["Tô bún", "Phở", "Đồ uống", "Tạp hóa", "Khác"])
            gia_ban = st.number_input("Nhập giá bán (nghìn đồng)", 0.0, step=1.0)
            if st.button("Tính thuế GTGT & tiền nhận sau thuế"):
                # Thuế suất mặc định 10%
                thue_gtgt = gia_ban * 0.10
                gia_sau_thue = gia_ban - thue_gtgt
                st.info(f"Thuế GTGT phải nộp: **{thue_gtgt:.0f} nghìn đồng**")
                st.success(f"Số tiền còn lại sau thuế: **{gia_sau_thue:.0f} nghìn đồng**")

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






