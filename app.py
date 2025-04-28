import streamlit as st
from PIL import Image
from predict import get_prediction, draw_bounding_boxes
import io

# Set the page configuration
st.set_page_config(
    page_title="Object Detection App",
    layout="wide"
)

# Inject custom CSS to adjust layout without cropping and fix image size
st.markdown(
    """
    <style>
    body {
        margin: 0;
        padding: 0;
    }
    .main {
        padding: 0;
    }
    .block-container {
        padding-top: 40px;  /* Ensure there's space at the top */
        padding-bottom: 0;
    }
    h4 {
        font-size: 28px;  /* Increased font size to give more prominence */
        margin-top: 40px;  /* Increased top margin to avoid cropping */
        margin-bottom: 20px;  /* Added bottom margin to separate from content */
        line-height: 1.3;  /* Increased line-height for better vertical spacing */
        text-align: center;
    }
    .image-box {
        max-width: 100%;
        max-height: 600px;  /* Increased max height to utilize space */
        overflow: hidden;  /* Hide any overflow */
    }
    </style>
    """, unsafe_allow_html=True
)

# 🌟 Title with custom styling
st.markdown("<h4>Intelligent Detection and Verification App</h4>", unsafe_allow_html=True)

# 🌐 Create three columns with adjusted widths
col1, col2, col3 = st.columns([1, 2, 2])  # Adjust column sizes to fit layout

# First column: Upload Image
with col1:
    st.markdown("<h5 style='font-size: 16px;'>📁 Upload Image</h5>", unsafe_allow_html=True)
    option = st.radio("Image Input:", ["📁 Upload", "📷 Camera"], horizontal=True)
    uploaded_image = (st.file_uploader("Choose file", type=["jpg", "jpeg", "png"]) if option == "📁 Upload" 
                      else st.camera_input("Take a picture"))

# Second column: Show input image (empty box for now)
with col2:
    st.markdown("<h5 style='font-size: 16px;'>🖼️ Input Image</h5>", unsafe_allow_html=True)
    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        # Resize the image to fit the container box
        max_width = 700  # Increased max width for better utilization of space
        max_height = 600  # Increased max height for better utilization of space
        image = image.resize((min(image.width, max_width), min(image.height, max_height)))

        st.image(image, use_container_width=True)
    else:
        st.empty()  # Empty box if no image uploaded

# Third column: Show output image (after processing)
with col3:
    st.markdown("<h5 style='font-size: 16px;'>🎯 Detection Result</h5>", unsafe_allow_html=True)
    if uploaded_image is not None:
        with st.spinner("Detecting objects..."):
            try:
                predictions = get_prediction(image_bytes)
                result_image = draw_bounding_boxes(image.copy(), predictions)

                # Resize the output image to fit the container box
                result_image = result_image.resize((min(result_image.width, max_width), min(result_image.height, max_height)))
                st.image(result_image, use_container_width=True)
            except Exception as e:
                st.error(f"Prediction failed: {e}")
    else:
        st.empty()  # Empty box if no image uploaded

