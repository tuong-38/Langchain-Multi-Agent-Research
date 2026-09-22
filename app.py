import streamlit as st
from src.pipelines.pipelines import run_research_pipeline

# Cấu hình trang
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Tiêu đề giao diện
st.title("🔍 Multi-Agent Research System")
st.caption("Hệ thống nghiên cứu thông minh tự động: Tìm kiếm ➔ Cào dữ liệu ➔ Soạn thảo ➔ Phản biện ➔ Hoàn thiện")

# Thanh bên (Sidebar) cấu hình
with st.sidebar:
    st.header("⚙️ Cấu hình")
    st.info("Hệ thống chạy trên nền tảng LangChain & Google Gemini.")
    st.markdown("---")
    st.markdown("**Quy trình 5 bước:**")
    st.markdown("1. **Search Agent** (Tavily)")
    st.markdown("2. **Reader Agent** (Scraper)")
    st.markdown("3. **Writer Chain** (Draft)")
    st.markdown("4. **Critic Chain** (Review)")
    st.markdown("5. **Rewrite Chain** (Final Polish)")

# Khung nhập chủ đề nghiên cứu
topic = st.text_input(
    "Nhập chủ đề bạn muốn nghiên cứu:",
    placeholder="Ví dụ: Tác động của AI đối với thị trường lao động tại Việt Nam"
)

start_button = st.button("Bắt đầu nghiên cứu", type="primary")

if start_button:
    if not topic.strip():
        st.warning("Vui lòng nhập chủ đề trước khi bắt đầu!")
    else:
        # Vùng chứa tiến trình chạy
        status_box = st.status("Đang khởi tạo các tác tử và thu thập dữ liệu...", expanded=True)
        
        try:
            with status_box:
                st.write("⏳ Đang thực thi toàn bộ pipeline nghiên cứu...")
                # Gọi hàm pipeline đã nâng cấp
                results = run_research_pipeline(topic)
                status_box.update(label="Nghiên cứu hoàn tất thành công!", state="complete", expanded=False)

            # Tab phân loại dữ liệu chi tiết
            tab_final, tab_critic, tab_draft, tab_sources = st.tabs([
                "📄 Báo cáo hoàn chỉnh", 
                "🧐 Đánh giá phản biện (Critic)", 
                "📝 Bản thảo đầu tiên (Draft)", 
                "🌐 Dữ liệu thu thập & Nguồn"
            ])

            with tab_final:
                st.subheader("Báo cáo nghiên cứu hoàn chỉnh")
                st.markdown(results.get("final_report", "Không có nội dung báo cáo."))

            with tab_critic:
                st.subheader("Nhận xét từ Critic Chain")
                st.markdown(results.get("feedback", "Không có dữ liệu phản biện."))

            with tab_draft:
                st.subheader("Bản thảo ban đầu của Writer")
                st.markdown(results.get("report", "Không có dữ liệu bản thảo."))

            with tab_sources:
                st.subheader("Kết quả tìm kiếm & Nội dung bóc tách")
                with st.expander("Kết quả tìm kiếm (Search Agent)"):
                    st.text(results.get("search_results", "Không tìm thấy dữ liệu."))
                with st.expander("Nội dung trang web đã cào (Reader Agent)"):
                    st.text(results.get("scraped_content", "Không có dữ liệu cào."))

        except Exception as e:
            status_box.update(label="Có lỗi xảy ra trong quá trình nghiên cứu!", state="error", expanded=True)
            st.error(f"Chi tiết lỗi: {str(e)}")