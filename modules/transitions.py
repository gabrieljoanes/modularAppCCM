import streamlit as st
import openai
from utils.file_io import load_prompt, load_transitions, sample_shots
from utils.transition_filter import validate_transitions

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

def render():
    st.title("🧠 Transition Generator")
    st.markdown("Paste your article with TRANSITION markers. We'll insert natural transitions.")

    meta_instruction = load_prompt("prompts/transition_meta.txt")
    prompt_scaffold = load_prompt("prompts/transition_prompt.txt")  # optional formatting
    examples = sample_shots(load_transitions("assets/transitions.jsonl"), 3)

    user_input = st.text_area("📝 Input Article", height=400)

    if st.button("✨ Generate Transitions"):
        with st.spinner("Generating transitions..."):
            # Split the article into segments at each TRANSITION
            parts = user_input.split("TRANSITION")
            if len(parts) < 2:
                st.warning("No TRANSITION markers found.")
                return

            transitions = []
            for i in range(len(parts) - 1):
                # Build few-shot prompt per transition
                messages = [{"role": "system", "content": meta_instruction}]
                for ex in examples:
                    messages.append({"role": "user", "content": ex["input"]})
                    messages.append({"role": "assistant", "content": ex["transition"]})
                messages.append({
                    "role": "user",
                    "content": f"{parts[i].strip()}\nTRANSITION\n{parts[i + 1].strip()}"
                })

                # Generate a single transition
                response = client.chat.completions.create(
                    model="gpt-4",
                    temperature=0.7,
                    messages=messages,
                    max_tokens=30
                )
                transition = response.choices[0].message.content.strip()
                transitions.append(transition)

            # Validate and optionally clean transitions
            validated = validate_transitions(transitions)

            # Rebuild final output with transitions
            rebuilt_article = parts[0].strip()
            for i, t in enumerate(validated):
                rebuilt_article += f"\n\n{t}\n\n{parts[i + 1].strip()}"

            st.markdown("### 🪄 Output")
            st.text_area("Generated Output", rebuilt_article, height=500) 
