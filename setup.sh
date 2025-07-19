#!/bin/bash
pip install -r requirements.txt
echo "🔧 Đang cài đặt thư viện từ requirements.txt..."
pip install -r requirements.txt

echo "🚀 Khởi chạy ứng dụng Streamlit..."
streamlit run app.py
