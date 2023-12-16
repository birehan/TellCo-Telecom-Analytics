import streamlit as st
def run():

    st.set_page_config(
        page_title="Tellco Telecom Analytics!",
        page_icon="🌐",
    )

    with open('style/style.css') as f:
      css = f.read()

    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    st.write("# Tellco Telecom Analytics! 🌐")

    st.sidebar.success("Select a section above.")

   


if __name__ == "__main__":
    run()
