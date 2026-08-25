import streamlit as st
import openai
import requests

# Page configuration
st.set_page_config(
    page_title="مدير الصفحات والنشر الآلي",
    page_icon="✨",
    layout="centered"
)

# Modern Clean UI Styling (Fixed RTL and Layout)
st.markdown("""
<style>
    /* Global Settings for Clean Modern Look */
    .main {
        background-color: #f8fafc;
    }
    
    /* Force proper RTL alignment cleanly */
    div.block-container {
        direction: rtl;
        text-align: right;
    }
    
    p, label, span, h1, h2, h3, h4, h5, h6, div {
        direction: rtl !important;
        text-align: right !important;
    }

    /* Modern Card Container */
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Modern Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 15px rgba(29, 78, 216, 0.4);
    }

    /* Inputs Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center; color: #1e293b;'>🚀 لوحة تحكم الذكاء الاصطناعي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>أهلاً بك يا جاسم! أنشئ صور منتجاتك، اكتب منشوراتك، وانشرها بضغطة زر واحدة.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for Settings
with st.sidebar:
    st.markdown("### ⚙️ إعدادات الحساب")
    openai_api_key = st.text_input("مفتاح OpenAI API Key", type="password", placeholder="sk-...")
    
    st.markdown("---")
    st.markdown("### 🌐 ربط فيسبوك (اختياري)")
    fb_page_id = st.text_input("معرف الصفحة (Page ID)", placeholder="أدخل رقم الصفحة")
    fb_access_token = st.text_input("توكن الوصول (Access Token)", type="password", placeholder="EAAG...")
    
    st.info("💡 أدخل مفتاح OpenAI لتفعيل التوليد.")

# Main Form Area
with st.form("ai_creator_form"):
    st.markdown("### 📝 تفاصيل المنتج أو الحملة")
    product_prompt = st.text_area(
        "اكتب وصفاً تفصيلياً للمنتج أو العرض:",
        placeholder="مثلاً: عطر رجالي فخم بتركيبة العود والعنبر، زجاجة أنيقة بتصميم عصري...",
        height=120
    )
    
    submitted = st.form_submit_button("✨ ابدأ توليد المحتوى والنشر الآلي")

if submitted:
    if not openai_api_key:
        st.error("الرجاء إدخال مفتاح OpenAI API Key في الشريط الجانبي أولاً.")
    else:
        openai.api_key = openai_api_key
        
        # Step 1: Generate Post Text
        with st.spinner("⏳ جاري صياغة المنشور التسويقي الاحترافي..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت مسوق إلكتروني محترف تكتب منشورات تجارية جذابة جداً باللغة العربية مع إيموجي مناسبة."},
                        {"role": "user", "content": f"اكتب منشور تسويقي قصير وجذاب بالاعتماد على هذا الوصف: {product_prompt}"}
                    ]
                )
                post_caption = response.choices[0].message.content
            except Exception as e:
                post_caption = f"عروض حصرية ومميزة على {product_prompt}! لا تفوت الفرصة واطلب الآن."

        # Step 2: Generate Image
        with st.spinner("🎨 جاري توليد الصورة التجريبية بالذكاء الاصطناعي..."):
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
            st.success("🎉 تم توليد المحتوى والصورة بنجاح!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 🖼️ الصورة المولّدة:")
                st.image(image_url, use_container_width=True)
            with col2:
                st.markdown("#### 📄 النص التسويقي:")
                st.info(post_caption)

            # Step 3: Publish to Facebook
            if fb_page_id and fb_access_token:
                with st.spinner("🚀 جاري النشر التلقائي على فيسبوك..."):
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
                            st.success("✅ تم النشر بنجاح على صفحتك في فيسبوك!")
                        else:
                            st.warning(f"تعذر النشر التلقائي: {res_data.get('error', {}).get('message', 'خطأ غير معروف')}")
                    except Exception as ex:
                        st.error(f"خطأ في الاتصال بواجهة فيسبوك: {ex}")
            else:
                st.info("💡 ملاحظة: لم تقم بإدخال بيانات فيسبوك، تم عرض النتائج لك للمراجعة اليدوية.")
