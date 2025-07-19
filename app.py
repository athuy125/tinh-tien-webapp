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
        tab = st.radio("Chọn tác vụ", ["Xem nợ", "Thêm nợ", "Sửa nợ", "Tính nợ theo số thùng", "Xóa người nợ"])

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
                no_cu_raw = str(tu_dien.get(ten, "0"))
                try:
                    no_cu = int(no_cu_raw.split()[0])  # lấy số đầu tiên
                except:
                    no_cu = 0
                st.write(f"**Số nợ hiện tại của {ten}:** {no_cu} nghìn đồng")
                so_tra = st.number_input("Nhập số tiền người đó vừa trả (nghìn đồng)", 0, step=1)
                if st.button("Cập nhật sau khi trả"):
                    no_moi = max(no_cu - so_tra, 0)  # tránh âm
                    tu_dien[ten] = f"{no_moi} (Đã trả {so_tra} từ {no_cu})"
                    save_data(tu_dien)
                    st.success(f"Đã cập nhật nợ cho **{ten}**: Nợ mới là **{no_moi} nghìn đồng**")
            else:
                st.info("Chưa có ai nợ để sửa.")

        elif tab == "Tính nợ theo số thùng":
            ten = st.text_input("Tên người nợ")
            so_thung = st.number_input("Số thùng nợ thêm", 0, step=1)
            gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
            if st.button("Tính & Cập nhật nợ"):
                so_no_moi = so_thung * gia_ban  # số nợ mới tính thêm
                try:
            # Nếu người đó đã nợ, cộng thêm
                    no_cu = int(str(tu_dien.get(ten, "0")).split()[0])  # lấy số đầu tiên, phòng trường hợp có chữ
                except:
                    no_cu = 0
                tong_no = no_cu + so_no_moi
                tu_dien[ten] = f"{tong_no} (Đã nợ {no_cu} + thêm {so_no_moi} từ {so_thung} thùng × {gia_ban})"
                save_data(tu_dien)
                st.success(f"Đã tính và cập nhật nợ cho **{ten}**: Tổng nợ mới **{tong_no} nghìn đồng**")
        elif tab == "Xóa người nợ":
            if tu_dien:
                ten = st.selectbox("Chọn người muốn xóa", list(tu_dien.keys()))
            if st.button(f"Xóa {ten} khỏi danh sách nợ"):
                del tu_dien[ten]
                save_data(tu_dien)
                st.success(f"Đã xóa **{ten}** khỏi danh sách nợ.")
        else:
            st.info("Danh sách nợ đang trống, không có ai để xóa.")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")

