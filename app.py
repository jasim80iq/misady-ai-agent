import streamlit as st
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="مدير الصفحات والخدمة الذكية", page_icon="🚀")

st.title("🚀 مدير الصفحات والخدمة الذكية")
st.caption("مساعدك العراقي الذكي لإدارة الصفحات، خدمة العملاء، وكتابة المحتوى")

st.header("💬 اكتب طلبك أو استفسار الزبون")

# تعليمات النظام لضبط المساعد كـ مدير صفحات
SYSTEM_PROMPT = """
أنت "مدير الصفحات الذكي"، مساعد محترف متخصص في إدارة الصفحات، خدمة العملاء، والتسويق الرقمي.
تتحدث باللهجة العراقية العفوية والمهنية واللطيفة.

مهامك تشمل:
1. كتابة ردود احترافية ولبقة على أسئلة واستفسارات الزبائن.
2. صياغة منشورات تسويقية وإعلانات جذابة لصفحات التواصل الاجتماعي.
3. اقتراح أفكار للستوريات، المنشورات، والخُطط التسويقية.
4. التعامل مع شكاوى الزبائن بحكمة وامتصاص غضبهم.

قواعد مهمة:
- أجب بشكل مباشر وبدون أي مقدمات إنجليزية أو خطوات تفكير داخلية.
- استخدم اللهجة العراقية البسيطة والمهنية.
"""

user_input = st.text_area(
    "مثال: 'اكتبلي رد على زبون يسأل عن السعر' أو 'سويلي منشور إعلاني لمنتج جديد':",
    key="input_text",
    height=150
)

if st.button("تنفيذ الطلب 🚀"):
    if user_input.strip():
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets.")
        else:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            with st.spinner("جاري إعداد الرد..."):
                try:
                    model = genai.GenerativeModel(
                        model_name="gemini-3.6-flash",
                        system_instruction=SYSTEM_PROMPT
                    )
                    
                    response = model.generate_content(user_input)
                    
                    st.markdown("---")
                    st.markdown("### 💡 الرد المقترح:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى كتابة الطلب أولاً.")
