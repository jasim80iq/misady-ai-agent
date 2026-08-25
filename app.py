import streamlit as st
import openai
import requests

st.set_page_config(
    page_title="مدير الصفحات الذكي",
    page_icon="🚀",
    layout="centered"
)

# Proper RTL styling for Arabic text alignment
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .stTextInput, .stTextArea {
        direction: rtl;
    }
    input, textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 مدير الصفحات والذكاء الاصطناعي")
st.write("أهلاً بك يا جاسم! أنشئ صور منتجاتك واكتب منشوراتك بكل سهولة.")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.subheader("إعدادات المنظومة")
    openai_api_key = st.text_input("مفتاح الذكاء الاصطناعي", type="password")
    
    st.markdown("---")
    st.subheader("بيانات فيسبوك")
    fb_page_id = st.text_input("معرف الصفحة")
    fb_access_token = st.text_input("رمز التوكن", type="password")
    
    st.info("أدخل مفتاح الذكاء الاصطناعي للبدء.")

# Form
with st.form("form_one"):
    st.subheader("تفاصيل المنتج")
    product_prompt = st.text_area(
        "اكتب وصف المنتج هنا:",
        placeholder="مثلاً: حذاء رياضي شبابي مريح بتصميم عصري..."
    )
    
    submitted = st.form_submit_button("✨ توليد ونشر")

if submitted:
    if not openai_api_key:
        st.error("الرجاء إدخال مفتاح الذكاء الاصطناعي في القائمة الجانبية أولاً.")
    else:
        openai.api_key = openai_api_key
        
        with st.spinner("جاري صياغة المنشور..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت مسوق إلكتروني محترف. اكتب منشور تسويقي باللغة العربية مع إيموجي."},
                        {"role": "user", "content": f"اكتب منشور لـ: {product_prompt}"}
                    ]
                )
                post_caption = response.choices[0].message.content
            except Exception as e:
                post_caption = f"عروض مميزة على {product_prompt}!"

        with st.spinner("جاري توليد الصورة..."):
            try:
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"A professional commercial product photography of: {product_prompt}, studio lighting",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = image_response.data[0].url
            except Exception as e:
                st.error(f"خطأ في توليد الصورة: {e}")
                image_url = None

        if image_url:
            st.success("تم بنجاح!")
            col1, col2 = st.columns(2)
            with col1:
                st.image(image_url, caption="الصورة", use_container_width=True)
            with col2:
                st.markdown("### النص:")
                st.info(post_caption)

            if fb_page_id and fb_access_token:
                with st.spinner("جاري النشر على فيسبوك..."):
                    try:
                        url = f"https://graph.facebook.com/v18.0/{fb_page_id}/photos"
                        payload = {'url': image_url, 'caption': post_caption, 'access_token': fb_access_token}
                        fb_res = requests.post(url, data=payload)
                        res_data = fb_res.json()
                        if "id" in res_data:
                            st.success("تم النشر بنجاح على فيسبوك!")
                        else:
                            st.warning(f"تعذر النشر: {res_data.get('error', {}).get('message', 'خطأ')}")
                    except Exception as ex:
                        st.error(f"خطأ اتصال: {ex}")
            else:
                st.info("لم تقم بإدخال بيانات فيسبوك، النتائج معروضة للمراجعة فقط.")
