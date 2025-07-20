from io import BytesIO
import streamlit as st
import os
import json
from docx import Document


st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS nền đẹp, chữ sáng
st.markdown("""
<style>
.stApp {
    background: url('https://i.imgur.com/L6XG8Pt.jpg');  /* bạn có thể thay URL khác */
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

    # Lợi nhuận chuyến xe
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

    # Quản lý nợ
    elif choice == "Quản lý nợ":
        st.subheader("📝 Quản lý danh sách nợ")
        list_no = {k: v for k, v in data.items() if k not in ["is_vip","vip_amount"]}
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
            st.subheader("📊 Thống kê")
            list_no = {k: v for k, v in data.items() if k not in ["is_vip","vip_amount"]}
            tong_no = sum(int(str(v).split()[0]) for v in list_no.values() if str(v).split()[0].isdigit())
            st.metric("👥 Số người nợ", len(list_no))
            st.metric("💰 Tổng nợ", tong_no)

            if st.button("📥 Xuất JSON"):
                json_data = json.dumps(data, ensure_ascii=False, indent=4)
                st.download_button("Tải JSON", json_data, file_name=f"data_{username}.json")

            if st.button("📄 Xuất Word"):
                doc = Document()
                doc.add_heading('Danh sách nợ', 0)
                doc.add_paragraph(f'Số người nợ: {len(list_no)}')
                doc.add_paragraph(f'Tổng số nợ: {tong_no} nghìn đồng')
                doc.add_heading('Chi tiết:', level=1)
                for ten, so in list_no.items():
                    doc.add_paragraph(f"{ten}: {so}")
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                st.download_button(
                    "Tải file Word",
                    data=buffer,
                    file_name=f"no_{username}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.warning("🌟 Vui lòng nâng cấp VIP để sử dụng tính năng này!")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")







