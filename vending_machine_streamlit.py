"""
Healthcare Vending Machine DFA - Streamlit Web App
===================================================
A web-based DFA simulation using Streamlit.

To run locally:
    pip install streamlit
    streamlit run vending_machine_streamlit.py

To deploy free on Streamlit Cloud:
    1. Push this file to GitHub
    2. Go to share.streamlit.io
    3. Connect your GitHub repo
    4. Deploy!
"""

import streamlit as st

# ============================================================
# DFA DEFINITION
# ============================================================

ACCEPTING_STATES = {'Q7', 'Q8', 'Q9', 'Q10'}

DELTA = {
    'Q0':  {'RM5': 'Q1',  'RM10': 'Q2',  'RM20': 'Q4',  'e': 'Q0',  'v': 'Q0'},
    'Q1':  {'RM5': 'Q2',  'RM10': 'Q3',  'RM20': 'Q5',  'e': 'Q1',  'v': 'Q1'},
    'Q2':  {'RM5': 'Q3',  'RM10': 'Q4',  'RM20': 'Q6',  'e': 'Q2',  'v': 'Q2'},
    'Q3':  {'RM5': 'Q4',  'RM10': 'Q5',  'RM20': 'Q7',  'e': 'Q3',  'v': 'Q3'},
    'Q4':  {'RM5': 'Q5',  'RM10': 'Q6',  'RM20': 'Q8',  'e': 'Q4',  'v': 'Q4'},
    'Q5':  {'RM5': 'Q6',  'RM10': 'Q7',  'RM20': 'Q9',  'e': 'Q5',  'v': 'Q5'},
    'Q6':  {'RM5': 'Q7',  'RM10': 'Q8',  'RM20': 'Q10', 'e': 'Q6',  'v': 'Q6'},
    'Q7':  {'RM5': 'Q8',  'RM10': 'Q9',  'RM20': 'Q10', 'e': 'Q0',  'v': 'Q7'},
    'Q8':  {'RM5': 'Q9',  'RM10': 'Q10', 'RM20': 'Q10', 'e': 'Q0',  'v': 'Q8'},
    'Q9':  {'RM5': 'Q10', 'RM10': 'Q10', 'RM20': 'Q10', 'e': 'Q0',  'v': 'Q9'},
    'Q10': {'RM5': 'Q10', 'RM10': 'Q10', 'RM20': 'Q10', 'e': 'Q0',  'v': 'Q0'},
}

STATE_INFO = {
    'Q0':  (0,  'No money inserted'),
    'Q1':  (5,  'RM5 inserted'),
    'Q2':  (10, 'RM10 inserted'),
    'Q3':  (15, 'RM15 inserted'),
    'Q4':  (20, 'RM20 inserted'),
    'Q5':  (25, 'RM25 inserted'),
    'Q6':  (30, 'RM30 inserted'),
    'Q7':  (35, 'RM35 - Eye Drop ready!'),
    'Q8':  (40, 'RM40 - Eye Drop ready!'),
    'Q9':  (45, 'RM45 - Eye Drop ready!'),
    'Q10': (50, 'RM50 - Both products ready!'),
}

# ============================================================
# STREAMLIT APP
# ============================================================

# Page configuration
st.set_page_config(
    page_title="Healthcare Vending Machine DFA",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'current_state' not in st.session_state:
    st.session_state.current_state = 'Q0'
if 'history' not in st.session_state:
    st.session_state.history = []

def transition(symbol):
    """Apply DFA transition and return dispensed item if any."""
    old_state = st.session_state.current_state
    new_state = DELTA.get(old_state, {}).get(symbol, old_state)

    dispensed = None
    if old_state in ACCEPTING_STATES and new_state == 'Q0':
        if symbol == 'e':
            dispensed = 'Eye Drop'
        elif symbol == 'v':
            dispensed = 'Vitamin'

    st.session_state.current_state = new_state
    st.session_state.history.append((old_state, symbol, new_state, dispensed))

    return dispensed

def reset_machine():
    """Reset the DFA to initial state."""
    st.session_state.current_state = 'Q0'
    st.session_state.history = []

def get_balance():
    """Get current balance from state."""
    return STATE_INFO.get(st.session_state.current_state, (0, ''))[0]

def is_accepting():
    """Check if current state is accepting."""
    return st.session_state.current_state in ACCEPTING_STATES

def can_buy_vitamin():
    """Check if Vitamin can be purchased."""
    return st.session_state.current_state == 'Q10'

# ============================================================
# UI LAYOUT
# ============================================================

# Title
st.title("🏥 Healthcare Vending Machine")
st.markdown("**DFA Simulation** - Eye Drop (RM35) | Vitamin (RM50)")

# Create two columns
col_left, col_right = st.columns([1, 2])

# LEFT COLUMN - Controls
with col_left:
    # Current State Display
    st.markdown("### Current State")

    state = st.session_state.current_state
    balance = get_balance()
    accepting = is_accepting()

    # State badge with color
    if accepting:
        st.success(f"## {state}")
        st.markdown("**Status:** ✅ ACCEPTING")
    else:
        st.info(f"## {state}")
        st.markdown("**Status:** ⏳ REJECT (need more money)")

    st.markdown(f"**Balance:** RM{balance}")
    st.markdown(f"**Description:** {STATE_INFO.get(state, (0, 'Unknown'))[1]}")

    st.divider()

    # Money Buttons
    st.markdown("### 💵 Insert Money")

    money_cols = st.columns(3)
    with money_cols[0]:
        if st.button("RM5", use_container_width=True, type="primary"):
            transition('RM5')
            st.rerun()
    with money_cols[1]:
        if st.button("RM10", use_container_width=True, type="primary"):
            transition('RM10')
            st.rerun()
    with money_cols[2]:
        if st.button("RM20", use_container_width=True, type="primary"):
            transition('RM20')
            st.rerun()

    st.divider()

    # Product Buttons
    st.markdown("### 🛒 Select Product")

    prod_cols = st.columns(2)
    with prod_cols[0]:
        eye_disabled = not is_accepting()
        if st.button("👁️ Eye Drop\n(RM35)", use_container_width=True, disabled=eye_disabled):
            dispensed = transition('e')
            if dispensed:
                st.balloons()
                st.toast(f"🎉 {dispensed} dispensed!")
            st.rerun()

    with prod_cols[1]:
        vit_disabled = not can_buy_vitamin()
        if st.button("💊 Vitamin\n(RM50)", use_container_width=True, disabled=vit_disabled):
            dispensed = transition('v')
            if dispensed:
                st.balloons()
                st.toast(f"🎉 {dispensed} dispensed!")
            st.rerun()

    # Info about what can be purchased
    if is_accepting():
        if can_buy_vitamin():
            st.success("Both Eye Drop and Vitamin available!")
        else:
            need = 50 - balance
            st.warning(f"Eye Drop ready! Need RM{need} more for Vitamin")
    else:
        need_eye = max(0, 35 - balance)
        need_vit = max(0, 50 - balance)
        st.info(f"Need RM{need_eye} for Eye Drop, RM{need_vit} for Vitamin")

    st.divider()

    # Reset Button
    if st.button("🔄 Reset Machine", use_container_width=True, type="secondary"):
        reset_machine()
        st.rerun()

# RIGHT COLUMN - State Diagram & History
with col_right:
    # Tabs for diagram and history
    tab1, tab2, tab3 = st.tabs(["📊 State Diagram", "📜 History", "📖 DFA Definition"])

    with tab1:
        st.markdown("### DFA State Diagram")
        st.markdown("*Current state is highlighted*")

        # Create a simple visual representation using Mermaid
        current = st.session_state.current_state

        # Build mermaid diagram
        mermaid_code = """
        stateDiagram-v2
            direction LR
            [*] --> Q0

            Q0 --> Q1 : RM5
            Q0 --> Q2 : RM10
            Q0 --> Q4 : RM20

            Q1 --> Q2 : RM5
            Q1 --> Q3 : RM10
            Q1 --> Q5 : RM20

            Q2 --> Q3 : RM5
            Q2 --> Q4 : RM10
            Q2 --> Q6 : RM20

            Q3 --> Q4 : RM5
            Q3 --> Q5 : RM10
            Q3 --> Q7 : RM20

            Q4 --> Q5 : RM5
            Q4 --> Q6 : RM10
            Q4 --> Q8 : RM20

            Q5 --> Q6 : RM5
            Q5 --> Q7 : RM10
            Q5 --> Q9 : RM20

            Q6 --> Q7 : RM5
            Q6 --> Q8 : RM10
            Q6 --> Q10 : RM20

            Q7 --> Q8 : RM5
            Q7 --> Q9 : RM10
            Q7 --> Q10 : RM20
            Q7 --> Q0 : e

            Q8 --> Q9 : RM5
            Q8 --> Q10 : RM10,RM20
            Q8 --> Q0 : e

            Q9 --> Q10 : RM5,RM10,RM20
            Q9 --> Q0 : e

            Q10 --> Q0 : e,v
        """

        st.markdown(f"""
        ```mermaid
        {mermaid_code}
        ```
        """)

        # Show state table
        st.markdown("### State Overview")

        # Create state table
        state_data = []
        for s in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']:
            balance_val, desc = STATE_INFO[s]
            is_current = "👉" if s == current else ""
            is_accept = "✅" if s in ACCEPTING_STATES else ""
            state_data.append({
                "": is_current,
                "State": s,
                "Balance": f"RM{balance_val}",
                "Accepting": is_accept,
                "Description": desc
            })

        st.dataframe(state_data, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Transition History")

        if st.session_state.history:
            # Show history in reverse (newest first)
            for i, (old, symbol, new, dispensed) in enumerate(reversed(st.session_state.history)):
                symbol_display = {
                    'RM5': '💵 RM5',
                    'RM10': '💵 RM10',
                    'RM20': '💵 RM20',
                    'e': '👁️ Eye Drop',
                    'v': '💊 Vitamin'
                }.get(symbol, symbol)

                if dispensed:
                    st.success(f"**{len(st.session_state.history) - i}.** {old} → {new} [{symbol_display}] 🎉 **{dispensed} dispensed!**")
                else:
                    st.markdown(f"**{len(st.session_state.history) - i}.** {old} → {new} [{symbol_display}]")
        else:
            st.info("No transitions yet. Insert money to begin!")

    with tab3:
        st.markdown("### Formal DFA Definition")

        st.markdown("""
        **5-tuple: (Q, Σ, δ, q₀, F)**

        | Component | Definition |
        |-----------|------------|
        | **Q** (States) | {Q0, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10} |
        | **Σ** (Alphabet) | {RM5, RM10, RM20, e, v} |
        | **δ** (Transition) | See transition table below |
        | **q₀** (Initial) | Q0 |
        | **F** (Accepting) | {Q7, Q8, Q9, Q10} |
        """)

        st.markdown("### Transition Table (δ)")

        # Create transition table
        trans_data = []
        for state in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']:
            row = {"State": state}
            for symbol in ['RM5', 'RM10', 'RM20', 'e', 'v']:
                row[symbol] = DELTA[state][symbol]
            trans_data.append(row)

        st.dataframe(trans_data, use_container_width=True, hide_index=True)

        st.markdown("""
        ### Products
        - **Eye Drop**: RM35 (available in Q7, Q8, Q9, Q10)
        - **Vitamin**: RM50 (available only in Q10)

        ### How It Works
        1. Insert money (RM5, RM10, or RM20) to accumulate balance
        2. Each state represents the total money inserted
        3. When you reach an accepting state, you can dispense products
        4. Selecting a product returns you to Q0 (initial state)
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    Healthcare Vending Machine DFA Simulation<br>
    Built with Streamlit
</div>
""", unsafe_allow_html=True)
