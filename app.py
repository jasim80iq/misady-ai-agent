import streamlit as st
import openai
import requests

# Page configuration
st.set_page_config(
    page_title="مدير الصفحات والنشر الآلي",
    page_icon="🤖",
    layout="centered"
)

# Custom Styling for Arabic RTL layout & fixing text wrapping
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    p, h1, h2, h3, h4, h5, h6, label, span, div {
        direction: rtl !important;
        text-align: right !important;
        font-family: sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 مدير الصفحات والذكاء الاصطناعي")
st.write("أهلاً بك يا جاسم! من خلال هذه الواجهة، يمكنك توليد صور لمنتجاتك، كتابة المنشورات، ونشرها تلقائياً بضغطة زر.")

# Sidebar for API Keys configuration
with st.sidebar:
    st.header("🔑 إعدادات المفاتيح")
    openai_api_key = st.text_input("مفتاح OpenAI API Key", type="password")
    fb_page_id = st.text_input("معرف صفحة فيسبوك (Page ID)")
    fb_access_token = st.text_input("توكن صفحة فيسبوك (Page Access Token)", type="password")
    st.info("قم بإدخال مفتاح OpenAI أولاً لتفعيل التوليد.")

# Main Form
with st.form("publishing_form"):
    st.subheader("📝 تفاصيل المنتج أو المنشور")
    product_prompt = st.text_area(
        "اكتب وصفاً مختصراً للمنتج أو العرض:",
        placeholder="مثلاً: حذاء رياضي شبابي جديد ذو تصميم عالي الجودة ومريح..."
    )
    
    submitted = st.form_submit_button("✨ ولّد الصورة والمنشور وانشر الآن")

if submitted:
    if not openai_api_key:
        st.error("الرجاء إدخال مفتاح OpenAI API Key في الشريط الجانبي أولاً.")
    else:
        openai.api_key = openai_api_key
        
        # Step 1: Generate Marketing Post Text
        with st.spinner("جاري صياغة المنشور التسويقي..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "أنت مسوق إلكتروني محترف تكتب منشورات جذابة لصفحات التسوق باللغة العربية مع الإيموجي المناسبة."},
                        {"role": "user", "content": f"اكتب منشور تسويقي قصير وجذاب لمنتج بالاعتماد على الوصف التالي: {product_prompt}"}
                    ]
                )
                post_caption = response.choices[0].message.content
            except Exception as e:
                post_caption = f"عروض مميزة وخصومات رائعة على {product_prompt}! لا تفوت الفرصة."

        # Step 2: Generate Image using DALL-E 3
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
                st.image(image_url, caption="الصورة المولّدة", use_container_width=True)
            with col2:
                st.markdown("### 📄 المنشور المقترح:")
                st.write(post_caption)

            # Step 3: Publish to Facebook (if tokens provided)
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
                            st.success("🎉 تم النشر بنجاح على صفحتك في فيسبوك!")
                        else:
                            st.warning(f"تم توليد المحتوى ولكن تعذر النشر التلقائي: {res_data.get('error', {}).get('message', 'خطأ غير معروف')}")
                    except Exception as ex:
                        st.error(f"خطأ في الاتصال بواجهة فيسبوك: {ex}")
            else:
                st.info("💡 لم يتم إدخال بيانات فيسبوك، تم عرض النتيجة لك هنا للمراجعة.")
