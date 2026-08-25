import streamlit as st
import requests
import replicate

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات والصور باستخدام Gemini و Replicate")

# الشريط الجانبي للمفاتيح
with st.sidebar:
    st.header("مفاتيح API")
    gemini_key = st.text_input("Gemini API Key (المجاني)", type="password")
    replicate_key = st.text_input("Replicate API Token", type="password")

# مدخل النص
prompt_input = st.text_area("وصف المنتج أو الفكرة بالعربي:")

if st.button("توليد الصورة والبوست"):
    if not gemini_key or not replicate_key:
        st.error("يرجى إدخال مفتاحي Gemini و Replicate بالشريط الجانبي أولاً!")
    else:
        # 1. توليد النص باستخدام Gemini المجاني
        with st.spinner("جاري كتابة المنشور..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
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
                    st.error("تأكد من صحة مفتاح Gemini")
            except Exception as e:
                st.error(f"خطأ في توليد النص: {e}")

        # 2. توليد الصورة باستخدام Replicate
        with st.spinner("جاري تصميم الصورة..."):
            try:
                client = replicate.Client(api_token=replicate_key)
                output = client.run(
                    "black-forest-labs/flux-schnell",
                    input={"prompt": prompt_input}
                )
                st.subheader("🖼️ الصورة:")
                st.image(output[0] if isinstance(output, list) else output)
            except Exception as e:
                st.error(f"خطأ في توليد الصورة: {e}")
