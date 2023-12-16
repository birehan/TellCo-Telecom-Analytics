import streamlit as st
def run():

    st.set_page_config(
        page_title="Tellco Telecom Analytics!",
        page_icon="🌐",
    )

    # with open('style/style.css') as f:
    #   css = f.read()

    # st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    st.write("# Tellco Telecom Analytics! 🌐")
    
    st.markdown(
        """
        Welcome to the Tellco Telecom Data Analysis Dashboard! 🌐

        This interactive dashboard provides a comprehensive analysis of Tellco Telecom's user data, offering insights into user behavior, engagement, experience, and overall satisfaction.

        ### Sections:
        - **User Overview Analysis:** Explore general statistics and patterns in the user dataset, including top handsets, user sessions, and data usage.

        - **User Engagement Analysis:** Gain insights into user engagement metrics such as session frequency, duration, and data usage patterns.

        - **User Experience Analysis:** Dive into the user experience, analyzing factors like average round-trip time, throughput, and TCP retransmission.

        - **User Satisfaction Analysis:** Understand user satisfaction by combining engagement and experience scores, with a focus on the top satisfied customers.

        ### Instructions:
        - Use the sidebar to navigate between different sections of the analysis.
        - Each section provides detailed visualizations and summaries based on specific aspects of user data.

        Explore the various facets of Tellco Telecom's user data to make informed decisions and uncover valuable insights!
        """
    )

    st.sidebar.success("Select a section above.")

if __name__ == "__main__":
    run()
