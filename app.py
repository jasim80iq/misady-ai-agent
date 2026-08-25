import streamlit as st
import requests
import urllib.parse

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات (باللهجة العراقية) والصور بدقة عالية (مجاني 100%)")

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
        clean_key = gemini_key.strip()
        
        with st.spinner("جاري كتابة المنشور بالعراقي وتصميم الصورة الاحترافية..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={clean_key}"
                headers = {"Content-Type": "application/json"}
                
                # توجيه دقيق باللهجة العراقية وبدون تخريبط
                system_instruction = f"""
                أنت مسوق إلكتروني محترف. المطلوب منك أمرين:
                1. اكتب منشور إعلاني وجذاب للسوشيال ميديا باللهجة العراقية الدقيقة حصراً (وبدون أي كلام شامي أو فصحى معقدة)، مع إيموجيات وهاشتاقات عن: {prompt_input}
                2. اصنع وصفاً دقيقاً باللغة الإنجليزية حصراً لتوليد صورة واقعية وجميلة تناسب الطلب (Photorealistic, cinematic lighting, 8k, highly detailed).
                
                اجعل إجابتك مرتبة، وفي السطر الأخير تماماً اكتب الوصف الإنجليزي للصورة مسبوقاً حصراً بهذه الكلمة:
                [IMAGE_PROMPT:] تليها الجملة الإنجليزية.
                """
                
                payload = {"contents": [{"parts": [{"text": system_instruction}]}]}
                res = requests.post(url, json=payload, headers=headers).json()
                
                if "candidates" in res:
                    full_text = res["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # فصل النص عن وصف الصورة الإنجليزي
                    if "[IMAGE_PROMPT:]" in full_text:
                        parts = full_text.split("[IMAGE_PROMPT:]")
                        post_text = parts[0].strip()
                        english_img_prompt = parts[1].strip()
                    else:
                        post_text = full_text
                        english_img_prompt = f"Professional photograph, {prompt_input}, 8k resolution, highly detailed"

                    # 1. عرض الصورة باستخدام نموذج FLUX عالي الدقة
                    encoded_prompt = urllib.parse.quote(english_img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                    
                    st.subheader("🖼️ الصورة:")
                    st.image(image_url)

                    # 2. عرض المنشور باللهجة العراقية
                    st.subheader("📝 المنشور (باللهجة العراقية):")
                    st.write(post_text)

                elif "error" in res:
                    st.error(f"خطأ من Gemini: {res['error'].get('message', res['error'])}")
                else:
                    st.error(f"استجابة غير متوقعة: {res}")
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {e}")
