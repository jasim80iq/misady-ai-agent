import streamlit as st

st.set_page_config(page_title='مساعدي الذكي', page_icon='🤖', layout='wide')
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

st.title('🤖 مساعدي الذكي')
st.caption('وكيل عراقي متعدد المهام — الإصدار الأول')

with st.sidebar:
    st.header('الأقسام')
    mode = st.radio('اختار المهمة', [
        '💬 المساعد العام', '🎬 الفيديو', '📸 الصور والإعلانات',
        '📱 السوشيال ميديا', '💬 ردود الزبائن', '📂 الملفات'
    ])
    st.divider()
    st.write('النسخة الحالية هي الهيكل الأول للوكيل. يتم ربط الذكاء الاصطناعي والأدوات الخارجية في المرحلة التالية.')

if mode == '🎬 الفيديو':
    st.header('🎬 استوديو الفيديو')
    idea = st.text_area('اكتب فكرتك', placeholder='مثال: إعلان لعطر فاخر لمدة 8 ثوانٍ باللهجة العراقية')
    duration = st.selectbox('المدة', ['8 ثوانٍ', '15 ثانية', '30 ثانية'])
    if st.button('جهّز الإعلان', type='primary'):
        st.subheader('مخطط جاهز')
        st.write(f'**المدة:** {duration}')
        st.write('**المشهد:** لقطة افتتاحية للمنتج → حركة كاميرا سينمائية → إبراز التفاصيل → لقطة ختامية للعلامة.')
        st.code('Ultra-realistic cinematic commercial, premium product advertising, 4K, dramatic studio lighting, smooth camera movement, shallow depth of field, highly detailed, premium look.')

elif mode == '📸 الصور والإعلانات':
    st.header('📸 استوديو الصور والإعلانات')
    product = st.text_area('صف المنتج أو اكتب المطلوب')
    if st.button('جهّز Prompt', type='primary'):
        st.code('Create a premium commercial product photograph, ultra-realistic, cinematic studio lighting, 4K, sharp details, elegant composition, realistic reflections, advertising photography.')

elif mode == '📱 السوشيال ميديا':
    st.header('📱 السوشيال ميديا')
    idea = st.text_area('شنو تريد تنشر؟')
    platform = st.selectbox('المنصة', ['Instagram', 'Facebook', 'TikTok'])
    if st.button('جهّز المنشور', type='primary'):
        st.subheader('منشور مقترح')
        st.write(f'**المنصة:** {platform}')
        st.write(f'{idea}\n\n🔥 خلي تجربتك غير! تواصل ويانا للمزيد من التفاصيل.\n\n#عروض #عراق #محتوى')

elif mode == '💬 ردود الزبائن':
    st.header('💬 مساعد الزبائن')
    msg = st.text_area('الصق رسالة الزبون')
    if st.button('اكتب الرد', type='primary'):
        st.write('أهلاً وسهلاً بيك 🌹 شكراً لتواصلك ويانا. نعتذر إذا تأخرنا بالرد، وراح نساعدك بكل التفاصيل المطلوبة.')

elif mode == '📂 الملفات':
    st.header('📂 مركز الملفات')
    f = st.file_uploader('ارفع ملفاً', type=['txt','csv','pdf','docx'])
    if f:
        st.success(f'تم استلام: {f.name}')
        st.info('سيتم ربط القراءة الذكية والتلخيص والبحث داخل الملفات في المرحلة التالية.')

else:
    st.header('💬 المساعد العام')
    request = st.text_area('اكتب طلبك باللهجة العراقية أو العربية', height=140)
    if st.button('تنفيذ', type='primary'):
        if request.strip():
            st.write('تم استلام طلبك. هذه النسخة هي الهيكل الأول؛ الخطوة التالية تربط العقل الذكي حتى يحلل الطلب ويختار الأداة المناسبة تلقائياً.')
        else:
            st.warning('اكتب طلبك أولاً.')

st.divider()
st.caption('مساعدي الذكي — Prototype 0.1')
