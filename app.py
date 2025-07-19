import streamlit as st
import json
import os

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="wide")

# Thêm background (sử dụng file ảnh bạn gửi)
st.markdown(
    """
    <style>
    .stApp {
        background: url('pngtree-deep-blue-abstract-wallpaper-design-vector-abstract-background-image_442495.jpg');
        background-size: cover;
        background-position: center;
        color: #fff;
    }
    .big-font {
        font-size: 25px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Hiển thị tiêu đề to
st.markdown('<h1 class="big-font">📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi</h1>', unsafe_allow_html=True)

username = st.text_input("Nhập tên của bạn để bắt đầu:", key="username")
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

    menu = ["Tính tiền lời", "Tính tiền nhập hàng", "Quản lý nợ"]
    choice = st.sidebar.selectbox("📌 Chọn chức năng", menu)

    if choice == "Tính tiền lời":
        st.markdown('<h2 class="big-font">💰 Tính tiền lời khi bán hàng</h2>', unsafe_allow_html=True)
        thung = st.number_input("Số thùng", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn)", 0, step=1)
        if st.button("Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * thung
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    elif choice == "Tính tiền nhập hàng":
        st.markdown('<h2 class="big-font">📦 Tính tiền cần trả khi nhập hàng</h2>', unsafe_allow_html=True)
        thung_nhap = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn)", 0, step=1)
        if st.button("Tính tổng tiền"):
            tong = thung_nhap * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    elif choice == "Quản lý nợ":
        st.markdown('<h2 class="big-font">📝 Quản lý danh sách nợ</h2>', unsafe_allow_html=True)
        tab = st.radio("Chọn tác vụ", ["Xem nợ", "Thêm nợ", "Trả bớt nợ", "Tính nợ theo số thùng", "Xóa người nợ"])

        if tab == "Xem nợ":
            if tu_dien:
                for ten, so_tien in tu_dien.items():
                    st.write(f"👉 **{ten}** nợ **{so_tien} nghìn đồng**")
            else:
                st.info("Hiện chưa có ai nợ.")

        elif tab == "Thêm nợ":
            ten = st.text_input("Tên người nợ mới:")
            so_tien = st.number_input("Số tiền nợ thêm (nghìn đồng):", 0, step=1)
            if st.button("Thêm nợ"):
                tu_dien[ten] = tu_dien.get(ten, 0) + so_tien
                save_data(tu_dien)
                st.success(f"Đã thêm nợ: {ten} nợ thêm {so_tien} nghìn đồng.")

        elif tab == "Trả bớt nợ":
            if tu_dien:
                ten = st.selectbox("Chọn người trả bớt nợ:", list(tu_dien.keys()))
                so_tra = st.number_input("Số tiền trả bớt (nghìn đồng):", 0, step=1)
                if st.button("Cập nhật"):
                    tu_dien[ten] = max(tu_dien[ten] - so_tra, 0)
                    save_data(tu_dien)
                    st.success(f"{ten} đã trả bớt {so_tra} nghìn đồng. Số nợ còn lại: {tu_dien[ten]} nghìn đồng.")
            else:
                st.info("Chưa có ai nợ để trả bớt.")

        elif tab == "Tính nợ theo số thùng":
            ten = st.text_input("Tên người nợ:")
            so_thung = st.number_input("Số thùng nợ:", 0, step=1)
            gia_ban = st.number_input("Giá bán / thùng (nghìn đồng):", 0, step=1)
            if st.button("Tính & Cộng thêm"):
                so_no = so_thung * gia_ban
                tu_dien[ten] = tu_dien.get(ten, 0) + so_no
                save_data(tu_dien)
                st.success(f"{ten} nợ thêm {so_no} nghìn đồng (từ {so_thung} thùng × {gia_ban}). Tổng mới: {tu_dien[ten]} nghìn đồng.")

        elif tab == "Xóa người nợ":
            if tu_dien:
                ten = st.selectbox("Chọn người cần xóa:", list(tu_dien.keys()))
                if st.button("Xóa"):
                    del tu_dien[ten]
                    save_data(tu_dien)
                    st.success(f"Đã xóa {ten} khỏi danh sách nợ.")
            else:
                st.info("Chưa có ai nợ để xóa.")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")





