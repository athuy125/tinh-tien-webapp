import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi")

# CSS: Thêm background và chỉnh màu, chữ to
st.markdown(
    """
    <style>

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

    menu = ["Tính tiền lời", "Tính tiền nhập hàng", "Quản lý nợ"]
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

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        if tu_dien:
            ten = st.selectbox("👉 Chọn người nợ để quản lý:", list(tu_dien.keys()))
            if ten:
                st.write(f"**Số nợ hiện tại của {ten}:** {tu_dien[ten]}")
                action = st.radio("Chọn tác vụ", [
                    "➕ Cộng thêm nợ",
                    "✅ Trả bớt nợ",
                    "📦 Tính nợ theo số thùng",
                    "🗑️ Xóa người nợ"
                ])

                if action == "➕ Cộng thêm nợ":
                    so_them = st.number_input("Số tiền muốn cộng thêm (nghìn đồng)", 0, step=1)
                    if st.button("Cộng thêm"):
                        try:
                            no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except:
                            no_cu = 0
                        no_moi = no_cu + so_them
                        tu_dien[ten] = f"{no_moi} (Đã nợ {no_cu} + thêm {so_them})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới của {ten}: {no_moi} nghìn đồng")

                elif action == "✅ Trả bớt nợ":
                    so_tra = st.number_input("Nhập số tiền muốn trả bớt (nghìn đồng)", 0, step=1)
                    if st.button("Cập nhật sau khi trả"):
                        try:
                            no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except:
                            no_cu = 0
                        no_moi = max(no_cu - so_tra, 0)
                        tu_dien[ten] = f"{no_moi} (Đã trả {so_tra} từ {no_cu})"
                        save_data(tu_dien)
                        st.success(f"✅ Nợ mới của {ten}: {no_moi} nghìn đồng")

                elif action == "📦 Tính nợ theo số thùng":
                    so_thung = st.number_input("Số thùng nợ thêm", 0, step=1)
                    gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
                    if st.button("Tính & Cập nhật nợ"):
                        so_no_moi = so_thung * gia_ban
                        try:
                            no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except:
                            no_cu = 0
                        tong_no = no_cu + so_no_moi
                        tu_dien[ten] = f"{tong_no} (Đã nợ {no_cu} + thêm {so_no_moi} từ {so_thung} thùng × {gia_ban})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới của {ten}: {tong_no} nghìn đồng")

                elif action == "🗑️ Xóa người nợ":
                    if st.button(f"Xóa {ten} khỏi danh sách nợ"):
                        del tu_dien[ten]
                        save_data(tu_dien)
                        st.success(f"✅ Đã xóa {ten} khỏi danh sách nợ")

        else:
            st.info("Danh sách đang trống, hãy thêm người nợ mới bên dưới.")

        st.markdown("---")
        st.subheader("➕ Thêm người nợ mới")
        ten_moi = st.text_input("Tên người nợ mới")
        so_tien_moi = st.text_input("Số tiền nợ (có thể nhập chữ hoặc số)")
        if st.button("Thêm người nợ"):
            tu_dien[ten_moi] = so_tien_moi
            save_data(tu_dien)
            st.success(f"✅ Đã thêm người nợ mới: {ten_moi}")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu sử dụng ứng dụng.")





