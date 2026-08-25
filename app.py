import re
import requests
import streamlit as st
import urllib.parse

st.set_page_config(page_title="AI Page Manager", page_icon="🚀")

st.title("AI Page Manager 🚀")
st.write("توليد منشورات عراقيّة واحترافيّة وصور بدقة عالية (مجاني 100%)")

# الشريط الجانبي للمفاتيح
with st.sidebar:
  st.header("إعدادات API")
  gemini_key = st.text_input(
      "Gemini API Key",
      type="password",
      help="ضع مفتاح Gemini الخاص بك هنا",
  )

# مدخل النص
prompt_input = st.text_area(
    "وصف المنتج أو الفكرة بالعربي:",
    placeholder="مثال: اكتب لي بوست وصورة لثريد بامية عراقي باللحم...",
)

if st.button("توليد الصورة والبوست"):
  if not gemini_key:
    st.error("يرجى إدخال مفتاح Gemini في الشريط الجانبي أولاً!")
  elif not prompt_input.strip():
    st.warning("يرجى كتابة وصف أو فكرة أولاً!")
  else:
    clean_key = gemini_key.strip()

    with st.spinner("جاري تحليل الطلب وتصميم البوست والصورة الواقعية..."):
      try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={clean_key}"
        headers = {"Content-Type": "application/json"}

        # توجيه ذكي ومفصل يفهم الثقافة والأكلات العراقية
        system_prompt = f"""
                أنت خبير تسويق عراقي ومصمم بصري احترافي.
                المطلوب منك:
                1. كتابة منشور إعلاني جذاب باللهجة العراقية البغدادية الأصيلة والجميلة جداً مع إيموجيات وهاشتاقات عن: {prompt_input}
                2. صياغة وصف إنجليزي دقيق ومفصل جداً في سطر واحد لتوليد صورة واقعية سينمائية (Photorealistic food or product photography).
                
                ملاحظة صارمة للأكلات والثقافة العراقية: 
                إذا كان الطلب عن أكلة شعبية (مثل: ثريد، بامية، دولمة، مسكوف، كبة)، اشرح مكوناتها البصرية بالكامل بالإنجليزية في سطر واحد.
                مثال للثريد: authentic traditional Iraqi food thareed bamia, rich red tomato stew with green okra pods and lamb meat poured over flatbread pieces in a metal tray, photorealistic culinary photography, 8k resolution.

                اكتب المنشور العراقي أولاً، وفي آخر سطر تماماً اكتب الكلمة [IMAGE_PROMPT:] وبعدها اكتب الوصف الإنجليزي في سطر واحد فقط.
                """

        payload = {"contents": [{"parts": [{"text": system_prompt}]}]}
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        data = res.json()

        if "candidates" in data:
          text_response = data["candidates"][0]["content"]["parts"][0]["text"]

          # استخراج البوست ووصف الصورة بدقة
          if "[IMAGE_PROMPT:]" in text_response:
            parts = text_response.split("[IMAGE_PROMPT:]")
            post_text = parts[0].strip()
            raw_img_prompt = parts[1].strip()
          else:
            post_text = text_response.strip()
            raw_img_prompt = (
                f"authentic Iraqi style {prompt_input}, photorealistic, 8k"
            )

          # تنظيف الوصف الإنجليزي من الأسطر والرموز الغريبة لضمان عمل الرابط
          clean_img_prompt = re.sub(r"[\r\n]+", " ", raw_img_prompt).strip()
          clean_img_prompt += ", highly detailed photorealistic photography, 8k"

          encoded_prompt = urllib.parse.quote(clean_img_prompt)
          image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"

          # عرض الصورة والبوست
          st.subheader("🖼️ الصورة:")
          st.image(image_url, use_container_width=True)

          st.subheader("📝 المنشور (باللهجة العراقية):")
          st.write(post_text)

        elif "error" in data:
          st.error(
              f"خطأ من Gemini: {data['error'].get('message', str(data['error']))}"
          )
        else:
          st.error("لم يتم استلام استجابة صحيحة من Gemini.")

      except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
