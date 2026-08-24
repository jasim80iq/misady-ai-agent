import streamlit as st
import google.generativeai as genai

st.title("🤖 مدير مزارع")
st.caption("الوكيل العراقي متعدد المهام — الإصدار الأول")

st.header("💬 المساعد العام")

user_input = st.text_area("اكتب طلبك باللهجة العراقية أو العربية:", key="input_text")

if st.button("تنفيذ"):
    if user_input.strip():
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets.")
        else:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            with st.spinner("جاري التفكير..."):
                # البحث عن جميع الموديلات المتاحة في حسابك تلقائياً
                try:
                    available_models = [
                        m.name for m in genai.list_models() 
                        if 'generateContent' in m.supported_generation_methods
                    ]
                except Exception:
                    available_models = []

                # قائمة احتياطية
                fallback_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
                all_models = available_models + [m for m in fallback_models if m not in available_models]

                success = False
                for model_name in all_models:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(user_input)
                        st.markdown("---")
                        st.markdown("### 💡 الإجابة:")
                        st.write(response.text)
                        success = True
                        break
                    except Exception:
                        continue

                if not success:
                    st.error("لم نتمكن من الاتصال بالخدمة. يرجى التأكد من صحة مفتاح الـ API.")
    else:
        st.warning("يرجى كتابة نص قبل الضغط على تنفيذ.")
