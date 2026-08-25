import streamlit as st
import openai
import requests

# Page configuration
st.set_page_config(
    page_title="مدير الصفحات والنشر الآلي",
    page_icon="🚀",
    layout="centered"
)

# Clean CSS to fix vertical text wrapping completely
st.markdown("""
<style>
    /* Force proper Arabic alignment and prevent vertical breaking */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    label, p, span, div, h1, h2, h3, h4 {
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: plaintext;
    }

    /* Modern Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 مدير الصفحات والذكاء الاصطناعي")
st.write("أهلاً بك يا جاسم! أنشئ صور منتجاتك، اكتب منشوراتك، وانشرها بضغطة زر واحدة.")
st.markdown("---")

# Sidebar for Settings (Completely in Arabic to avoid breaking)
with st.sidebar:
    st.header("⚙️ الإعدادات الأساسية")
    openai_api_key = st.text_input("مفتاح الذكاء الاصطناعي (API Key)", type="password", placeholder="أدخل المفتاح هنا")
    
    st.markdown("---")
    st.header("🌐 ربط صفحة فيسبوك")
    fb_page_id = st.text_input("رقم تعريف الصفحة (Page ID)", placeholder="أدخل رقم الصفحة")
    fb_access_token = st.text_input("رمز وصول الصفحة (Access Token)", type="password", placeholder="أدخل الرمز هنا")
    
    st.info("قم بإدخال مفتاح الذكاء الاصطناعي لتفعيل التوليد.")

# Main Form Area
with st.form("publishing_form"):
    st.subheader("📝 تفاصيل المنتج أو المنشور")
    product_prompt = st.text_area(
        "اكتب وصفاً مختصراً للمنتج أو العرض:",
        placeholder="مثلاً: عطر رجالي فخم بتركيبة العود والعنبر..."
    )
    
    submitted = st.form_submit_button("✨ ابدأ توليد المحتوى والنشر الآلي")

if submitted:
    if not openai_api_key:
        st.error("الرجاء إدخال مفتاح الذكاء الاصطناعي في القائمة الجانبية أولاً.")
    else:
        openai.api_key = openai_api_key
        
        # Step 1: Generate Post Text
        with st.spinner("جاري صياغة المنشور التسويقي..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت مسوق إلكتروني محترف تكتب منشورات تسويقية جذابة باللغة العربية مع إيموجي مناسبة."},
                        {"role": "user", "content": f"اكتب منشور تسويقي قصير وجذاب بالاعتماد على هذا الوصف: {product_prompt}"}
                    ]
                )
                post_caption = response.choices[0].message.content
            except Exception as e:
                post_caption = f"عروض مميزة وخصومات رائعة على {product_prompt}! لا تفوت الفرصة."

        # Step 2: Generate Image
        with st.spinner("جاري توليد الصورة بالذكاء الاصطناعي..."):
            try:
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=f"A professional commercial product photography of: {product_prompt}, high resolution, studio lighting, advertising style",
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                image_url = image_response.data[0].url
            except Exception as e:
                st.error(f"حدث خطأ أثناء توليد الصورة: {e}")
                image_url = None

        # Display Results
        if image_url:
            st.success("تم توليد المحتوى والصورة بنجاح!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### الصورة المولّدة:")
                st.image(image_url, use_container_width=True)
            with col2:
                st.markdown("### النص التسويقي:")
                st.info(post_caption)

            # Step 3: Publish to Facebook
            if fb_page_id and fb_access_token:
                with st.spinner("جاري النشر تلقائياً على صفحة فيسبوك..."):
                    try:
                        url = f"https://graph.facebook.com/v18.0/{fb_page_id}/photos"
                        payload = {
                            'url': image_url,
                            'caption': post_caption,
                            'access_token': fb_access_token
                        }
                        fb_res = requests.post(url, data=payload)
                        res_data = fb_res.json()
                        
                        if "id" in res_data:
                            st.success("تم النشر بنجاح على صفحتك في فيسبوك!")
                        else:
                            st.warning(f"تعذر النشر التلقائي: {res_data.get('error', {}).get('message', 'خطأ غير معروف')}")
                    except Exception as ex:
                        st.error(f"خطأ في الاتصال بواجهة فيسبوك: {ex}")
            else:
                st.info("ملاحظة: لم يتم إدخال بيانات فيسبوك، تم عرض النتائج لك للمراجعة اليدوية.")
