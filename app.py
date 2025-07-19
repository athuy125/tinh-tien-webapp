import streamlit as st
import json
import os

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi")

# Nhập tên user
username = st.text_input("Nhập tên của bạn để bắt đầu:")

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
        st.subheader("💰 Tính tiền lời khi bán hàng")
        thung = st.number_input("Số thùng bán được", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * thung
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        thung_nhap = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("Tính tổng tiền"):
            tong = thung_nhap * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        tab = st.radio("Chọn tác vụ", ["Xem nợ", "Thêm nợ", "Sửa nợ", "Tính nợ theo số thùng"])

        if tab == "Xem nợ":
            st.write("**Danh sách nợ hiện tại:**")
            if tu_dien:
                for ten, so_tien in tu_dien.items():
                    st.write(f"👉 **{ten}** nợ **{so_tien}**")
            else:
                st.info("Chưa có ai nợ.")

        elif tab == "Thêm nợ":
            ten = st.text_input("Tên người nợ")
            so_tien = st.text_input("Số tiền nợ (có thể nhập chữ hoặc số)")
            if st.button("Thêm"):
                tu_dien[ten] = so_tien
                save_data(tu_dien)
                st.success(f"Đã thêm nợ cho **{ten}**")

        elif tab == "Sửa nợ":
            if tu_dien:
                ten = st.selectbox("Chọn người cần sửa", list(tu_dien.keys()))
                so_moi = st.text_input("Nhập số tiền mới (có thể nhập chữ hoặc số)")
                if st.button("Cập nhật"):
                    tu_dien[ten] = so_moi
                    save_data(tu_dien)
                    st.success(f"Đã cập nhật nợ cho **{ten}**")
            else:
                st.info("Chưa có ai nợ để sửa.")

        elif tab == "Tính nợ theo số thùng":
            ten = st.text_input("Tên người nợ")
            so_thung = st.number_input("Số thùng nợ", 0, step=1)
            gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
            if st.button("Tính & Thêm vào danh sách nợ"):
                so_no = so_thung * gia_ban
                tu_dien[ten] = f"{so_no} (Tính từ {so_thung} thùng × {gia_ban})"
                save_data(tu_dien)
                st.success(f"Đã tính và thêm nợ cho **{ten}**: {so_no} nghìn đồng")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")

