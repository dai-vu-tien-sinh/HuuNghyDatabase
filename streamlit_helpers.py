import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
import re
from translations import get_text

def translate_sidebar_nav():
    """
    This function injects CSS to translate the sidebar navigation items.
    Should be called at the start of each page.
    """
    # Get current page name
    ctx = get_script_run_ctx()
    if ctx is None:
        return

    current_page = ctx.page_script_hash

    # CSS for translating sidebar labels
    css = """
    <style>
    /* Target all sidebar nav links with more comprehensive selectors */
    /* Main page */
    [data-testid="stSidebar"] a[href="/"],
    .st-emotion-cache-j9xo7p a[href="/"],
    .st-emotion-cache-16idsys a[href="/"],
    .st-emotion-cache-7ym5gk a[href="/"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/"]:after,
    .st-emotion-cache-j9xo7p a[href="/"]:after,
    .st-emotion-cache-16idsys a[href="/"]:after,
    .st-emotion-cache-7ym5gk a[href="/"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }

    /* Admin page */
    [data-testid="stSidebar"] a[href="/admin"],
    .st-emotion-cache-j9xo7p a[href="/admin"],
    .st-emotion-cache-16idsys a[href="/admin"],
    .st-emotion-cache-7ym5gk a[href="/admin"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/admin"]:after,
    .st-emotion-cache-j9xo7p a[href="/admin"]:after,
    .st-emotion-cache-16idsys a[href="/admin"]:after,
    .st-emotion-cache-7ym5gk a[href="/admin"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }

    /* Medical page */
    [data-testid="stSidebar"] a[href="/medical"],
    .st-emotion-cache-j9xo7p a[href="/medical"],
    .st-emotion-cache-16idsys a[href="/medical"],
    .st-emotion-cache-7ym5gk a[href="/medical"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/medical"]:after,
    .st-emotion-cache-j9xo7p a[href="/medical"]:after,
    .st-emotion-cache-16idsys a[href="/medical"]:after,
    .st-emotion-cache-7ym5gk a[href="/medical"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }

    /* Psychology page */
    [data-testid="stSidebar"] a[href="/psychology"],
    .st-emotion-cache-j9xo7p a[href="/psychology"],
    .st-emotion-cache-16idsys a[href="/psychology"],
    .st-emotion-cache-7ym5gk a[href="/psychology"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/psychology"]:after,
    .st-emotion-cache-j9xo7p a[href="/psychology"]:after,
    .st-emotion-cache-16idsys a[href="/psychology"]:after,
    .st-emotion-cache-7ym5gk a[href="/psychology"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }

    /* Students page */
    [data-testid="stSidebar"] a[href="/students"],
    .st-emotion-cache-j9xo7p a[href="/students"],
    .st-emotion-cache-16idsys a[href="/students"],
    .st-emotion-cache-7ym5gk a[href="/students"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/students"]:after,
    .st-emotion-cache-j9xo7p a[href="/students"]:after,
    .st-emotion-cache-16idsys a[href="/students"]:after,
    .st-emotion-cache-7ym5gk a[href="/students"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }

    /* Veterans page */
    [data-testid="stSidebar"] a[href="/veterans"],
    .st-emotion-cache-j9xo7p a[href="/veterans"],
    .st-emotion-cache-16idsys a[href="/veterans"],
    .st-emotion-cache-7ym5gk a[href="/veterans"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/veterans"]:after,
    .st-emotion-cache-j9xo7p a[href="/veterans"]:after,
    .st-emotion-cache-16idsys a[href="/veterans"]:after,
    .st-emotion-cache-7ym5gk a[href="/veterans"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Data Import page */
    [data-testid="stSidebar"] a[href="/data_import"],
    .st-emotion-cache-j9xo7p a[href="/data_import"],
    .st-emotion-cache-16idsys a[href="/data_import"],
    .st-emotion-cache-7ym5gk a[href="/data_import"] {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebar"] a[href="/data_import"]:after,
    .st-emotion-cache-j9xo7p a[href="/data_import"]:after,
    .st-emotion-cache-16idsys a[href="/data_import"]:after,
    .st-emotion-cache-7ym5gk a[href="/data_import"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "Import Data";
    }
    </style>
    """ % (
        get_text("navigation.main"),
        get_text("navigation.admin"),
        get_text("navigation.medical"),
        get_text("navigation.psychology"),
        get_text("navigation.students"),
        get_text("navigation.veterans")
    )

    st.markdown(css, unsafe_allow_html=True)