import streamlit as st
import wikipedia

# --- Page Config ---
st.set_page_config(page_title="chatbot", page_icon="🤖")
st.title("📚 Info Guru")

# --- Features Box ---
with st.expander("📌 Features"):
    st.markdown("""
    - 💬 Ask questions and get answers from Wikipedia  
    - 👁 View only 2 sentences initially with See More / See Less toggle  
    - 🗑 Clear chat history  
    """)

# --- Initialize Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "expanded" not in st.session_state:
    st.session_state.expanded = {}
if "input_processed" not in st.session_state:
    st.session_state.input_processed = False

# --- Clear Chat History Button ---
if st.button("🗑 Clear Chat History"):
    st.session_state.messages = []
    st.session_state.expanded = {}
    st.session_state.input_processed = False
    st.rerun()

# --- Wikipedia Summary Function ---
def get_wikipedia_summary(query):
    try:
        results = wikipedia.search(query)
        if not results:
            return "❌ Sorry, I couldn't find anything on that topic."

        summary = wikipedia.summary(results[0], sentences=5, auto_suggest=False, redirect=True)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"⚠️ Your query is ambiguous, did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.PageError:
        return "❌ Sorry, I couldn't find a page matching your query."
    except Exception:
        return "⚠️ Oops, something went wrong."

# --- User Input ---
user_input = st.text_input("Ask me anything:")

if user_input and not st.session_state.input_processed:
    # Only process input if it's new or not a repeat
    if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["content"] != user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        bot_response = get_wikipedia_summary(user_input)
        msg_index = len(st.session_state.messages)
        st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.session_state.expanded[msg_index] = False  # collapsed by default
        st.session_state.input_processed = True
        st.rerun()

# Reset input_processed if input field is cleared
if user_input == "":
    st.session_state.input_processed = False

# --- Display Chat History ---
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"🧑 You: {msg['content']}")
    else:
        content = msg["content"]
        if len(content.split(". ")) > 2:
            if st.session_state.expanded.get(idx, False):
                st.markdown(f"🤖 Bot: {content}")
                if st.button("See Less ⬆️", key=f"less_{idx}"):
                    st.session_state.expanded[idx] = False
                    st.rerun()
            else:
                short_text = ". ".join(content.split(". ")[:2]) + "..."
                st.markdown(f"🤖 Bot: {short_text}")
                if st.button("See More ⬇️", key=f"more_{idx}"):
                    st.session_state.expanded[idx] = True
                    st.rerun()
        else:

            st.markdown(f"🤖 Bot: {content}")
