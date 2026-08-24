import streamlit as st
import google.generativeai as genai

st.title("🤖 مدير مزارع")
st.caption("الوكيل العراقي متعدد المهام — الإصدار الأول")

st.header("💬 المساعد العام")

# جلب مفتاح الـ API من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets.")

user_input = st.text_area("اكتب طلبك باللهجة العراقية أو العربية:", key="input_text")

if st.button("تنفيذ"):
    if user_input.strip():
        with st.spinner("جاري التفكير..."):
            try:
                response = model.generate_content(user_input)
                st.markdown("---")
                st.markdown("### 💡 الإجابة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى كتابة نص قبل الضغط على تنفيذ.")
