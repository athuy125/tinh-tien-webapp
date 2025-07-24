
import json
from db import save_tinh_toan

# 👉 Đọc dữ liệu cũ từ file local
with open("data/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 👉 Tên người dùng 
username = "nhung ruby"  # ⚡ ĐỔI thành tên người dùng thật 

# 👉 Lấy lịch sử tính toán
history = data.get("history", {})

# 👉 Lặp qua từng mặt hàng
for hang, items in history.items():
    for noi_dung in items:
        save_tinh_toan(username, hang, noi_dung)

print("✅ Toàn bộ lịch sử đã được chuyển lên MongoDB Atlas!")
