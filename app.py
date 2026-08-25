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
        # 1. توليد النص باستخدام Gemini المجاني
        with st.spinner("جاري كتابة المنشور..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key.strip()}"
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
                else:
                    st.error("تأكد من صحة مفتاح Gemini ونسخه بالكامل")
            except Exception as e:
                st.error(f"خطأ في توليد النص: {e}")

        # 2. توليد الصورة مجاناً وبدون مفتاح (Pollinations)
        with st.spinner("جاري تصميم الصورة..."):
            try:
                encoded_prompt = urllib.parse.quote(prompt_input)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                st.subheader("🖼️ الصورة:")
                st.image(image_url)
            except Exception as e:
                st.error(f"خطأ في توليد الصورة: {e}")
