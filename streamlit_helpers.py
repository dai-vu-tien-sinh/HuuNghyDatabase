
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
    /* Main page */
    .st-emotion-cache-j9xo7p a[href="/"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Admin page */
    .st-emotion-cache-j9xo7p a[href="/admin"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/admin"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Medical page */
    .st-emotion-cache-j9xo7p a[href="/medical"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/medical"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Psychology page */
    .st-emotion-cache-j9xo7p a[href="/psychology"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/psychology"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Students page */
    .st-emotion-cache-j9xo7p a[href="/students"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/students"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
    }
    
    /* Veterans page */
    .st-emotion-cache-j9xo7p a[href="/veterans"] {
        visibility: hidden;
        position: relative;
    }
    .st-emotion-cache-j9xo7p a[href="/veterans"]:after {
        visibility: visible;
        position: absolute;
        left: 0;
        content: "%s";
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
