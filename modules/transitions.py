import streamlit as st
import openai
from utils.file_io import load_prompt, load_transitions, sample_shots
from utils.transition_filter import validate_transitions

import re

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

def extract_locations(text):
    """Very simple heuristic location detector (can be replaced by spaCy later)."""
    return re.findall(r"\\b(?:Fougères|Maen Roch|Saint-Malo|Dompierre|Ille-et-Vilaine|Bretagne|St-Brice)\\b", text)

def render():
    st.title("🧠 Transition Generator")
    st.markdown("Paste your article with `TRANSITION` markers. We'll insert natural transitions.")

    meta_instruction = load_prompt("prompts/transition_meta.txt")
    prompt_scaffold = load_prompt("prompts/transition_prompt.txt")  # optional formatting
    examples = sample_shots(load_transitions("assets/transitions.jsonl"), 3)

    user_input = st.text_area("📝 Input Article", height=400)

    if st.button("✨ Generate Transitions"):
        with st.spinner("Generating transitions..."):
            parts = user_input.split("TRANSITION")
            if len(parts) < 2:
                st.warning("No TRANSITION markers found.")
                return

            transitions = []
            contexts = []

            for i in range(len(parts) - 1):
                para_a = parts[i].strip()
                para_b = parts[i + 1].strip()

                # Simple geographic similarity heuristic
                loc_a = set(extract_locations(para_a))
                loc_b = set(extract_locations(para_b))
                same_region = bool(loc_a & loc_b) or "Ille-et-Vilaine" in loc_a.union(loc_b)

                context_info = {"same_region": same_region}

                # Build few-shot messages
                messages = [{"role": "system", "content": meta_instruction}]
                for ex in examples:
                    messages.append({"role": "user", "content": ex["input"]})
                    messages.append({"role": "assistant", "content": ex["transition"]})
                messages.append({
                    "role": "user",
                    "content": f"{para_a}\nTRANSITION\n{para_b}"
                })

                # Generate transition
                response = client.chat.completions.create(
                    model="gpt-4",
                    temperature=0.7,
                    messages=messages,
                    max_tokens=30
                )
                transition = response.choices[0].message.content.strip()
                transitions.append(transition)
                contexts.append(context_info)

            # Validate transitions with individual context
            validated = [
                validate_transitions([t], context_info=contexts[i])[0]
                for i, t in enumerate(transitions)
            ]

            # Rebuild the full article
            rebuilt_article = parts[0].strip()
            for i, t in enumerate(validated):
                rebuilt_article += f"\n\n{t}\n\n{parts[i + 1].strip()}"

            st.markdown("### 🪄 Output")
            st.text_area("Generated Output", rebuilt_article, height=500)
