import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Lỗi: Chưa tìm thấy GOOGLE_API_KEY trong file .env!")
    exit(1)

genai.configure(api_key=api_key)

print("🔍 Đang kết nối tới Google API để lấy danh sách mô hình khả dụng...\n")

try:
    available_models = []
    for model in genai.list_models():
        # Lọc các model hỗ trợ tạo văn bản/nội dung
        if "generateContent" in model.supported_generation_methods:
            # Bỏ tiền tố "models/" để lấy tên định dạng truyền vào ChatGoogleGenerativeAI
            name = model.name.replace("models/", "")
            available_models.append((name, model.display_name))

    if available_models:
        print(f"✅ Tìm thấy {len(available_models)} mô hình đang hoạt động:\n")
        print(f"{'Tên truyền vào code (model=...)':<35} | {'Tên hiển thị (Display Name)'}")
        print("-" * 75)
        for name, display_name in available_models:
            print(f"{name:<35} | {display_name}")
    else:
        print("⚠️ Không tìm thấy mô hình nào hỗ trợ generateContent.")

except Exception as e:
    print(f"❌ Có lỗi xảy ra khi kiểm tra: {e}")