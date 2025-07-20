import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS: background và font
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
    if tu_dien.get("is_vip"):
        st.success(f"🌟 {username}, bạn đang là THÀNH VIÊN VIP! 🌟")

    menu = [
        "Tính tiền lời", 
        "Tính tiền nhập hàng", 
        "Quản lý nợ", 
        "Tính thuế", 
        "💼 Lợi nhuận chuyến xe đầu kéo",
        "🌟 Thông tin VIP & Thanh toán"
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
    elif choice == "🌟 Thông tin VIP & Thanh toán":
        st.subheader("🌟 Thông tin tài khoản & Đăng ký VIP")
        st.info("Khi bạn chuyển khoản, tài khoản của bạn sẽ được nâng cấp thành VIP!")

        st.markdown("""
        **🏦 Ngân hàng:** Techcombank  
        **👤 Chủ tài khoản:** Đỗ Hoàng Gia Huy  
        **💳 Số tài khoản:** 7937481127  
        **💰 Nội dung chuyển khoản:** VIP + [Tên bạn] + [SĐT]
        """)

        st.markdown("---")
        st.caption("📌 Sau khi chuyển khoản, bạn sẽ nhận được **một mã VIP** từ admin. "
               "Nhập mã đó vào để xác nhận nâng cấp.")

        vip_amount = st.number_input("Nhập số tiền bạn đã chuyển khoản (nghìn đồng)", 0, step=1)
        vip_code_input = st.text_input("🔒 Nhập mã VIP bạn nhận được")

    if st.button("✅ Xác nhận & nâng cấp VIP"):
        CORRECT_VIP_CODE = "521985"  

        if vip_amount <= 0:
            st.warning("⚠️ Vui lòng nhập số tiền > 0!")
        elif vip_code_input.strip() != CORRECT_VIP_CODE:
            st.error("❌ Sai mã VIP! Vui lòng kiểm tra lại.")
        else:
            tu_dien["is_vip"] = True
            tu_dien["vip_amount"] = vip_amount
            tu_dien["vip_code"] = vip_code_input.strip()
            save_data(tu_dien)
            st.success("🌟 Bạn đã trở thành thành viên VIP! 🌟")

    
    if tu_dien.get("is_vip"):
        st.info(f"✅ Bạn là VIP. Số tiền đã chuyển khoản: {tu_dien.get('vip_amount', 0)} nghìn đồng.")

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
                    "➕ Cộng thêm nợ", 
                    "✅ Trả bớt nợ", 
                    "📦 Tính nợ theo số thùng", 
                    "✏️ Đổi tên người nợ",
                    "🗑️ Xóa người nợ"
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
                elif action == "✏️ Đổi tên người nợ":
                    ten_moi = st.text_input("Nhập tên mới")
                    if st.button(f"Đổi tên {ten} → {ten_moi}"):
                        if ten_moi and ten_moi not in tu_dien:
                            tu_dien[ten_moi] = tu_dien.pop(ten)
                            save_data(tu_dien)
                            st.success(f"✅ Đã đổi tên {ten} thành {ten_moi}")
                        else:
                            st.error("⚠️ Tên mới bị trống hoặc đã tồn tại!")
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
        st.subheader("💵 Tính thuế theo quy định năm 2025")

        tab = st.radio("Chọn loại thuế", [
            "TNCN (tiền lương)", 
            "Thuế định kỳ chuyển khoản cá nhân", 
            "Thuế bán hàng (GTGT)"
        ])

        if tab == "TNCN (tiền lương)":
            st.caption("📌 Áp dụng biểu thuế rút gọn mới nhất 2025. "
                       "Giảm trừ bản thân: 11 triệu/tháng; người phụ thuộc: 4.4 triệu/tháng.")
            luong = st.number_input("Tổng thu nhập (triệu đồng/tháng)", 0.0, step=0.1)
            phu_thuoc = st.number_input("Số người phụ thuộc", 0, step=1)
            hop_dong = st.checkbox("Hợp đồng lao động ≥3 tháng?", value=True)

            if st.button("Tính thuế TNCN"):
                giam_tru = 11 + phu_thuoc * 4.4
                tntt = max(luong - giam_tru, 0)

                if not hop_dong:
                    thue = luong * 0.10
                    phuong_phap = "Khấu trừ 10% (lao động thời vụ <3 tháng)"
                else:
                    t = tntt
                    if t <= 0:
                        thue = 0
                    elif t <= 5:
                        thue = 0.05 * t
                    elif t <= 10:
                        thue = 0.10 * t - 0.25
                    elif t <= 18:
                        thue = 0.15 * t - 0.75
                    elif t <= 32:
                        thue = 0.20 * t - 1.65
                    elif t <= 52:
                        thue = 0.25 * t - 3.25
                    elif t <= 80:
                        thue = 0.30 * t - 5.85
                    else:
                        thue = 0.35 * t - 9.85
                    phuong_phap = "Biểu thuế lũy tiến rút gọn"

                con_lai = luong - thue
                st.info(f"✅ TNTT: **{tntt:.2f} triệu**")
                st.info(f"📌 Phương pháp tính: {phuong_phap}")
                st.success(f"💰 Thuế TNCN: **{thue:.2f} triệu**")
                st.success(f"👉 Sau thuế: **{con_lai:.2f} triệu**")

        elif tab == "Thuế định kỳ chuyển khoản cá nhân":
            st.caption("📌 Nếu chỉ chuyển khoản thông thường không phải nộp thuế.\n"
                       "⚠️ Nếu kinh doanh, doanh thu >100 triệu/năm thì phải đóng thuế.")
            kinh_doanh = st.checkbox("✅ Tôi đang kinh doanh, doanh thu năm >100 triệu")

            if kinh_doanh:
                tong = st.number_input("Tổng doanh thu năm (triệu đồng)", 0.0, step=0.1)
                if st.button("Tính thuế kinh doanh"):
                    thue_gtgt = tong * 0.10
                    thue_tncn = tong * 0.01
                    tong_thue = thue_gtgt + thue_tncn
                    st.info(f"Thuế GTGT (10%): **{thue_gtgt:.2f} triệu**")
                    st.info(f"Thuế TNCN (1%): **{thue_tncn:.2f} triệu**")
                    st.success(f"👉 Tổng thuế dự kiến: **{tong_thue:.2f} triệu**")
            else:
                st.info("✅ Không phải nộp thuế nếu không kinh doanh, doanh thu ≤100 triệu/năm.")

        elif tab == "Thuế bán hàng (GTGT)":
            st.caption("📌 Hàng hóa, dịch vụ thường chịu thuế GTGT 10%.")
            doanhthu = st.number_input("Doanh thu bán hàng (triệu đồng)", 0.0, step=0.1)
            if st.button("Tính thuế GTGT"):
                thue_gtgt = doanhthu * 0.10
                st.success(f"✅ Thuế GTGT phải nộp: **{thue_gtgt:.2f} triệu đồng**")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")

