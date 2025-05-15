from utils.version import get_version
import streamlit as st
import openai
from utils.file_io import load_prompt, load_transitions, sample_shots
from utils.transition_validator import validate_transitions
from utils.transition_cleaner import clean_transitions
from utils.geo_checker import detect_misleading_geo_transition

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

def render():
    st.title("🧠 Transition Generator")
    st.markdown("Paste your article with `TRANSITION` markers. We'll insert natural transitions.")
    st.markdown(f"**🧾 Version:** `{get_version()}`")
    meta_instruction = load_prompt("prompts/transition_meta.txt")
    prompt_template = load_prompt("prompts/transition_prompt.txt")
    examples = sample_shots(load_transitions("assets/transitions.jsonl"), 3)

    user_input = st.text_area("📝 Input Article", height=400)

    if st.button("✨ Generate Transitions"):
        with st.spinner("Generating transitions..."):
            parts = user_input.split("TRANSITION")
            if len(parts) < 2:
                st.warning("No TRANSITION markers found.")
                return

            transitions = []
            for i in range(len(parts) - 1):
                messages = [{"role": "system", "content": meta_instruction}]
                for ex in examples:
                    messages.append({"role": "user", "content": ex["input"]})
                    messages.append({"role": "assistant", "content": ex["transition"]})

                formatted_prompt = prompt_template.format(
                    paragraph_a=parts[i].strip(),
                    paragraph_b=parts[i + 1].strip()
                )
                messages.append({"role": "user", "content": formatted_prompt})

                response = client.chat.completions.create(
                    model="gpt-4",
                    temperature=0.7,
                    messages=messages,
                    max_tokens=30
                )
                transition = response.choices[0].message.content.strip()
                transitions.append(transition)

            # Apply all filters
            transitions = validate_transitions(transitions)
            transitions = clean_transitions(transitions)

            for i, t in enumerate(transitions):
                if detect_misleading_geo_transition(t, parts[i], parts[i + 1]):
                    transitions[i] = "[GEO WARNING: Check transition accuracy]"

            # Rebuild article
            rebuilt_article = parts[0].strip()
            for i, t in enumerate(transitions):
                rebuilt_article += f"\n\n{t}\n\n{parts[i + 1].strip()}"

            st.markdown("### 🪄 Output")
            st.text_area("Generated Output", rebuilt_article, height=500)
