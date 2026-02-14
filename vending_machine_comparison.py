"""
Healthcare Vending Machine - Automaton Comparison
==================================================
Compare different automaton implementations:
1. Original DFA (Single path)
2. Two-Line DFA (Parallel product paths)
3. NFA (Non-deterministic with epsilon transitions)

Products:
- Eye Drop: RM35
- Vitamin:  RM50
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

# ============================================================
# 1. ORIGINAL DFA (Single Path)
# ============================================================
class OriginalDFA:
    """Original DFA - Single shared state path."""

    NAME = "Original DFA"
    DESCRIPTION = "Single state path shared by both products"

    STATES = ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
    SIGMA = ['RM5', 'RM10', 'RM20', 'e', 'v']
    INITIAL = 'Q0'
    ACCEPTING = {'Q7', 'Q8', 'Q9', 'Q10'}

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
        'Q0': (0, 'Initial'), 'Q1': (5, 'RM5'), 'Q2': (10, 'RM10'),
        'Q3': (15, 'RM15'), 'Q4': (20, 'RM20'), 'Q5': (25, 'RM25'),
        'Q6': (30, 'RM30'), 'Q7': (35, 'Eye Drop Ready'),
        'Q8': (40, 'Eye Drop Ready'), 'Q9': (45, 'Eye Drop Ready'),
        'Q10': (50, 'Both Ready'),
    }

    def __init__(self):
        self.current_state = self.INITIAL
        self.history = []

    def transition(self, symbol):
        old = self.current_state
        new = self.DELTA.get(old, {}).get(symbol, old)
        dispensed = None
        if old in self.ACCEPTING and new == 'Q0':
            dispensed = 'Eye Drop' if symbol == 'e' else 'Vitamin' if symbol == 'v' else None
        self.current_state = new
        self.history.append((old, symbol, new))
        return old, new, dispensed

    def reset(self):
        self.current_state = self.INITIAL
        self.history = []

    def get_balance(self):
        return self.STATE_INFO.get(self.current_state, (0, ''))[0]

    def is_accepting(self):
        return self.current_state in self.ACCEPTING

    def can_buy_eye_drop(self):
        return self.current_state in self.ACCEPTING

    def can_buy_vitamin(self):
        return self.current_state == 'Q10'


# ============================================================
# 2. TWO-LINE DFA (Parallel Product Paths)
# ============================================================
class TwoLineDFA:
    """Two parallel state lines - one for each product."""

    NAME = "Two-Line DFA"
    DESCRIPTION = "Separate state paths for Eye Drop and Vitamin"

    # States: S0 = Start, E1-E7 = Eye Drop path, V1-V10 = Vitamin path
    STATES = ['S0', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7',
              'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10']
    SIGMA = ['RM5', 'RM10', 'RM20', 'e', 'v', 'select_e', 'select_v']
    INITIAL = 'S0'
    ACCEPTING_EYE = {'E7'}
    ACCEPTING_VIT = {'V10'}
    ACCEPTING = ACCEPTING_EYE | ACCEPTING_VIT

    # Transition table
    DELTA = {
        # Start - choose product first
        'S0': {'select_e': 'E1', 'select_v': 'V1', 'RM5': 'S0', 'RM10': 'S0', 'RM20': 'S0', 'e': 'S0', 'v': 'S0'},

        # Eye Drop path (need RM35)
        'E1': {'RM5': 'E2', 'RM10': 'E3', 'RM20': 'E5', 'e': 'E1', 'v': 'E1', 'select_e': 'E1', 'select_v': 'V1'},
        'E2': {'RM5': 'E3', 'RM10': 'E4', 'RM20': 'E6', 'e': 'E2', 'v': 'E2', 'select_e': 'E2', 'select_v': 'V2'},
        'E3': {'RM5': 'E4', 'RM10': 'E5', 'RM20': 'E7', 'e': 'E3', 'v': 'E3', 'select_e': 'E3', 'select_v': 'V3'},
        'E4': {'RM5': 'E5', 'RM10': 'E6', 'RM20': 'E7', 'e': 'E4', 'v': 'E4', 'select_e': 'E4', 'select_v': 'V4'},
        'E5': {'RM5': 'E6', 'RM10': 'E7', 'RM20': 'E7', 'e': 'E5', 'v': 'E5', 'select_e': 'E5', 'select_v': 'V5'},
        'E6': {'RM5': 'E7', 'RM10': 'E7', 'RM20': 'E7', 'e': 'E6', 'v': 'E6', 'select_e': 'E6', 'select_v': 'V6'},
        'E7': {'RM5': 'E7', 'RM10': 'E7', 'RM20': 'E7', 'e': 'S0', 'v': 'E7', 'select_e': 'E7', 'select_v': 'V7'},

        # Vitamin path (need RM50)
        'V1':  {'RM5': 'V2',  'RM10': 'V3',  'RM20': 'V5',  'e': 'V1',  'v': 'V1',  'select_e': 'E1',  'select_v': 'V1'},
        'V2':  {'RM5': 'V3',  'RM10': 'V4',  'RM20': 'V6',  'e': 'V2',  'v': 'V2',  'select_e': 'E2',  'select_v': 'V2'},
        'V3':  {'RM5': 'V4',  'RM10': 'V5',  'RM20': 'V7',  'e': 'V3',  'v': 'V3',  'select_e': 'E3',  'select_v': 'V3'},
        'V4':  {'RM5': 'V5',  'RM10': 'V6',  'RM20': 'V8',  'e': 'V4',  'v': 'V4',  'select_e': 'E4',  'select_v': 'V4'},
        'V5':  {'RM5': 'V6',  'RM10': 'V7',  'RM20': 'V9',  'e': 'V5',  'v': 'V5',  'select_e': 'E5',  'select_v': 'V5'},
        'V6':  {'RM5': 'V7',  'RM10': 'V8',  'RM20': 'V10', 'e': 'V6',  'v': 'V6',  'select_e': 'E6',  'select_v': 'V6'},
        'V7':  {'RM5': 'V8',  'RM10': 'V9',  'RM20': 'V10', 'e': 'V7',  'v': 'V7',  'select_e': 'E7',  'select_v': 'V7'},
        'V8':  {'RM5': 'V9',  'RM10': 'V10', 'RM20': 'V10', 'e': 'V8',  'v': 'V8',  'select_e': 'E7',  'select_v': 'V8'},
        'V9':  {'RM5': 'V10', 'RM10': 'V10', 'RM20': 'V10', 'e': 'V9',  'v': 'V9',  'select_e': 'E7',  'select_v': 'V9'},
        'V10': {'RM5': 'V10', 'RM10': 'V10', 'RM20': 'V10', 'e': 'V10', 'v': 'S0',  'select_e': 'E7',  'select_v': 'V10'},
    }

    STATE_INFO = {
        'S0': (0, 'Select Product'),
        'E1': (5, 'Eye Drop: RM5'), 'E2': (10, 'Eye Drop: RM10'), 'E3': (15, 'Eye Drop: RM15'),
        'E4': (20, 'Eye Drop: RM20'), 'E5': (25, 'Eye Drop: RM25'), 'E6': (30, 'Eye Drop: RM30'),
        'E7': (35, 'Eye Drop: READY'),
        'V1': (5, 'Vitamin: RM5'), 'V2': (10, 'Vitamin: RM10'), 'V3': (15, 'Vitamin: RM15'),
        'V4': (20, 'Vitamin: RM20'), 'V5': (25, 'Vitamin: RM25'), 'V6': (30, 'Vitamin: RM30'),
        'V7': (35, 'Vitamin: RM35'), 'V8': (40, 'Vitamin: RM40'), 'V9': (45, 'Vitamin: RM45'),
        'V10': (50, 'Vitamin: READY'),
    }

    def __init__(self):
        self.current_state = self.INITIAL
        self.history = []

    def transition(self, symbol):
        old = self.current_state
        new = self.DELTA.get(old, {}).get(symbol, old)
        dispensed = None
        if old in self.ACCEPTING_EYE and new == 'S0' and symbol == 'e':
            dispensed = 'Eye Drop'
        elif old in self.ACCEPTING_VIT and new == 'S0' and symbol == 'v':
            dispensed = 'Vitamin'
        self.current_state = new
        self.history.append((old, symbol, new))
        return old, new, dispensed

    def reset(self):
        self.current_state = self.INITIAL
        self.history = []

    def get_balance(self):
        return self.STATE_INFO.get(self.current_state, (0, ''))[0]

    def is_accepting(self):
        return self.current_state in self.ACCEPTING

    def can_buy_eye_drop(self):
        return self.current_state in self.ACCEPTING_EYE

    def can_buy_vitamin(self):
        return self.current_state in self.ACCEPTING_VIT


# ============================================================
# 3. NFA (Non-deterministic Finite Automaton)
# ============================================================
class NFASimulator:
    """NFA with epsilon transitions - can be in multiple states."""

    NAME = "NFA"
    DESCRIPTION = "Non-deterministic with epsilon (e) transitions"

    STATES = ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10',
              'EYE_READY', 'VIT_READY', 'DISPENSE']
    SIGMA = ['RM5', 'RM10', 'RM20', 'dispense_e', 'dispense_v']
    INITIAL = 'Q0'
    ACCEPTING = {'EYE_READY', 'VIT_READY'}

    # NFA transitions: state -> symbol -> set of next states
    # 'eps' = epsilon transition (no input consumed)
    DELTA = {
        'Q0':  {'RM5': {'Q1'}, 'RM10': {'Q2'}, 'RM20': {'Q4'}, 'eps': set()},
        'Q1':  {'RM5': {'Q2'}, 'RM10': {'Q3'}, 'RM20': {'Q5'}, 'eps': set()},
        'Q2':  {'RM5': {'Q3'}, 'RM10': {'Q4'}, 'RM20': {'Q6'}, 'eps': set()},
        'Q3':  {'RM5': {'Q4'}, 'RM10': {'Q5'}, 'RM20': {'Q7'}, 'eps': set()},
        'Q4':  {'RM5': {'Q5'}, 'RM10': {'Q6'}, 'RM20': {'Q8'}, 'eps': set()},
        'Q5':  {'RM5': {'Q6'}, 'RM10': {'Q7'}, 'RM20': {'Q9'}, 'eps': set()},
        'Q6':  {'RM5': {'Q7'}, 'RM10': {'Q8'}, 'RM20': {'Q10'}, 'eps': set()},
        'Q7':  {'RM5': {'Q8'}, 'RM10': {'Q9'}, 'RM20': {'Q10'}, 'eps': {'EYE_READY'}},  # epsilon to EYE_READY
        'Q8':  {'RM5': {'Q9'}, 'RM10': {'Q10'}, 'RM20': {'Q10'}, 'eps': {'EYE_READY'}},
        'Q9':  {'RM5': {'Q10'}, 'RM10': {'Q10'}, 'RM20': {'Q10'}, 'eps': {'EYE_READY'}},
        'Q10': {'RM5': {'Q10'}, 'RM10': {'Q10'}, 'RM20': {'Q10'}, 'eps': {'EYE_READY', 'VIT_READY'}},
        'EYE_READY': {'dispense_e': {'DISPENSE'}, 'eps': set()},
        'VIT_READY': {'dispense_v': {'DISPENSE'}, 'eps': set()},
        'DISPENSE': {'eps': {'Q0'}},  # Return to start
    }

    STATE_INFO = {
        'Q0': (0, 'Initial'), 'Q1': (5, 'RM5'), 'Q2': (10, 'RM10'),
        'Q3': (15, 'RM15'), 'Q4': (20, 'RM20'), 'Q5': (25, 'RM25'),
        'Q6': (30, 'RM30'), 'Q7': (35, 'RM35'), 'Q8': (40, 'RM40'),
        'Q9': (45, 'RM45'), 'Q10': (50, 'RM50'),
        'EYE_READY': (0, 'Eye Drop Ready'), 'VIT_READY': (0, 'Vitamin Ready'),
        'DISPENSE': (0, 'Dispensing...'),
    }

    def __init__(self):
        self.current_states = {self.INITIAL}
        self.history = []
        self._apply_epsilon_closure()

    def _epsilon_closure(self, states):
        """Compute epsilon closure of a set of states."""
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for next_state in self.DELTA.get(state, {}).get('eps', set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def _apply_epsilon_closure(self):
        """Apply epsilon closure to current states."""
        self.current_states = self._epsilon_closure(self.current_states)

    def transition(self, symbol):
        old_states = self.current_states.copy()
        new_states = set()

        for state in self.current_states:
            next_states = self.DELTA.get(state, {}).get(symbol, set())
            new_states.update(next_states)

        if new_states:
            self.current_states = self._epsilon_closure(new_states)

        # Check for dispense
        dispensed = None
        if 'DISPENSE' in self.current_states:
            if symbol == 'dispense_e':
                dispensed = 'Eye Drop'
            elif symbol == 'dispense_v':
                dispensed = 'Vitamin'
            # Reset after dispense
            self.current_states = self._epsilon_closure({'Q0'})

        self.history.append((old_states, symbol, self.current_states.copy()))
        return old_states, self.current_states.copy(), dispensed

    def reset(self):
        self.current_states = {self.INITIAL}
        self._apply_epsilon_closure()
        self.history = []

    def get_balance(self):
        # Return max balance from current states
        max_bal = 0
        for state in self.current_states:
            bal = self.STATE_INFO.get(state, (0, ''))[0]
            if bal > max_bal:
                max_bal = bal
        return max_bal

    def is_accepting(self):
        return bool(self.current_states & self.ACCEPTING)

    def can_buy_eye_drop(self):
        return 'EYE_READY' in self.current_states

    def can_buy_vitamin(self):
        return 'VIT_READY' in self.current_states

    @property
    def current_state(self):
        """For compatibility - return string representation of current states."""
        return ', '.join(sorted(self.current_states))


# ============================================================
# GUI WITH TABS
# ============================================================
class ComparisonGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vending Machine - Automaton Comparison")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f5f5f5')

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs for each automaton
        self.tabs = {}
        self.machines = {}

        automaton_classes = [OriginalDFA, TwoLineDFA, NFASimulator]

        for cls in automaton_classes:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=cls.NAME)
            self.tabs[cls.NAME] = tab
            self.machines[cls.NAME] = cls()
            self.create_tab_content(tab, cls)

    def create_tab_content(self, tab, automaton_class):
        """Create content for a tab."""
        machine = self.machines[automaton_class.NAME]

        # Main frame
        main_frame = tk.Frame(tab, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Controls
        control_frame = tk.Frame(main_frame, bg='#f5f5f5', width=350)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)

        # Title
        title_frame = tk.Frame(control_frame, bg='#1976D2', pady=10)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text=automaton_class.NAME,
                font=('Arial', 16, 'bold'), bg='#1976D2', fg='white').pack()
        tk.Label(title_frame, text=automaton_class.DESCRIPTION,
                font=('Arial', 9), bg='#1976D2', fg='#BBDEFB').pack()

        # State display
        state_frame = tk.LabelFrame(control_frame, text="Current State",
                                   font=('Arial', 10, 'bold'), padx=10, pady=10, bg='white')
        state_frame.pack(fill=tk.X, pady=10)

        state_label = tk.Label(state_frame, text=machine.current_state,
                              font=('Arial', 24, 'bold'), fg='#1976D2', bg='white')
        state_label.pack()

        status_label = tk.Label(state_frame, text="[REJECT]",
                               font=('Arial', 11, 'bold'), fg='#757575', bg='white')
        status_label.pack()

        balance_label = tk.Label(state_frame, text=f"Balance: RM{machine.get_balance()}",
                                font=('Arial', 14), fg='#333', bg='white')
        balance_label.pack(pady=5)

        # Store labels for updating
        tab.state_label = state_label
        tab.status_label = status_label
        tab.balance_label = balance_label

        # For Two-Line DFA, add product selection buttons
        if automaton_class == TwoLineDFA:
            select_frame = tk.LabelFrame(control_frame, text="Select Product First",
                                        font=('Arial', 10, 'bold'), padx=10, pady=5, bg='white')
            select_frame.pack(fill=tk.X, pady=5)

            sel_cols = tk.Frame(select_frame, bg='white')
            sel_cols.pack()

            tk.Button(sel_cols, text="Eye Drop\nPath", font=('Arial', 10, 'bold'),
                     width=10, height=2, bg='#FF9800', fg='white',
                     command=lambda: self.process_input(automaton_class.NAME, 'select_e')
                     ).pack(side=tk.LEFT, padx=5, pady=5)

            tk.Button(sel_cols, text="Vitamin\nPath", font=('Arial', 10, 'bold'),
                     width=10, height=2, bg='#E91E63', fg='white',
                     command=lambda: self.process_input(automaton_class.NAME, 'select_v')
                     ).pack(side=tk.LEFT, padx=5, pady=5)

        # Money buttons
        money_frame = tk.LabelFrame(control_frame, text="Insert Money",
                                   font=('Arial', 10, 'bold'), padx=10, pady=5, bg='white')
        money_frame.pack(fill=tk.X, pady=5)

        btn_frame = tk.Frame(money_frame, bg='white')
        btn_frame.pack()

        for amount, color in [('RM5', '#4CAF50'), ('RM10', '#2196F3'), ('RM20', '#9C27B0')]:
            tk.Button(btn_frame, text=amount, font=('Arial', 12, 'bold'),
                     width=6, height=2, bg=color, fg='white', cursor='hand2',
                     command=lambda a=amount, n=automaton_class.NAME: self.process_input(n, a)
                     ).pack(side=tk.LEFT, padx=3, pady=5)

        # Product buttons
        product_frame = tk.LabelFrame(control_frame, text="Dispense Product",
                                     font=('Arial', 10, 'bold'), padx=10, pady=5, bg='white')
        product_frame.pack(fill=tk.X, pady=5)

        prod_cols = tk.Frame(product_frame, bg='white')
        prod_cols.pack()

        # Determine dispense symbols based on automaton type
        eye_symbol = 'dispense_e' if automaton_class == NFASimulator else 'e'
        vit_symbol = 'dispense_v' if automaton_class == NFASimulator else 'v'

        eye_btn = tk.Button(prod_cols, text="Eye Drop\n(RM35)",
                           font=('Arial', 11, 'bold'), width=10, height=2,
                           bg='#FF9800', fg='white', cursor='hand2',
                           command=lambda: self.process_input(automaton_class.NAME, eye_symbol))
        eye_btn.pack(side=tk.LEFT, padx=5, pady=5)
        tab.eye_btn = eye_btn

        vit_btn = tk.Button(prod_cols, text="Vitamin\n(RM50)",
                           font=('Arial', 11, 'bold'), width=10, height=2,
                           bg='#E91E63', fg='white', cursor='hand2',
                           command=lambda: self.process_input(automaton_class.NAME, vit_symbol))
        vit_btn.pack(side=tk.LEFT, padx=5, pady=5)
        tab.vit_btn = vit_btn

        # History
        history_frame = tk.LabelFrame(control_frame, text="Transition History",
                                     font=('Arial', 10, 'bold'), padx=5, pady=5, bg='white')
        history_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        history_text = tk.Text(history_frame, height=6, font=('Consolas', 8),
                              state=tk.DISABLED, bg='#FAFAFA', relief=tk.FLAT)
        scrollbar = tk.Scrollbar(history_frame, command=history_text.yview)
        history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_text.pack(fill=tk.BOTH, expand=True)
        tab.history_text = history_text

        # Reset button
        tk.Button(control_frame, text="Reset", font=('Arial', 10),
                 bg='#f44336', fg='white', cursor='hand2', pady=5,
                 command=lambda: self.reset_machine(automaton_class.NAME)
                 ).pack(fill=tk.X, pady=5)

        # Right panel - Diagram
        diagram_frame = tk.LabelFrame(main_frame, text="State Diagram",
                                     font=('Arial', 11, 'bold'), bg='white', padx=5, pady=5)
        diagram_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(diagram_frame, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        tab.canvas = canvas

        # Bind resize
        canvas.bind('<Configure>', lambda e, n=automaton_class.NAME: self.draw_diagram(n))

        # Initial update
        self.update_display(automaton_class.NAME)

    def process_input(self, name, symbol):
        """Process input for a specific automaton."""
        machine = self.machines[name]
        old, new, dispensed = machine.transition(symbol)

        # Log
        tab = self.tabs[name]
        tab.history_text.config(state=tk.NORMAL)

        if isinstance(machine, NFASimulator):
            old_str = ', '.join(sorted(old)) if isinstance(old, set) else old
            new_str = ', '.join(sorted(new)) if isinstance(new, set) else new
        else:
            old_str, new_str = old, new

        tab.history_text.insert(tk.END, f"  {old_str} --[{symbol}]--> {new_str}\n")
        tab.history_text.see(tk.END)
        tab.history_text.config(state=tk.DISABLED)

        if dispensed:
            messagebox.showinfo("Dispensed!", f"{dispensed} has been dispensed!")

        self.update_display(name)

    def reset_machine(self, name):
        """Reset a specific automaton."""
        machine = self.machines[name]
        machine.reset()

        tab = self.tabs[name]
        tab.history_text.config(state=tk.NORMAL)
        tab.history_text.delete(1.0, tk.END)
        tab.history_text.insert(tk.END, "--- Reset ---\n")
        tab.history_text.config(state=tk.DISABLED)

        self.update_display(name)

    def update_display(self, name):
        """Update display for a specific automaton."""
        machine = self.machines[name]
        tab = self.tabs[name]

        # Update state label
        if isinstance(machine, NFASimulator):
            state_text = '\n'.join(sorted(machine.current_states))
        else:
            state_text = machine.current_state

        tab.state_label.config(text=state_text)

        # Update status
        if machine.is_accepting():
            tab.state_label.config(fg='#4CAF50')
            tab.status_label.config(text="[ACCEPT]", fg='#4CAF50')
        else:
            tab.state_label.config(fg='#1976D2')
            tab.status_label.config(text="[REJECT]", fg='#757575')

        # Update balance
        tab.balance_label.config(text=f"Balance: RM{machine.get_balance()}")

        # Update buttons
        can_eye = machine.can_buy_eye_drop()
        can_vit = machine.can_buy_vitamin()
        tab.eye_btn.config(bg='#4CAF50' if can_eye else '#FF9800')
        tab.vit_btn.config(bg='#4CAF50' if can_vit else '#E91E63')

        # Redraw diagram
        self.draw_diagram(name)

    def draw_diagram(self, name):
        """Draw state diagram for specific automaton."""
        machine = self.machines[name]
        tab = self.tabs[name]
        canvas = tab.canvas

        canvas.delete("all")

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w < 50 or h < 50:
            return

        # Get current state(s)
        if isinstance(machine, NFASimulator):
            current = machine.current_states
        else:
            current = {machine.current_state}

        # Draw based on automaton type
        if isinstance(machine, OriginalDFA):
            self.draw_original_dfa(canvas, w, h, machine, current)
        elif isinstance(machine, TwoLineDFA):
            self.draw_twoline_dfa(canvas, w, h, machine, current)
        elif isinstance(machine, NFASimulator):
            self.draw_nfa(canvas, w, h, machine, current)

    def draw_arrow(self, canvas, x1, y1, x2, y2, label, active=False, arrow_type='RM5'):
        """Draw an arrow between two points with active/inactive coloring."""
        # Color scheme based on arrow type
        if active:
            if arrow_type == 'RM5' or 'RM5' in label:
                color = '#4CAF50'  # Green
            elif arrow_type == 'RM10' or 'RM10' in label:
                color = '#2196F3'  # Blue
            elif arrow_type == 'RM20' or 'RM20' in label:
                color = '#9C27B0'  # Purple
            elif arrow_type == 'return':
                color = '#F44336'  # Red
            elif arrow_type == 'self':
                color = '#FF9800'  # Orange
            else:
                color = '#4CAF50'
            width = 2.5
            text_color = color
        else:
            color = '#E0E0E0'  # Grey inactive
            width = 1
            text_color = '#BDBDBD'

        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color, width=width,
                          arrowshape=(10, 12, 4))

        # Label at midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 - 10
        label_font = ('Arial', 8, 'bold') if active else ('Arial', 7)
        canvas.create_text(mid_x, mid_y, text=label, font=label_font, fill=text_color)

    def draw_curved_arrow(self, canvas, x1, y1, x2, y2, label, active=False, arrow_type='RM5', curve_offset=30):
        """Draw a curved arrow with bezier curve."""
        if active:
            if 'RM5' in label:
                color = '#4CAF50'
            elif 'RM10' in label:
                color = '#2196F3'
            elif 'RM20' in label:
                color = '#9C27B0'
            elif arrow_type == 'return':
                color = '#F44336'
            else:
                color = '#4CAF50'
            width = 2.5
            text_color = color
        else:
            color = '#E0E0E0'
            width = 1
            text_color = '#BDBDBD'

        # Control point for curve
        ctrl_x = (x1 + x2) / 2
        ctrl_y = (y1 + y2) / 2 + curve_offset

        # Generate bezier points
        points = []
        for i in range(21):
            t = i / 20.0
            px = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
            py = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2
            points.extend([px, py])

        if len(points) >= 4:
            canvas.create_line(points, smooth=True, fill=color, width=width,
                              arrow=tk.LAST, arrowshape=(10, 12, 4))

        # Label
        label_x = ctrl_x
        label_y = ctrl_y + (10 if curve_offset >= 0 else -10)
        label_font = ('Arial', 8, 'bold') if active else ('Arial', 7)
        canvas.create_text(label_x, label_y, text=label, font=label_font, fill=text_color)

    def draw_self_loop(self, canvas, x, y, r, label, active=False, position='top'):
        """Draw a self-loop on a state with consistent sizing."""
        if active:
            color = '#FF9800'  # Orange for self-loops
            text_color = '#E65100'
            width = 2.2
        else:
            color = '#E0E0E0'
            text_color = '#BDBDBD'
            width = 1

        loop_size = max(16, int(r * 0.85))
        font = ('Arial', 8, 'bold') if active else ('Arial', 7)

        def draw_arrowhead(xh, yh, dx, dy):
            length = math.hypot(dx, dy)
            if length == 0:
                return
            ux, uy = dx / length, dy / length
            size = 7
            angle = math.pi / 6
            ax1 = xh - size * (ux * math.cos(angle) - uy * math.sin(angle))
            ay1 = yh - size * (uy * math.cos(angle) + ux * math.sin(angle))
            ax2 = xh - size * (ux * math.cos(angle) + uy * math.sin(angle))
            ay2 = yh - size * (uy * math.cos(angle) - ux * math.sin(angle))
            canvas.create_polygon(xh, yh, ax1, ay1, ax2, ay2, fill=color, outline=color)

        if position == 'top':
            start_x = x - r * 0.7
            start_y = y - r * 0.7
            end_x = x + r * 0.7
            end_y = y - r * 0.7
            ctrl1_x = x - loop_size
            ctrl1_y = y - r - loop_size * 1.6
            ctrl2_x = x + loop_size
            ctrl2_y = y - r - loop_size * 1.6

            points = []
            for t in [i / 20.0 for i in range(21)]:
                px = (1-t)**3 * start_x + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * end_x
                py = (1-t)**3 * start_y + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * end_y
                points.extend([px, py])

            canvas.create_line(points, smooth=True, fill=color, width=width)
            draw_arrowhead(end_x, end_y, end_x - ctrl2_x, end_y - ctrl2_y)
            canvas.create_text(x, y - r - loop_size * 1.8, text=label, font=font, fill=text_color)
        elif position == 'right':
            start_x = x + r * 0.7
            start_y = y - r * 0.5
            end_x = x + r * 0.7
            end_y = y + r * 0.5
            ctrl1_x = x + r + loop_size * 1.5
            ctrl1_y = y - loop_size
            ctrl2_x = x + r + loop_size * 1.5
            ctrl2_y = y + loop_size

            points = []
            for t in [i / 20.0 for i in range(21)]:
                px = (1-t)**3 * start_x + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * end_x
                py = (1-t)**3 * start_y + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * end_y
                points.extend([px, py])

            canvas.create_line(points, smooth=True, fill=color, width=width)
            draw_arrowhead(end_x, end_y, end_x - ctrl2_x, end_y - ctrl2_y)
            canvas.create_text(x + r + loop_size * 2, y, text=label, font=font, fill=text_color, anchor='w')
        elif position == 'bottom':
            start_x = x + r * 0.7
            start_y = y + r * 0.7
            end_x = x - r * 0.7
            end_y = y + r * 0.7
            ctrl1_x = x + loop_size
            ctrl1_y = y + r + loop_size * 1.5
            ctrl2_x = x - loop_size
            ctrl2_y = y + r + loop_size * 1.5

            points = []
            for t in [i / 20.0 for i in range(21)]:
                px = (1-t)**3 * start_x + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * end_x
                py = (1-t)**3 * start_y + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * end_y
                points.extend([px, py])

            canvas.create_line(points, smooth=True, fill=color, width=width)
            draw_arrowhead(end_x, end_y, end_x - ctrl2_x, end_y - ctrl2_y)
            canvas.create_text(x, y + r + loop_size * 2.0, text=label, font=font, fill=text_color)

    def draw_return_arrow(self, canvas, x1, y1, x0, y0, r, label, active=False, offset=50):
        """Draw return arrow from accepting state to Q0."""
        if active:
            color = '#F44336'  # Red
            text_color = '#C62828'
            width = 2.5
        else:
            color = '#E0E0E0'
            text_color = '#BDBDBD'
            width = 1

        # Curved path back to Q0
        ctrl_y = max(y1, y0) + offset

        points = []
        start_x, start_y = x1 - r, y1 + r * 0.5
        end_x, end_y = x0, y0 + r
        ctrl1_x, ctrl1_y = x1 - r - 20, ctrl_y
        ctrl2_x, ctrl2_y = x0 + 20, ctrl_y

        for i in range(21):
            t = i / 20.0
            px = (1-t)**3 * start_x + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * end_x
            py = (1-t)**3 * start_y + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * end_y
            points.extend([px, py])

        canvas.create_line(points, smooth=True, fill=color, width=width,
                          arrow=tk.LAST, arrowshape=(10, 12, 4))
        label_font = ('Arial', 8, 'bold') if active else ('Arial', 7)
        canvas.create_text(start_x - 15, start_y + 15, text=label,
                          font=label_font, fill=text_color)

    def draw_original_dfa(self, canvas, w, h, machine, current):
        """Draw Original DFA diagram with active/inactive arrows."""
        r = 22

        # Position states in two rows
        positions = {}

        # Q0-Q6 in top row
        for i in range(7):
            x = 60 + i * (w - 140) / 6
            y = h * 0.25
            positions[f'Q{i}'] = (x, y)

        # Q7-Q10 in bottom row
        for i, state in enumerate(['Q7', 'Q8', 'Q9', 'Q10']):
            x = 60 + (i + 3) * (w - 140) / 6
            y = h * 0.65
            positions[state] = (x, y)

        current_state = list(current)[0] if current else 'Q0'

        # Draw RM5 transitions (green) - horizontal in top row
        for i in range(6):
            from_s, to_s = f'Q{i}', f'Q{i+1}'
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_arrow(canvas, x1 + r, y1, x2 - r, y2, 'RM5', active, 'RM5')

        # Draw RM5 transitions in accepting states
        for from_s, to_s in [('Q7', 'Q8'), ('Q8', 'Q9'), ('Q9', 'Q10')]:
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_arrow(canvas, x1 + r, y1, x2 - r, y2, 'RM5', active, 'RM5')

        # Draw RM10 transitions (blue) - skip one state
        rm10_transitions = [('Q0', 'Q2'), ('Q1', 'Q3'), ('Q2', 'Q4'), ('Q3', 'Q5'),
                           ('Q4', 'Q6'), ('Q5', 'Q7'), ('Q6', 'Q8'),
                           ('Q7', 'Q9'), ('Q8', 'Q10')]
        for from_s, to_s in rm10_transitions:
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_curved_arrow(canvas, x1, y1 + r, x2, y2 - r if y2 > y1 else y2 + r,
                                  'RM10', active, 'RM10', 20 if y1 == y2 else -20)

        # Draw RM20 transitions (purple) - skip two states
        rm20_transitions = [('Q0', 'Q4'), ('Q1', 'Q5'), ('Q2', 'Q6'), ('Q3', 'Q7'),
                           ('Q4', 'Q8'), ('Q5', 'Q9'), ('Q6', 'Q10')]
        for from_s, to_s in rm20_transitions:
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_curved_arrow(canvas, x1, y1 + r, x2, y2 - r if y2 > y1 else y2 + r,
                                  'RM20', active, 'RM20', 40)

        # Draw self-loops for e,v on non-accepting states
        for i in range(7):
            state = f'Q{i}'
            x, y = positions[state]
            active = current_state == state
            self.draw_self_loop(canvas, x, y, r, 'e,v', active, 'top')

        # Draw return arrows from accepting states
        x0, y0 = positions['Q0']
        for state in ['Q7', 'Q8', 'Q9', 'Q10']:
            x1, y1 = positions[state]
            active = current_state == state
            label = 'e' if state != 'Q10' else 'e,v'
            offset = {'Q7': 40, 'Q8': 60, 'Q9': 80, 'Q10': 100}.get(state, 50)
            self.draw_return_arrow(canvas, x1, y1, x0, y0, r, label, active, offset)

        # Draw v self-loops on Q7-Q9
        for state in ['Q7', 'Q8', 'Q9']:
            x, y = positions[state]
            active = current_state == state
            self.draw_self_loop(canvas, x, y, r, 'v', active, 'right')

        # Money self-loop on Q10
        x10, y10 = positions['Q10']
        active = current_state == 'Q10'
        self.draw_self_loop(canvas, x10, y10, r, 'RM*', active, 'right')

        # Draw states (on top of arrows)
        for state, (x, y) in positions.items():
            is_current = state in current
            is_accepting = state in machine.ACCEPTING

            fill = '#4CAF50' if is_current and is_accepting else '#2196F3' if is_current else 'white'
            outline = '#333'
            text_color = 'white' if is_current else '#333'

            if is_accepting:
                canvas.create_oval(x-r-4, y-r-4, x+r+4, y+r+4, outline=outline, width=2)

            canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=2)
            canvas.create_text(x, y, text=state, font=('Arial', 9, 'bold'), fill=text_color)

        # Draw initial arrow
        x0, y0 = positions['Q0']
        canvas.create_line(x0 - r - 30, y0, x0 - r - 2, y0, arrow=tk.LAST, width=2, fill='#333')

    def draw_twoline_dfa(self, canvas, w, h, machine, current):
        """Draw Two-Line DFA diagram with active/inactive arrows."""
        r = 18

        positions = {}

        # Start state
        positions['S0'] = (50, h / 2)

        # Eye Drop path (top row) - E1 to E7
        for i in range(1, 8):
            x = 100 + i * (w - 180) / 8
            y = h * 0.28
            positions[f'E{i}'] = (x, y)

        # Vitamin path (bottom row) - V1 to V10
        for i in range(1, 11):
            x = 80 + i * (w - 150) / 11
            y = h * 0.72
            positions[f'V{i}'] = (x, y)

        current_state = list(current)[0] if current else 'S0'

        # Draw selection arrows from S0
        x0, y0 = positions['S0']
        xe1, ye1 = positions['E1']
        xv1, yv1 = positions['V1']

        # S0 -> E1 (select eye drop)
        active = current_state == 'S0'
        self.draw_curved_arrow(canvas, x0 + r, y0 - r*0.5, xe1 - r, ye1 + r*0.5,
                              'select_e', active, 'select', -30)

        # S0 -> V1 (select vitamin)
        self.draw_curved_arrow(canvas, x0 + r, y0 + r*0.5, xv1 - r, yv1 - r*0.5,
                              'select_v', active, 'select', 30)

        # Draw Eye Drop path transitions (E1 -> E7)
        for i in range(1, 7):
            from_s, to_s = f'E{i}', f'E{i+1}'
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_arrow(canvas, x1 + r, y1, x2 - r, y2, 'RM5', active, 'RM5')

        # Draw Vitamin path transitions (V1 -> V10)
        for i in range(1, 10):
            from_s, to_s = f'V{i}', f'V{i+1}'
            x1, y1 = positions[from_s]
            x2, y2 = positions[to_s]
            active = current_state == from_s
            self.draw_arrow(canvas, x1 + r, y1, x2 - r, y2, 'RM5', active, 'RM5')

        # Draw return arrows from accepting states
        # E7 -> S0 (dispense eye drop)
        xe7, ye7 = positions['E7']
        active = current_state == 'E7'
        self.draw_return_arrow(canvas, xe7, ye7, x0, y0, r, 'e', active, 50)

        # V10 -> S0 (dispense vitamin)
        xv10, yv10 = positions['V10']
        active = current_state == 'V10'
        self.draw_return_arrow(canvas, xv10, yv10, x0, y0, r, 'v', active, 70)

        # Draw states (on top of arrows)
        for state, (x, y) in positions.items():
            is_current = state in current
            is_accepting = state in machine.ACCEPTING

            # Color based on path
            if state.startswith('E'):
                base_color = '#FF9800'
            elif state.startswith('V'):
                base_color = '#E91E63'
            else:
                base_color = '#2196F3'

            fill = base_color if is_current else 'white'
            text_color = 'white' if is_current else '#333'

            if is_accepting:
                canvas.create_oval(x-r-4, y-r-4, x+r+4, y+r+4, outline='#333', width=2)

            canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline='#333', width=2)
            canvas.create_text(x, y, text=state, font=('Arial', 8, 'bold'), fill=text_color)

        # Draw initial arrow to S0
        canvas.create_line(x0 - r - 25, y0, x0 - r - 2, y0, arrow=tk.LAST, width=2, fill='#333')

        # Labels
        canvas.create_text(w/2, 15, text="Eye Drop Path (RM35)", font=('Arial', 10, 'bold'), fill='#FF9800')
        canvas.create_text(w/2, h - 8, text="Vitamin Path (RM50)", font=('Arial', 10, 'bold'), fill='#E91E63')

    def draw_nfa(self, canvas, w, h, machine, current):
        """Draw NFA diagram."""
        r = 20

        positions = {}

        # Money states in a row
        for i in range(11):
            x = 40 + i * (w - 120) / 10
            y = h * 0.35
            positions[f'Q{i}'] = (x, y)

        # Ready states
        positions['EYE_READY'] = (w * 0.3, h * 0.7)
        positions['VIT_READY'] = (w * 0.7, h * 0.7)
        positions['DISPENSE'] = (w * 0.5, h * 0.85)

        # Draw epsilon transitions (dashed)
        for state in ['Q7', 'Q8', 'Q9', 'Q10']:
            if state in positions:
                x1, y1 = positions[state]
                x2, y2 = positions['EYE_READY']
                canvas.create_line(x1, y1 + r, x2, y2 - r, dash=(4, 2), fill='#FF9800', arrow=tk.LAST)

        x1, y1 = positions['Q10']
        x2, y2 = positions['VIT_READY']
        canvas.create_line(x1, y1 + r, x2, y2 - r, dash=(4, 2), fill='#E91E63', arrow=tk.LAST)

        # Draw states
        for state, (x, y) in positions.items():
            is_current = state in current
            is_accepting = state in machine.ACCEPTING

            if state == 'EYE_READY':
                base_color = '#FF9800'
            elif state == 'VIT_READY':
                base_color = '#E91E63'
            elif state == 'DISPENSE':
                base_color = '#4CAF50'
            else:
                base_color = '#2196F3'

            fill = base_color if is_current else 'white'
            text_color = 'white' if is_current else '#333'

            if is_accepting:
                canvas.create_oval(x-r-4, y-r-4, x+r+4, y+r+4, outline='#333', width=2)

            canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline='#333', width=2)

            # Shorter labels
            label = state.replace('_READY', '').replace('DISPENSE', 'DISP')
            canvas.create_text(x, y, text=label, font=('Arial', 7, 'bold'), fill=text_color)

        # NFA indicator
        canvas.create_text(w/2, 15, text="NFA: Can be in multiple states (epsilon transitions shown dashed)",
                          font=('Arial', 9, 'italic'), fill='#666')

        # Current states indicator
        states_str = ', '.join(sorted(current))
        canvas.create_text(w/2, h - 5, text=f"Current: {{{states_str}}}",
                          font=('Arial', 9, 'bold'), fill='#1976D2')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ComparisonGUI()
    app.run()
