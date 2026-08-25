import streamlit as st
import openai
import requests

st.set_page_config(
    page_title="AI Page Manager",
    page_icon="🚀",
    layout="centered"
)

# Strict styling to lock direction and prevent character breakage
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
    }
    .main-title {
        text-align: center;
        color: #1e293b;
        font-weight: 800;
    }
    .sub-text {
        text-align: center;
        color: #64748b;
        margin-bottom: 30px;
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

st.markdown("<h1 class='main-title'>AI Social Media Manager</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>Generate images, marketing captions, and publish automatically.</p>", unsafe_allow_html=True)

# Sidebar with clean English labels to avoid mobile rendering bugs
with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    st.markdown("---")
    st.header("Facebook Integration")
    fb_page_id = st.text_input("Facebook Page ID")
    fb_access_token = st.text_input("Page Access Token", type="password")
    
    st.info("Enter your OpenAI key to start generating.")

# Main Form
with st.form("main_form"):
    st.subheader("Product Description")
    product_prompt = st.text_area(
        "Describe your product or offer:",
        placeholder="e.g., A luxury men's perfume with oud and amber notes..."
    )
    
    submitted = st.form_submit_button("✨ Generate & Publish")

if submitted:
    if not openai_api_key:
        st.error("Please enter your OpenAI API Key in the sidebar first.")
    else:
        openai.api_key = openai_api_key
        
        # Step 1: Generate Post Text
        with st.spinner("Writing marketing caption..."):
            try:
                client = openai.OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional digital marketer. Write a catchy marketing caption in Arabic with emojis based on the user's description."},
                        {"role": "user", "content": f"Write a marketing post for: {product_prompt}"}
                    ]
                )
                post_caption = response.choices[0].message.content
            except Exception as e:
                post_caption = f"عروض مميزة وخصومات رائعة على {product_prompt}!"

        # Step 2: Generate Image
        with st.spinner("Generating commercial image with DALL-E 3..."):
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
                st.error(f"Image generation failed: {e}")
                image_url = None

        # Display Results
        if image_url:
            st.success("Content generated successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(image_url, caption="Generated Image", use_container_width=True)
            with col2:
                st.markdown("### Marketing Caption:")
                st.info(post_caption)

            # Step 3: Publish to Facebook
            if fb_page_id and fb_access_token:
                with st.spinner("Publishing to Facebook..."):
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
                            st.success("Published successfully to Facebook!")
                        else:
                            st.warning(f"Publishing failed: {res_data.get('error', {}).get('message', 'Unknown error')}")
                    except Exception as ex:
                        st.error(f"Connection error: {ex}")
            else:
                st.info("Facebook credentials not provided. Results displayed for manual review.")
