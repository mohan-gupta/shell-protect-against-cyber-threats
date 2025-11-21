import streamlit as st

import base64

from predict import get_span


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

contnt = "<p>Protecting our software landscapes is not an easy task. Malicious actors are frequently trying to enter systems and get access to resources, whether operational or data. The ability for an actor to compromise systems, elevate their privileges, and move laterally within infrastructure typically hinges on executing hidden code. One common method they employ is embedding this code in seemingly harmless media—whether it's images, videos, or even simple text files.</p>"


if __name__ == '__main__':
    add_bg_from_local("../assets/background.jfif")
    new_title = '<p style="font-family:sans-serif; color:White; font-size: 42px;">Cyber Threat Detection</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    st.markdown(contnt, unsafe_allow_html=True)

    if text := st.text_area("Enter your text here.."):
        if st.button("Get Span"):
            span = get_span(text)

            result_text = '<p style="font-family:sans-serif; color:White; font-size: 16px; font-weight: bold">Identified code:</p>'
            span_result = '<p style="font-family:sans-serif; color:White; font-size: 14px; font-weight: italic">'+span+'</p>'
            st.markdown(result_text, unsafe_allow_html=True)
            st.markdown(span_result, unsafe_allow_html=True)