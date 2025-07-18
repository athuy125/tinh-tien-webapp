import streamlit as st
import json
import os

st.set_page_config(page_title="Công cụ Tính Tiền & Nợ", layout="centered")

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_data(tu_dien):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(tu_dien, f, ensure_ascii=False, indent=4)

st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ")
tu_dien = load_data()

menu = ["Tính tiền lời", "Tính tiền nhập hàng", "Quản lý nợ"]
choice = st.sidebar.selectbox("Chọn chức năng", menu)

if choice == "Tính tiền lời":
    st.subheader("💰 Tính tiền lời khi bán hàng")
    thung = st.number_input("Số thùng (thùng)", 0, step=1)
    gia_ban = st.number_input("Giá bán / thùng (nghìn)", 0, step=1)
    gia_von = st.number_input("Giá vốn / thùng (nghìn)", 0, step=1)
    if st.button("Tính lợi nhuận"):
        loi = (gia_ban - gia_von) * thung
        st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

elif choice == "Tính tiền nhập hàng":
    st.subheader("📦 Tính tiền cần trả khi nhập hàng")
    thung_nhap = st.number_input("Số thùng nhập", 0, step=1)
    gia_von = st.number_input("Giá vốn / thùng (nghìn)", 0, step=1)
    if st.button("Tính tổng tiền"):
        tong = thung_nhap * gia_von
        st.info(f"Cần trả: **{tong} nghìn đồng**")

elif choice == "Quản lý nợ":
    st.subheader("📝 Quản lý danh sách nợ")
    tab = st.radio("Chọn tác vụ", ["Xem nợ", "Thêm nợ", "Sửa nợ"])
    if tab == "Xem nợ":
        st.write("**Danh sách hiện tại:**")
        if tu_dien:
            st.json(tu_dien)
        else:
            st.info("Chưa có ai nợ.")
    elif tab == "Thêm nợ":
        ten = st.text_input("Tên người nợ")
        so_tien = st.number_input("Số tiền (nghìn đồng)", 0, step=1)
        if st.button("Thêm"):
            tu_dien[ten] = so_tien
            save_data(tu_dien)
            st.success("Đã thêm nợ.")
    else:
        ten = st.selectbox("Chọn người cần sửa", list(tu_dien.keys()))
        so_moi = st.number_input("Số tiền mới (nghìn)", 0, step=1)
        if st.button("Cập nhật"):
            tu_dien[ten] = so_moi
            save_data(tu_dien)
            st.success("Đã cập nhật nợ.")
