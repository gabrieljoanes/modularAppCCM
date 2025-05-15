import streamlit as st
import openai
from utils.file_io import load_prompt, load_transitions, sample_shots
from utils.transition_filter import validate_transitions  # ✅ NEW IMPORT

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

def render():
    st.title("🧠 Transition Generator")
    st.markdown("Paste your article with `TRANSITION` markers. We'll insert natural transitions.")

    meta_instruction = load_prompt("prompts/transition_meta.txt")
    prompt_scaffold = load_prompt("prompts/transition_prompt.txt")  # optional formatting
    examples = sample_shots(load_transitions("assets/transitions.jsonl"), 3)

    user_input = st.text_area("📝 Input Article", height=300)

    with st.expander("🔍 Prompt Preview (editable)"):
        example_block = "\n\n".join(
            [f"User: {ex['input']}\nAssistant: {ex['transition']}" for ex in examples]
        )
        full_prompt = f"{meta_instruction}\n\n{example_block}\n\nUser: {user_input}"
        editable_prompt = st.text_area("Prompt sent to model:", full_prompt, height=300)

    if st.button("✨ Generate Transitions"):
        with st.spinner("Generating..."):
            response = client.chat.completions.create(
                model="gpt-4",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": meta_instruction},
                    *[
                        {"role": "user", "content": ex["input"]}
                        if i % 2 == 0 else {"role": "assistant", "content": ex["transition"]}
                        for i, ex in enumerate(sum([[ex, ex] for ex in examples], []))
                    ],
                    {"role": "user", "content": user_input}
                ],
                max_tokens=1000
            )

            raw_output = response.choices[0].message.content
            # 🔍 Attempt to split into lines (assumes each transition on a new line)
            lines = [line.strip() for line in raw_output.split("\n") if line.strip()]
            filtered = validate_transitions(lines)
            final_output = "\n".join(filtered)

            st.markdown("### 🪄 Output")
            st.text_area("Generated Output", final_output, height=300)
