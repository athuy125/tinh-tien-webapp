import streamlit as st
import os
import json

# Thiết lập page
st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS tăng cỡ chữ và giãn dòng
st.markdown("""
    <style>
        h1, h2, h3, h4, h5, h6, .stTextInput label, .stNumberInput label, .stSelectbox label, .stRadio label, .stButton button {
            font-size: 22px !important;
        }
        .stTextInput input, .stNumberInput input {
            font-size: 20px !important;
        }
        .stMarkdown p {
            font-size: 20px !important;
        }
        .stAlert p {
            font-size: 20px !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Nhập tên để tách dữ liệu
username = st.text_input("👉 Nhập tên của bạn để bắt đầu:")

if username:
    filename = f"data_{username}.json"

    # Load data
    def load_data():
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    # Save data
    def save_data(tu_dien):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tu_dien, f, ensure_ascii=False, indent=4)

    tu_dien = load_data()

    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)

    # Menu bên trái
    menu = ["Tính tiền lời", "Tính tiền nhập hàng", "Quản lý nợ"]
    choice = st.sidebar.selectbox("📌 Chọn chức năng", menu)

    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)

    # Tính tiền lời
    if choice == "Tính tiền lời":
        st.subheader("💰 Tính tiền lời khi bán hàng")
        thung = st.number_input("Số thùng bán", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * thung
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    # Tính tiền nhập hàng
    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        thung_nhap = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Tính tổng tiền"):
            tong = thung_nhap * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    # Quản lý nợ
    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        tab = st.radio("Chọn tác vụ", [
            "Xem nợ",
            "Thêm người nợ mới",
            "Thêm nợ (cộng thêm tiền)",
            "Xóa nợ (trả bớt nợ)",
            "Tính nợ theo số thùng",
            "Xóa người nợ"
        ])
        st.markdown("<br>", unsafe_allow_html=True)

        if tab == "Xem nợ":
            st.write("**Danh sách nợ hiện tại:**")
            if tu_dien:
                for ten, so_tien in tu_dien.items():
                    st.write(f"👉 **{ten}** nợ **{so_tien}**")
            else:
                st.info("Chưa có ai nợ.")
            st.markdown("<br>", unsafe_allow_html=True)

        elif tab == "Thêm người nợ mới":
            ten = st.text_input("Tên người nợ")
            so_tien = st.text_input("Số tiền nợ (có thể nhập chữ hoặc số)")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Thêm"):
                tu_dien[ten] = so_tien
                save_data(tu_dien)
                st.success(f"✅ Đã thêm nợ mới cho **{ten}**")
            st.markdown("<br>", unsafe_allow_html=True)

        elif tab == "Thêm nợ (cộng thêm tiền)":
            if tu_dien:
                ten = st.selectbox("Chọn người muốn cộng thêm nợ", list(tu_dien.keys()))
                so_them = st.number_input("Nhập số tiền muốn cộng thêm (nghìn đồng)", 0, step=1)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➕ Cộng thêm nợ"):
                    try:
                        no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                    except:
                        no_cu = 0
                    no_moi = no_cu + so_them
                    tu_dien[ten] = f"{no_moi} (Đã nợ {no_cu} + thêm {so_them})"
                    save_data(tu_dien)
                    st.success(f"✅ Tổng nợ mới của **{ten}**: **{no_moi} nghìn đồng**")
            else:
                st.info("Danh sách đang trống, chưa có ai để cộng thêm nợ.")
            st.markdown("<br>", unsafe_allow_html=True)

        elif tab == "Xóa nợ (trả bớt nợ)":
            if tu_dien:
                ten = st.selectbox("Chọn người muốn trả bớt nợ", list(tu_dien.keys()))
                no_cu_raw = str(tu_dien.get(ten, "0"))
                try:
                    no_cu = int(no_cu_raw.split()[0])
                except:
                    no_cu = 0
                st.write(f"**Số nợ hiện tại của {ten}:** {no_cu} nghìn đồng")
                so_tra = st.number_input("Nhập số tiền muốn trả bớt (nghìn đồng)", 0, step=1)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✅ Cập nhật sau khi trả"):
                    no_moi = max(no_cu - so_tra, 0)
                    tu_dien[ten] = f"{no_moi} (Đã trả {so_tra} từ {no_cu})"
                    save_data(tu_dien)
                    st.success(f"✅ Nợ mới của **{ten}**: **{no_moi} nghìn đồng**")
            else:
                st.info("Chưa có ai nợ để sửa.")
            st.markdown("<br>", unsafe_allow_html=True)

        elif tab == "Tính nợ theo số thùng":
            ten = st.text_input("Tên người nợ")
            so_thung = st.number_input("Số thùng nợ thêm", 0, step=1)
            gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Tính & Cập nhật nợ"):
                so_no_moi = so_thung * gia_ban
                try:
                    no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                except:
                    no_cu = 0
                tong_no = no_cu + so_no_moi
                tu_dien[ten] = f"{tong_no} (Đã nợ {no_cu} + thêm {so_no_moi} từ {so_thung} thùng × {gia_ban})"
                save_data(tu_dien)
                st.success(f"✅ Tổng nợ mới của **{ten}**: **{tong_no} nghìn đồng**")
            st.markdown("<br>", unsafe_allow_html=True)

        elif tab == "Xóa người nợ":
            if tu_dien:
                ten = st.selectbox("Chọn người muốn xóa", list(tu_dien.keys()))
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"🗑️ Xóa {ten} khỏi danh sách nợ"):
                    del tu_dien[ten]
                    save_data(tu_dien)
                    st.success(f"✅ Đã xóa **{ten}** khỏi danh sách nợ.")
            else:
                st.info("Danh sách đang trống, không có ai để xóa.")
            st.markdown("<br>", unsafe_allow_html=True)

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")


