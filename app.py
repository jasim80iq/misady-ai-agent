import streamlit as st
import anthropic
import requests

st.set_page_config(page_title="AI Page Manager - Claude + Hunyuan", layout="centered")

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات والصورة باستخدام Claude للكبشن و Hunyuan للصور.")

# الشريط الجانبي للمفاتيح
with st.sidebar:
    st.header("إعدادات المفاتيح (API Keys)")
    anthropic_api_key = st.text_input("Claude (Anthropic) API Key", type="password", placeholder="sk-ant-...")
    replicate_api_key = st.text_input("Hunyuan (Replicate) API Token", type="password", placeholder="r8_...")

# نموذج الإدخال
with st.form("my_form"):
    user_prompt = st.text_area("وصف المنتج أو الفكرة بالعربي:", "حذاء جلدي فاخر بتصميم عصري وأنيق...")
    submit = st.form_submit_button("توليد الصورة والبوست")

if submit:
    if not anthropic_api_key or not replicate_api_key:
        st.error("يرجى إدخال مفتاح Claude ومفتاح Replicate/Hunyuan من القائمة الجانبية أولاً.")
    else:
        # 1. توليد المنشور والـ Prompt الإنجليزي باستخدام Claude
        with st.spinner("جاري كتابة المنشور العربي وتحضير الوصف بواسطة Claude..."):
            try:
                client_anthropic = anthropic.Anthropic(api_key=anthropic_api_key)
                
                # طلب الكبشن والوصف من كلاود
                msg = client_anthropic.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""اكتب منشور تسويقي جذاب بالعربي مع هشتاغات للمنتج التالي: {user_prompt}
                            ثم اذكر لي في السطر الأخير ترجمة دقيقة ومفصلة باللغة الإنجليزية لوصف الصورة ليتم إرسالها لمولد الصور.
                            اجعل السطر الأخير يفتح بـ PROMPT_EN: """
                        }
                    ]
                )
                
                full_text = msg.content[0].text
                
                # فصل الكبشن عن وصف الصورة الإنجليزي
                if "PROMPT_EN:" in full_text:
                    caption, english_prompt = full_text.split("PROMPT_EN:")
                else:
                    caption = full_text
                    english_prompt = "A high quality commercial studio product photograph of " + user_prompt
                    
            except Exception as e:
                st.error(f"خطأ في Claude: {e}")
                caption = None
                english_prompt = None

        # 2. توليد الصورة باستخدام نموذج Hunyuan (عبر Replicate API)
        if caption and english_prompt:
            st.info(caption.strip())
            
            with st.spinner("جاري رسم الصورة بواسطة نموذج Hunyuan (HY3)..."):
                try:
                    headers = {
                        "Authorization": f"Token {replicate_api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    # استدعاء نموذج Hunyuan-DiT على Replicate
                    payload = {
                        "version": "tencent/hunyuan-dit", 
                        "input": {
                            "prompt": english_prompt.strip(),
                            "width": 1024,
                            "height": 1024
                        }
                    }
                    
                    # إرسال طلب التوليد
                    res = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json={
                        "version": "920e140675750f7e5e4965b0e51786576b53a473e6a928ef231d683050c82270", # Hunyuan-DiT model hash
                        "input": {"prompt": english_prompt.strip()}
                    })
                    
                    response_json = res.json()
                    
                    if "urls" in response_json:
                        get_url = response_json["urls"]["get"]
                        # الانتظار لحين اكتمال الصورة
                        import time
                        status = "processing"
                        while status not in ["succeeded", "failed"]:
                            time.sleep(2)
                            check_res = requests.get(get_url, headers=headers).json()
                            status = check_res.get("status")
                            if status == "succeeded":
                                img_url = check_res["output"][0]
                                st.image(img_url, caption="صورة مولدة بواسطة Hunyuan", use_container_width=True)
                                st.success("تم التوليد بنجاح وبأعلى دقة!")
                                break
                            elif status == "failed":
                                st.error("فشل توليد الصورة من Hunyuan.")
                                break
                    else:
                        st.error(f"خطأ في الاتصال بـ Hunyuan: {response_json.get('detail', 'يرجى التأكد من التوكن')}")
                        
                except Exception as ex:
                    st.error(f"خطأ غير متوقع: {ex}")
