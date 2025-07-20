import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS: nền đẹp
st.markdown("""
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

    def save_data(data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    data = load_data()
    is_vip = data.get("is_vip", False)

    if is_vip:
        st.success(f"🌟 {username}, bạn đang là THÀNH VIÊN VIP! 🌟")

    menu = [
        "Tính tiền lời", 
        "Tính tiền nhập hàng", 
        "Quản lý nợ", 
        "Tính thuế", 
        "💼 Lợi nhuận chuyến xe đầu kéo",
        "🌟 Thông tin VIP & Thanh toán",
        "📊 Thống kê & Xuất dữ liệu"
    ]

    choice = st.sidebar.selectbox("📌 Chọn chức năng", menu)
    st.markdown("<hr style='margin:20px 0'>", unsafe_allow_html=True)

    # Tính tiền lời
    if choice == "Tính tiền lời":
        st.subheader("💰 Tính tiền lời khi bán hàng")
        sl = st.number_input("Số thùng bán", 0, step=1)
        gia_ban = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * sl
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    # Tính tiền nhập hàng
    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        sl = st.number_input("Số thùng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / thùng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính tổng tiền"):
            tong = sl * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    # Lợi nhuận chuyến xe đầu kéo
    elif choice == "💼 Lợi nhuận chuyến xe đầu kéo":
        st.subheader("🚚 Tính lợi nhuận 1 chuyến xe đầu kéo")
        doanh_thu = st.number_input("💰 Doanh thu (triệu đồng)", 0.0, step=0.1)
        xang = st.number_input("⛽ Xăng dầu (triệu đồng)", 0.0, step=0.1)
        cau = st.number_input("🛣️ Phí cầu đường (triệu đồng)", 0.0, step=0.1)
        sua = st.number_input("🔧 Sửa chữa (triệu đồng)", 0.0, step=0.1)
        cuoc = st.number_input("🚚 Cước xe (triệu đồng)", 0.0, step=0.1)
        an = st.number_input("🍚 Ăn uống (triệu đồng)", 0.0, step=0.1)
        if st.button("✅ Tính lợi nhuận"):
            tong_cp = xang + cau + sua + cuoc + an
            loi_nhuan = doanh_thu - tong_cp
            st.info(f"👉 **Tổng chi phí:** {tong_cp:.2f} triệu")
            st.success(f"✅ **Lợi nhuận:** {loi_nhuan:.2f} triệu")

    # Tính thuế
    elif choice == "Tính thuế":
        if is_vip:
            st.subheader("💵 Tính thuế theo quy định năm 2025")
            tab = st.radio("Chọn loại thuế", [
                "TNCN (tiền lương)", 
                "Thuế định kỳ chuyển khoản cá nhân", 
                "Thuế bán hàng (GTGT)"
            ])

            if tab == "TNCN (tiền lương)":
                luong = st.number_input("💰 Tổng thu nhập (triệu đồng/tháng)", 0.0, step=0.1)
                phu_thuoc = st.number_input("👨‍👩‍👧‍👦 Số người phụ thuộc", 0, step=1)
                hop_dong = st.checkbox("Hợp đồng lao động ≥3 tháng?", value=True)
                if st.button("✅ Tính thuế TNCN"):
                    giam_tru = 11 + phu_thuoc * 4.4
                    tntt = max(luong - giam_tru, 0)
                    if not hop_dong:
                        thue = luong * 0.10
                        phuong_phap = "Khấu trừ 10%"
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
                        phuong_phap = "Biểu thuế lũy tiến"
                    con_lai = luong - thue
                    st.info(f"TNTT: {tntt:.2f} triệu")
                    st.info(f"Phương pháp: {phuong_phap}")
                    st.success(f"Thuế TNCN: {thue:.2f} triệu")
                    st.success(f"Sau thuế: {con_lai:.2f} triệu")

            elif tab == "Thuế định kỳ chuyển khoản cá nhân":
                kinh_doanh = st.checkbox("Tôi đang kinh doanh, doanh thu năm >100 triệu")
                if kinh_doanh:
                    tong = st.number_input("Tổng doanh thu năm (triệu đồng)", 0.0, step=0.1)
                    if st.button("✅ Tính thuế"):
                        thue_gtgt = tong * 0.10
                        thue_tncn = tong * 0.01
                        st.info(f"Thuế GTGT: {thue_gtgt:.2f} triệu")
                        st.info(f"Thuế TNCN: {thue_tncn:.2f} triệu")
                        st.success(f"Tổng thuế: {(thue_gtgt + thue_tncn):.2f} triệu")
                else:
                    st.info("✅ Không phải nộp thuế nếu không kinh doanh, doanh thu ≤100 triệu/năm.")

            elif tab == "Thuế bán hàng (GTGT)":
                doanhthu = st.number_input("Doanh thu bán hàng (triệu đồng)", 0.0, step=0.1)
                if st.button("✅ Tính thuế GTGT"):
                    st.success(f"Thuế GTGT: {doanhthu * 0.10:.2f} triệu")
        else:
            st.warning("🌟 Vui lòng nâng cấp VIP để sử dụng tính năng này!")

    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        list_no = {k:v for k,v in data.items() if k not in ["is_vip","vip_amount"]}
        if list_no:
            ten = st.selectbox("👉 Chọn người nợ:", list(list_no.keys()))
            if ten:
                st.write(f"**Số nợ hiện tại của {ten}:** {list_no[ten]}")
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
                        try: cu = int(str(list_no[ten]).split()[0])
                        except: cu = 0
                        moi = cu + them
                        data[ten] = f"{moi} (Đã nợ {cu} + thêm {them})"
                        save_data(data)
                        st.success(f"✅ Tổng nợ mới: {moi} nghìn đồng")
                elif action == "✅ Trả bớt nợ":
                    tra = st.number_input("Số tiền muốn trả (nghìn đồng)", 0, step=1)
                    if st.button("Cập nhật sau khi trả"):
                        try: cu = int(str(list_no[ten]).split()[0])
                        except: cu = 0
                        moi = max(cu - tra, 0)
                        data[ten] = f"{moi} (Đã trả {tra} từ {cu})"
                        save_data(data)
                        st.success(f"✅ Nợ mới: {moi} nghìn đồng")
                elif action == "📦 Tính nợ theo số thùng":
                    sl = st.number_input("Số thùng nợ thêm", 0, step=1)
                    gia = st.number_input("Giá bán / thùng (nghìn đồng)", 0, step=1)
                    if st.button("Tính & Cập nhật"):
                        them = sl * gia
                        try: cu = int(str(list_no[ten]).split()[0])
                        except: cu = 0
                        moi = cu + them
                        data[ten] = f"{moi} (Đã nợ {cu} + thêm {them})"
                        save_data(data)
                        st.success(f"✅ Tổng nợ mới: {moi} nghìn đồng")
                elif action == "✏️ Đổi tên người nợ":
                    ten_moi = st.text_input("Nhập tên mới")
                    if st.button(f"Đổi tên {ten} → {ten_moi}"):
                        if ten_moi and ten_moi not in data:
                            data[ten_moi] = data.pop(ten)
                            save_data(data)
                            st.success(f"✅ Đã đổi tên {ten} thành {ten_moi}")
                        else:
                            st.error("⚠️ Tên mới bị trống hoặc đã tồn tại!")
                elif action == "🗑️ Xóa người nợ":
                    if st.button(f"Xóa {ten}"):
                        del data[ten]
                        save_data(data)
                        st.success("✅ Đã xóa người nợ")
        else:
            st.info("Danh sách nợ trống.")
        st.markdown("---")
        st.subheader("➕ Thêm người nợ mới")
        ten_moi = st.text_input("Tên người nợ mới")
        so_moi = st.text_input("Số tiền nợ")
        if st.button("Thêm"):
            data[ten_moi] = so_moi
            save_data(data)
            st.success(f"✅ Đã thêm: {ten_moi}")

    # VIP
    elif choice == "🌟 Thông tin VIP & Thanh toán":
        st.subheader("🌟 Đăng ký VIP")
        st.markdown("""
        **🏦 Ngân hàng:** Techcombank  
        **👤 Chủ tài khoản:** Đỗ Hoàng Gia Huy  
        **💳 Số tài khoản:** 7937481127  
        **💰 Nội dung:** VIP + [Tên bạn] + [SĐT]
        """)
        vip_amount = st.number_input("Số tiền đã chuyển (nghìn đồng)", 0, step=1)
        secret_code = st.text_input("Nhập mã bí mật bạn nhận được")
        if st.button("✅ Xác nhận VIP"):
            if secret_code == "521985":
                data["is_vip"] = True
                data["vip_amount"] = vip_amount
                save_data(data)
                st.success("🌟 Chúc mừng! Bạn đã trở thành VIP!")
            else:
                st.warning("⚠️ Mã không đúng, vui lòng kiểm tra.")

    # Thống kê & Xuất dữ liệu
    elif choice == "📊 Thống kê & Xuất dữ liệu":
        if is_vip:
            st.subheader("📊 Thống kê nhanh")
            list_no = {k:v for k,v in data.items() if k not in ["is_vip","vip_amount"]}
            tong_no = sum(int(str(v).split()[0]) for v in list_no.values() if str(v).split()[0].isdigit())
            st.metric("👥 Số người nợ", len(list_no))
            st.metric("💰 Tổng số nợ (nghìn đồng)", tong_no)
            if st.button("📥 Xuất dữ liệu"):
                json_data = json.dumps(data, ensure_ascii=False, indent=4)
                st.download_button("Tải xuống file JSON", json_data, file_name=f"data_{username}.json")
            st.caption("☁️ Gợi ý: tự động backup lên Google Drive (cần cấu hình).")
        else:
            st.warning("🌟 Vui lòng nâng cấp VIP để sử dụng tính năng này!")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")





