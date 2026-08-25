import streamlit as st
import requests
import urllib.parse

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات باللهجة العراقية والصور الواقعية (مجاني 100%)")

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
        
        with st.spinner("جاري تحليل الطلب وتصميم البوست والصورة الواقعية..."):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={clean_key}"
                headers = {"Content-Type": "application/json"}
                
                # توجيه ذكي لشرح التفاصيل البصرية للأكلات والثقافة العراقية
                system_instruction = f"""
                أنت خبير تسويق عراقي ومصمم بصري احترافي. المطلوب منك:
                1. كتابة منشور إعلاني وجذاب للسوشيال ميديا باللهجة العراقية الدقيقة والجميلة جداً مع إيموجيات وهاشتاقات عن: {prompt_input}
                2. صياغة وصف بصري إنجليزي دقيق جداً للصورة (Visual English Prompt) يفهمه الذكاء الاصطناعي الأجنبي.
                ملاحظة مهمة جداً: إذا كان الطلب يتعلق بأكلة شعبية أو عنصر ثفافي عراقي (مثلاً: ثريد بامية، دولمة، مسكوف، كبة)، لا تترجم اسم الأكلة حرفياً، بل اشرح مكوناتها البصرية بالإنجليزية (مثلاً للثريد: authentic traditional Iraqi thareed bamia, rich red tomato stew with tender green okra pods and lamb meat poured over torn flatbread in a wide round metal tray, photorealistic culinary photography).

                اجعل إجابتك مرتبة، وفي السطر الأخير تماماً اكتب الوصف الإنجليزي للصورة مسبوقاً حصراً بهذه الكلمة:
                [IMAGE_PROMPT:] تليها الجملة الإنجليزية التفصيلية.
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
                        english_img_prompt = f"authentic Iraqi dish, {prompt_input}, detailed food photography, photorealistic, 8k"

                    # 1. عرض الصورة باستخدام نموذج FLUX
                    encoded_prompt = urllib.parse.quote(english_img_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                    
                    st.subheader("🖼️ الصورة:")
                    st.image(image_url)

                    # 2. عرض المنشور
                    st.subheader("📝 المنشور (باللهجة العراقية):")
                    st.write(post_text)

                elif "error" in res:
                    st.error(f"خطأ من Gemini: {res['error'].get('message', res['error'])}")
                else:
                    st.error(f"استجابة غير متوقعة: {res}")
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال: {e}")
