import streamlit as st
import openai
import requests

st.set_page_config(page_title="AI Page Manager", layout="centered")

st.title("AI Page Manager")
st.write("Generate images and captions easily.")

with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-proj-...")
    
    fb_page_id = st.text_input("Facebook Page ID")
    fb_access_token = st.text_input("Access Token", type="password")

with st.form("my_form"):
    prompt = st.text_area("Product Description:", "A modern leather shoes...")
    submit = st.form_submit_button("Generate & Publish")

if submit:
    if not openai_api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    else:
        # Clean the prompt to remove any invisible/non-ascii characters
        clean_prompt = prompt.encode("ascii", "ignore").decode("ascii")
        if not clean_prompt.strip():
            clean_prompt = "A beautiful portrait of an arabic woman, professional photography"

        openai.api_key = openai_api_key
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Step 1: Translate prompt safely using GPT
        with st.spinner("Processing prompt..."):
            try:
                translation_res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Translate the user's description into a clean English prompt for image generation. Return ONLY the English translation."},
                        {"role": "user", "content": clean_prompt}
                    ]
                )
                english_prompt = translation_res.choices[0].message.content
            except Exception as e:
                english_prompt = "Professional commercial photography of " + clean_prompt

        # Step 2: Generate Post Caption
        with st.spinner("Generating caption..."):
            try:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": f"Write a short catchy marketing caption in Arabic for: {clean_prompt}"}]
                )
                caption = res.choices[0].message.content
            except Exception as e:
                caption = f"عروض مميزة وخصومات رائعة!"

        # Step 3: Generate Image using safe English prompt
        with st.spinner("Generating image..."):
            try:
                img_res = client.images.generate(
                    model="dall-e-2",
                    prompt=english_prompt,
                    size="512x512",
                    n=1
                )
                img_url = img_res.data[0].url
            except Exception as e:
                st.error(f"Image error: {e}")
                img_url = None

        if img_url:
            st.success("Generated successfully!")
            st.image(img_url, use_container_width=True)
            st.info(caption)

            if fb_page_id and fb_access_token:
                try:
                    url = f"https://graph.facebook.com/v18.0/{fb_page_id}/photos"
                    payload = {'url': img_url, 'caption': caption, 'access_token': fb_access_token}
                    fb_res = requests.post(url, data=payload).json()
                    if "id" in fb_res:
                        st.success("Published to Facebook!")
                    else:
                        st.warning("Publish failed.")
                except Exception as ex:
                    st.error(f"FB error: {ex}")
