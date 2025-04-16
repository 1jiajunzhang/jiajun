import streamlit as st
import requests

# Fetch Material Icons list from Google's official repository
@st.cache_data
def get_material_icons():
    url = "https://raw.githubusercontent.com/google/material-design-icons/master/font/MaterialIcons-Regular.codepoints"
    response = requests.get(url)
    if response.status_code == 200:
        icons = response.text.split("\n")
        icon_dict = {line.split()[0]: line.split()[1] for line in icons if line.strip()}
        return icon_dict
    else:
        return {}

# Load the icons
icons = get_material_icons()

# Streamlit UI
st.title("Material Icons Explorer")
st.write("Search and explore Material Design Icons for use in Streamlit!")

# Search box
query = st.text_input("Search for an icon:", "").strip().lower()

# Filter icons based on query
if query:
    filtered_icons = {name: code for name, code in icons.items() if query in name.lower()}
else:
    filtered_icons = icons

# Display results
if filtered_icons:
    cols = st.columns(5)  # Display 5 icons per row
    for idx, (icon_name, icon_code) in enumerate(filtered_icons.items()):
        with cols[idx % 5]:
            st.markdown(f":material/{icon_name}:")
            st.write(icon_name)
else:
    st.warning("No icons found. Try a different keyword.")

# Display total count
st.write(f"Showing {len(filtered_icons)} icons.")
