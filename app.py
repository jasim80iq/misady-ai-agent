import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Page Manager", layout="centered")

st.title("AI Page Manager 🚀")
st.write("توليد المنشورات والصور باستخدام Claude و Hunyuan.")

with st.sidebar:
    st.header("إعدادات المفاتيح (API Keys)")
    anthropic_api_key = st.text_input("Claude API Key", type="password", placeholder="sk-ant-...")
    replicate_api_key = st.text_input("Replicate API Token", type="password", placeholder="r8_...")

with st.form("my_form"):
    user_prompt = st.text_area("وصف المنتج أو الفكرة بالعربي:", "حذاء جلدي فاخر بتصميم عصري وأنيق...")
    submit = st.form_submit_button("توليد الصورة والبوست")

if submit:
    if not anthropic_api_key or not replicate_api_key:
        st.error("يرجى إدخال المفاتيح من القائمة الجانبية أولاً.")
    else:
        # 1. الاتصال المباشر بـ Claude
        with st.spinner("جاري كتابة المنشور بواسطة Claude..."):
            try:
                claude_headers = {
                    "x-api-key": anthropic_api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
                claude_payload = {
                    "model": "claude-3-5-sonnet-20240620",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": f"اكتب منشور تسويقي جذاب بالعربي مع هاشتاغات للمنتج: {user_prompt}\nوفي السطر الأخير اكتب ترجمة إنجليزية دقيقة للصورة وتبدأ بـ PROMPT_EN:"
                        }
                    ]
                }
                c_res = requests.post("https://api.anthropic.com/v1/messages", headers=claude_headers, json=claude_payload).json()
                
                if "content" in c_res:
                    full_text = c_res["content"][0]["text"]
                    if "PROMPT_EN:" in full_text:
                        caption, english_prompt = full_text.split("PROMPT_EN:")
                    else:
                        caption = full_text
                        english_prompt = f"A high quality product photo of {user_prompt}"
                else:
                    st.error(f"خطأ من Claude: {c_res.get('error', {}).get('message', 'تأكد من مفتاح Claude')}")
                    caption, english_prompt = None, None
            except Exception as e:
                st.error(f"خطأ اتصال بـ Claude: {e}")
                caption, english_prompt = None, None

        # 2. الاتصال بـ Hunyuan (Replicate)
        if caption and english_prompt:
            st.info(caption.strip())
            with st.spinner("جاري توليد الصورة بواسطة Hunyuan (HY3)..."):
                try:
                    rep_headers = {
                        "Authorization": f"Token {replicate_api_key}",
                        "Content-Type": "application/json"
                    }
                    rep_payload = {
                        "version": "920e140675750f7e5e4965b0e51786576b53a473e6a928ef231d683050c82270",
                        "input": {"prompt": english_prompt.strip()}
                    }
                    res = requests.post("https://api.replicate.com/v1/predictions", headers=rep_headers, json=rep_payload).json()
                    
                    if "urls" in res:
                        get_url = res["urls"]["get"]
                        status = "processing"
                        while status not in ["succeeded", "failed"]:
                            time.sleep(2)
                            check_res = requests.get(get_url, headers=rep_headers).json()
                            status = check_res.get("status")
                            if status == "succeeded":
                                img_url = check_res["output"][0]
                                st.image(img_url, caption="صورة مولدة بواسطة Hunyuan", use_container_width=True)
                                st.success("تم التوليد بنجاح!")
                                break
                            elif status == "failed":
                                st.error("فشل توليد الصورة من Hunyuan.")
                                break
                    else:
                        st.error(f"خطأ من Hunyuan: {res.get('detail', 'تأكد من توكن Replicate')}")
                except Exception as ex:
                    st.error(f"خطأ اتصال بـ Hunyuan: {ex}")
