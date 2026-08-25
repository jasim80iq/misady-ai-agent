import streamlit as st
import requests
import urllib.parse

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات والصور (مجاني 100%)")

# الشريط الجانبي للمفاتيح
with st.sidebar:
    st.header("إعدادات API")
    gemini_key = st.text_input("Gemini API Key", type="password")

# مدخل النص
prompt_input = st.text_area("وصف المنتج أو الفكرة بالعربي:")

if st.button("توليد الصورة والبوست"):
    if not gemini_key:
        st.error("يرجى إدخال مفتاح Gemini في الشريط الجانبي أولاً!")
    else:
        # 1. توليد وعرض الصورة أولاً لتظهر مباشرة
        with st.spinner("جاري تصميم الصورة..."):
            try:
                encoded_prompt = urllib.parse.quote(prompt_input)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                st.subheader("🖼️ الصورة:")
                st.image(image_url)
            except Exception as e:
                st.error(f"خطأ في توليد الصورة: {e}")

        # 2. توليد وعرض المنشور النصي بعدها
        with st.spinner("جاري كتابة المنشور..."):
            try:
                clean_key = gemini_key.strip()
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={clean_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"اكتب منشور إعلاني احترافي وجذاب للسوشيال ميديا باللغة العربية مع هاشتاقات وايموجيات عن: {prompt_input}"}]
                    }]
                }
                res = requests.post(url, json=payload, headers=headers).json()
                
                if "candidates" in res:
                    post_text = res["candidates"][0]["content"]["parts"][0]["text"]
                    st.subheader("📝 المنشور:")
                    st.write(post_text)
                elif "error" in res:
                    st.error(f"خطأ من Gemini: {res['error'].get('message', res['error'])}")
                else:
                    st.error(f"استجابة غير متوقعة: {res}")
            except Exception as e:
                st.error(f"خطأ في الاتصال: {e}")
