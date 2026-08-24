import streamlit as st
import google.generativeai as genai

st.title("🤖 مدير مزارع")
st.caption("الوكيل العراقي متعدد المهام — الإصدار الأول")

st.header("💬 المساعد العام")

# تعليمات النظام لضمان إجابة مباشرة ونظيفة بالعراقية
SYSTEM_PROMPT = """
أنت "مدير مزارع"، مساعد ذكي يتحدث باللهجة العراقية العفوية والعربية البسيطة.
واجبك الإجابة على سؤال المستخدم مباشرة بشكل محترم ومنظم.
ممنوع نهائياً طباعة أي مسودات أو تفكير داخلي أو نصوص باللغة الإنجليزية. أعطِ الإجابة النهائية فقط.
"""

user_input = st.text_area("اكتب طلبك باللهجة العراقية أو العربية:", key="input_text")

if st.button("تنفيذ"):
    if user_input.strip():
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets.")
        else:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            with st.spinner("جاري التفكير..."):
                try:
                    # جلب الموديلات المتاحة تلقائياً
                    available = [
                        m.name for m in genai.list_models() 
                        if 'generateContent' in m.supported_generation_methods
                    ]
                    
                    # اختيار أفضل موديل متاح
                    chosen_model = next((m for m in available if 'flash' in m), available[0] if available else "gemini-1.5-flash")
                    
                    model = genai.GenerativeModel(
                        model_name=chosen_model,
                        system_instruction=SYSTEM_PROMPT
                    )
                    
                    response = model.generate_content(user_input)
                    
                    st.markdown("---")
                    st.markdown("### 💡 الإجابة:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى كتابة نص قبل الضغط على تنفيذ.")
