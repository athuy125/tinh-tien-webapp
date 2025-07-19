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

    elif choice == "💼 Lợi nhuận chuyến xe đầu kéo":
        st.subheader("🚚 Tính lợi nhuận 1 chuyến xe đầu kéo")
        doanh_thu = st.number_input("💰 Doanh thu nhận được (triệu đồng)", 0.0, step=0.1)
        xang_dau = st.number_input("⛽ Chi phí xăng dầu (triệu đồng)", 0.0, step=0.1)
        cau_duong = st.number_input("🛣️ Phí cầu đường (triệu đồng)", 0.0, step=0.1)
        sua_chua = st.number_input("🔧 Phí sửa chữa (triệu đồng)", 0.0, step=0.1)
        cuoc_xe = st.number_input("🚚 Chi phí cước xe / thuê xe (triệu đồng)", 0.0, step=0.1)
        an_uong = st.number_input("🍚 Chi phí ăn uống, sinh hoạt (triệu đồng)", 0.0, step=0.1)
        if st.button("✅ Tính lợi nhuận"):
            tong_cp = xang_dau + cau_duong + sua_chua + cuoc_xe + an_uong
            loi_nhuan = doanh_thu - tong_cp
            st.info(f"👉 **Tổng chi phí:** {tong_cp:.2f} triệu đồng")
            st.success(f"✅ **Lợi nhuận sau chuyến:** {loi_nhuan:.2f} triệu đồng")

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        if tu_dien:
            ten = st.selectbox("👉 Chọn người nợ:", list(tu_dien.keys()))
            if ten:
                st.write(f"**Số nợ hiện tại của {ten}:** {tu_dien[ten]}")
                action = st.radio("Chọn tác vụ", [
                    "➕ Cộng thêm nợ", "✅ Trả bớt nợ", "📦 Tính nợ theo số thùng", "🗑️ Xóa người nợ"
                ])
                if action == "➕ Cộng thêm nợ":
                    them = st.number_input("Số tiền muốn cộng (nghìn đồng)", 0, step=1)
                    if st.button("Cộng thêm"):
                        try: cu = int(str(tu_dien[ten]).split()[0])
                        except: cu = 0
                        moi = cu + them
                        tu_dien[ten] = f"{moi} (Đã nợ {cu} + thêm {them})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới: {moi} nghìn đồng")
                elif action == "✅ Trả bớt nợ":
                    tra = st.number_input("Số tiền muốn trả (nghìn đồng)", 0, step=1)
                    if st.button("Cập nhật sau khi trả"):
                        try: cu = int(str(tu_dien[ten]).split()[0])
                        except: cu = 0
                        moi = max(cu - tra, 0)
                        tu_dien[ten] = f"{moi} (Đã trả {tra} từ {cu})"
                        save_data(tu_dien)
                        st.success(f"✅ Nợ mới: {moi} nghìn đồng")
                elif action == "📦 Tính nợ theo số thùng":
                    sl = st.number_input("Số thùng nợ thêm", 0, step=1)
                    gia = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
                    if st.button("Tính & Cập nhật"):
                        them = sl * gia
                        try: cu = int(str(tu_dien[ten]).split()[0])
                        except: cu = 0
                        moi = cu + them
                        tu_dien[ten] = f"{moi} (Đã nợ {cu} + thêm {them})"
                        save_data(tu_dien)
                        st.success(f"✅ Tổng nợ mới: {moi} nghìn đồng")
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
        if st.button("Thêm"):
            tu_dien[ten_moi] = so_moi
            save_data(tu_dien)
            st.success(f"✅ Đã thêm: {ten_moi}")

    elif choice == "Tính thuế":
        st.subheader("💵 Tính thuế (theo chuẩn Việt Nam 2025)")
        tab = st.radio("Chọn loại thuế", ["TNCN (thu nhập cá nhân)", "Thuế bán hàng"])

        if tab == "TNCN (thu nhập cá nhân)":
            st.caption("📌 Thuế TNCN tính theo biểu thuế lũy tiến từng phần (có giảm trừ) – theo Thư viện Pháp luật 2025.")
            luong = st.number_input("Tổng thu nhập/tháng (triệu đồng)", 0.0)
            if st.button("Tính thuế TNCN"):
                # Theo quy định: tính phần lũy tiến từng phần
                bac = [5, 10, 18, 32, 52, 80]
                ty_le = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
                so_tien = [0]+bac+[luong]
                thue = 0
                for i in range(len(bac)+1):
                    if luong > so_tien[i]:
                        thue_phan = min(luong, so_tien[i+1]) - so_tien[i]
                        thue += thue_phan * ty_le[i]
                thu_nhap_con_lai = luong - thue
                st.info(f"✅ Tiền thuế phải nộp: **{thue:.2f} triệu**")
                st.success(f"👉 Thu nhập còn lại sau thuế: **{thu_nhap_con_lai:.2f} triệu**")

        elif tab == "Thuế bán hàng":
            doanhthu = st.number_input("Doanh thu bán hàng (triệu đồng)", 0.0)
            st.caption("📌 Thuế GTGT áp dụng: 10% theo quy định chung.")
            thue_gtgt = doanhthu * 0.10
            st.info(f"✅ Thuế GTGT cần nộp: **{thue_gtgt:.2f} triệu đồng**")
else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")







