import streamlit as st
import os
import json

st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi", layout="centered")

# CSS: background đẹp
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

    # ✅ Nếu là VIP thì hiển thị ở đầu
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

    # --- Các chức năng khác giữ nguyên (bạn copy phần cũ của bạn vào đây) ---

    elif choice == "🌟 Thông tin VIP & Thanh toán":
        st.subheader("🌟 Thông tin tài khoản & Đăng ký VIP")
        st.info("Khi bạn chuyển khoản, tài khoản của bạn sẽ được nâng cấp thành VIP!")

        st.markdown("""
        **🏦 Ngân hàng:** Vietcombank  
        **👤 Chủ tài khoản:** Nguyễn Văn A  
        **💳 Số tài khoản:** 0123456789  
        **💰 Nội dung chuyển khoản:** VIP + [Tên bạn]
        """)

        st.markdown("---")
        st.caption("📌 Sau khi chuyển khoản, hãy bấm nút bên dưới để xác nhận bạn đã trở thành VIP.")

        vip_amount = st.number_input("Nhập số tiền bạn đã chuyển khoản (nghìn đồng)", 0, step=1)
        if st.button("✅ Tôi đã chuyển khoản, nâng cấp VIP"):
            if vip_amount > 0:
                tu_dien["is_vip"] = True
                tu_dien["vip_amount"] = vip_amount
                save_data(tu_dien)
                st.success("🌟 Bạn đã trở thành thành viên VIP! 🌟")
            else:
                st.warning("⚠️ Vui lòng nhập số tiền > 0!")

        # Hiển thị thông tin VIP của tài khoản hiện tại
        if tu_dien.get("is_vip"):
            st.info(f"✅ Bạn là VIP. Số tiền đã chuyển khoản: {tu_dien.get('vip_amount', 0)} nghìn đồng.")

else:
    st.info("👉 Vui lòng nhập tên để bắt đầu.")

