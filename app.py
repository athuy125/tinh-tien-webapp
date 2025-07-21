import zipfile
import requests
import streamlit as st
import os
import json
from docx import Document
import streamlit as st

# Thêm PWA header
st.markdown("""
<link rel="manifest" href="/https://yourdomain.com/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(function(reg) { console.log('✅ Service Worker đăng ký thành công:', reg); })
      .catch(function(err) { console.log('⚠️ Service Worker lỗi:', err); });
  }
</script>
""", unsafe_allow_html=True)
st.set_page_config(page_title="📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi ", layout="centered")

# CSS nền
st.markdown("""
<style>
/* Toàn bộ nền */
html, body, [class*="st-"], [class^="st-"] {
    background-color: #1e1e1e !important;
    color: #fdfdfd !important;
}

/* Tiêu đề lớn */
h1, h2, h3 {
    color: #fdfdfd !important;
    text-shadow: 1px 1px 3px black;
}

/* Label, text input, number input, radio label, checkbox label, selectbox label */
label, .css-1cpxqw2, .css-qrbaxs, .css-1offfwp, .css-1bzt06z, .st-bb, .st-cx, .st-eb {
    color: #fdfdfd !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* Text input & number input box nền đậm, chữ sáng */
input, textarea {
    background-color: #333 !important;
    color: #fdfdfd !important;
    border: 1px solid #555 !important;
}

/* Sidebar */
.css-1d391kg, .css-hxt7ib, .css-1d3z3hw {
    background-color: #2b2b2b !important;
    color: #fdfdfd !important;
}

/* Button */
.stButton>button {
    background-color: #444 !important;
    color: #fdfdfd !important;
    font-size: 18px !important;
    border-radius: 8px !important;
}

/* Metric text */
.css-1ht1j8u, .css-1aumxhk {
    color: #fdfdfd !important;
}
</style>
""", unsafe_allow_html=True)



st.title("📦 Công cụ Tính Tiền & Quản Lý Nợ by Huyhihihi ")

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

    # Menu
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
        sl = st.number_input("Số lượng bán", 0, step=1)
        gia_ban = st.number_input("Giá bán / số lượng (nghìn đồng)", 0, step=1)
        gia_von = st.number_input("Giá vốn / số lượng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính lợi nhuận"):
            loi = (gia_ban - gia_von) * sl
            st.success(f"Lợi nhuận: **{loi} nghìn đồng**")

    # Tính tiền nhập hàng
    elif choice == "Tính tiền nhập hàng":
        st.subheader("📦 Tính tiền cần trả khi nhập hàng")
        sl = st.number_input("Số lượng nhập", 0, step=1)
        gia_von = st.number_input("Giá vốn / số lượng (nghìn đồng)", 0, step=1)
        if st.button("✅ Tính tổng tiền"):
            tong = sl * gia_von
            st.info(f"Cần trả: **{tong} nghìn đồng**")

    # Lợi nhuận xe đầu kéo
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
        list_no = {k:v for k,v in data.items() if k not in ["is_vip","vip_amount"]}
        if list_no:
            ten = st.selectbox("👉 Chọn người nợ:", list(list_no.keys()))
            if ten:
                st.write(f"**Số nợ hiện tại của {ten}:** {list_no[ten]}")
                action = st.radio("Chọn tác vụ", [
                    "➕ Cộng thêm nợ", "✅ Trả bớt nợ", "📦 Tính nợ theo số thùng",
                    "✏️ Đổi tên người nợ", "🗑️ Xóa người nợ"
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
        st.subheader("🌟 Đăng ký VIP (LƯU Ý: SAU KHI ĐĂNG KÝ GÓI VIP VUI LÒNG CHÚ Ý ĐIỆN THOẠI, SẼ CÓ NGƯỜI GỌI ĐẾN CUNG CẤP MÃ VIP CHO BẠN, GỌI SỐ 0937481127 nếu muốn liên hệ)")
        st.markdown("""
        **🏦 Ngân hàng:** Techcombank  
        **👤 Chủ tài khoản:** Đỗ Hoàng Gia Huy  
        **💳 Số tài khoản:** 7937481127  
        **💰 Nội dung:** VIP + [Your name] + [phone number]
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

    # Tính thuế
    elif choice == "Tính thuế":
        if is_vip:
            st.subheader("💵 Tính thuế theo quy định 2025")
            tab = st.radio("Chọn loại thuế", ["TNCN (tiền lương)", "Thuế kinh doanh", "Thuế bán hàng (GTGT)"])
            if tab == "TNCN (tiền lương)":
                luong = st.number_input("Tổng thu nhập (triệu đồng/tháng)", 0.0, step=0.1)
                phu_thuoc = st.number_input("Số người phụ thuộc", 0, step=1)
                hop_dong = st.checkbox("Hợp đồng ≥3 tháng?", value=True)
                if st.button("✅ Tính"):
                    giam_tru = 11 + phu_thuoc * 4.4
                    tntt = max(luong - giam_tru, 0)
                    if not hop_dong:
                        thue = luong * 0.10
                        pp = "Khấu trừ 10%"
                    else:
                        t = tntt
                        if t<=0: thue=0
                        elif t<=5: thue=0.05*t
                        elif t<=10: thue=0.10*t-0.25
                        elif t<=18: thue=0.15*t-0.75
                        elif t<=32: thue=0.20*t-1.65
                        elif t<=52: thue=0.25*t-3.25
                        elif t<=80: thue=0.30*t-5.85
                        else: thue=0.35*t-9.85
                        pp = "Biểu thuế lũy tiến"
                    con_lai= luong - thue
                    st.info(f"TNTT: {tntt:.2f} triệu ({pp})")
                    st.success(f"Thuế: {thue:.2f} triệu | Sau thuế: {con_lai:.2f} triệu")
            elif tab=="Thuế kinh doanh":
                dt = st.number_input("Doanh thu năm (triệu)",0.0,step=0.1)
                if st.button("Tính"):
                    thue_gtgt=dt*0.10; thue_tncn=dt*0.01
                    st.success(f"GTGT: {thue_gtgt:.2f} | TNCN: {thue_tncn:.2f} | Tổng: {thue_gtgt+thue_tncn:.2f}")
            else:
                dt = st.number_input("Doanh thu bán hàng (triệu)",0.0,step=0.1)
                if st.button("Tính"):
                    thue=dt*0.10
                    st.success(f"Thuế GTGT: {thue:.2f} triệu")
        else:
            st.warning("🌟 Vui lòng nâng cấp VIP để dùng tính năng này!")

    # Thống kê & Xuất
    elif choice=="📊 Thống kê & Xuất dữ liệu":
        if is_vip:
            list_no={k:v for k,v in data.items() if k not in ["is_vip","vip_amount"]}
            tong_no=sum(int(str(v).split()[0]) for v in list_no.values() if str(v).split()[0].isdigit())
            st.metric("Số người nợ",len(list_no))
            st.metric("Tổng nợ (nghìn)",tong_no)
            if st.button("📥 Xuất JSON"):
                st.download_button("Tải JSON", json.dumps(data,ensure_ascii=False,indent=4), file_name=f"{username}_data.json")
            if st.button("📥 Xuất Word"):
                doc=Document(); doc.add_heading(f"Dữ liệu của {username}",0)
                for k,v in data.items(): doc.add_paragraph(f"{k}: {v}")
                tmp="temp.docx"; doc.save(tmp)
                with open(tmp,"rb") as f:
                    st.download_button("Tải Word",f, file_name=f"{username}_data.docx")
        else:
            st.warning("🌟 Vui lòng nâng cấp VIP để dùng tính năng này!")
else:
    st.info("👉 Nhập tên để bắt đầu.")








