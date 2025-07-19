import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS: background và font đẹp
st.markdown(
    """
    <style>
    .stApp {
        background: url('pngtree-deep-blue-abstract-wallpaper-design-vector-abstract-background-image_442495.jpg');
        background-size: cover;
        background-position: center;
        color: #f0f0f0;
    }
    h1 { font-size:36px !important; text-align:center; color:#fff; text-shadow:1px 1px 2px black;}
    h2, h3, .stTextInput label, .stNumberInput label, 
    .stSelectbox label, .stRadio label, .stButton button {
        font-size: 20px !important;
        color: #f8f8f8;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi")

username = st.text_input("👉 Nhập tên của bạn để bắt đầu:")

if username:
    filename = f"data_{username}.json"

    def load_data():
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(tu_dien):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tu_dien, f, ensure_ascii=False, indent=4)

    tu_dien = load_data()

    menu = [
        "Tính tiền lời", 
        "Tính tiền nhập hàng", 
        "Quản lý nợ", 
        "Tính thuế", 
        "💼 Lợi nhuận chuyến xe đầu kéo"
    ]
    choice = st.sidebar.selectbox("📌 Chọn chức năng", menu)

    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)

    if choice == "Tính tiền lời":
        st.subheader("💰 Tính tiền lời khi bán hàng")
        sl = st.number_input("Số thùng bán", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * sl
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        sl = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính tổng tiền"):
            tong = sl * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

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

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        if tu_dien:
            ten = st.selectbox("👉 Chọn người nợ để quản lý:", list(tu_dien.keys()))
            if ten:
                st.write(f"**Số nợ hiện tại của {ten}:** {tu_dien[ten]}")
                action = st.radio("Chọn tác vụ", [
                    "➕ Cộng thêm nợ", "✅ Trả bớt nợ", "📦 Tính nợ theo số thùng", "🗑️ Xóa người nợ"
                ])
                if action == "➕ Cộng thêm nợ":
                    so_them = st.number_input("Số tiền muốn cộng thêm (nghìn đồng)", 0, step=1)
                    if st.button("Cộng thêm"):
                        try:
                            no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except: no_cu = 0
                        no_moi = no_cu + so_them
                        tu_dien[ten] = f"{no_moi} (Đã nợ {no_cu} + thêm {so_them})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới: {no_moi} nghìn đồng")
                elif action == "✅ Trả bớt nợ":
                    so_tra = st.number_input("Số tiền muốn trả bớt (nghìn đồng)", 0, step=1)
                    if st.button("Cập nhật sau khi trả"):
                        try:
                            no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except: no_cu = 0
                        no_moi = max(no_cu - so_tra, 0)
                        tu_dien[ten] = f"{no_moi} (Đã trả {so_tra} từ {no_cu})"
                        save_data(tu_dien)
                        st.success(f"✅ Nợ mới: {no_moi} nghìn đồng")
                elif action == "📦 Tính nợ theo số thùng":
                    sl = st.number_input("Số thùng nợ thêm", 0, step=1)
                    gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
                    if st.button("Tính & Cập nhật nợ"):
                        them = sl * gia_ban
                        try: no_cu = int(str(tu_dien.get(ten, "0")).split()[0])
                        except: no_cu = 0
                        tong = no_cu + them
                        tu_dien[ten] = f"{tong} (Đã nợ {no_cu} + thêm {them})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới: {tong} nghìn đồng")
                elif action == "🗑️ Xóa người nợ":
                    if st.button(f"Xóa {ten}"):
                        del tu_dien[ten]
                        save_data(tu_dien)
                        st.success("✅ Đã xóa người nợ")
        else:
            st.info("Danh sách nợ trống.")

        st.markdown("---")
        st.subheader("➕ Thêm người nợ mới")
        ten_moi = st.text_input("Tên người nợ mới")
        so_moi = st.text_input("Số tiền nợ (có thể nhập chữ hoặc số)")
        if st.button("Thêm người nợ"):
            tu_dien[ten_moi] = so_moi
            save_data(tu_dien)
            st.success(f"✅ Đã thêm người nợ: {ten_moi}")

    elif choice == "Tính thuế":
        st.subheader("💵 Tính thuế")
        tab = st.radio("Chọn loại thuế", ["TNCN (tiền lương)", "Thuế bán hàng"])
        if tab == "TNCN (tiền lương)":
            luong = st.number_input("Tổng thu nhập/tháng (triệu đồng)", 0.0)
            if st.button("Tính thuế"):
                if luong <= 5: thue = 0
                elif luong <= 10: thue = luong * 0.05
                elif luong <= 18: thue = luong * 0.1
                elif luong <= 32: thue = luong * 0.15
                elif luong <= 52: thue = luong * 0.2
                elif luong <= 80: thue = luong * 0.25
                else: thue = luong * 0.3
                thu_nhap_con_lai = luong - thue
                st.info(f"Thuế: **{thue} triệu** - Còn lại: **{thu_nhap_con_lai} triệu**")
        elif tab == "Thuế bán hàng":
            doanhthu = st.number_input("Doanh thu bán hàng (triệu đồng)", 0.0)
            thue_gtgt = doanhthu * 0.1  # thuế GTGT 10%
            st.info(f"Thuế GTGT cần đóng: **{thue_gtgt} triệu đồng**")
else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")







