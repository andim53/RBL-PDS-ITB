# general lib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# fuzzy
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# time ani
import time

# data and smol klining
df = pd.read_csv("BBCA.csv")

df1 = df.iloc[4882:5145]
print(df1.head())
print(df1.tail())

df_pakai = df1['close']
print(df_pakai)
df_pakai = df_pakai.values.tolist()
print(df_pakai)

# inisiasi global dan lokal

df_global = []
i = 0
while i < 100:
    df_global.append(df_pakai[i])
    i += 1
print(df_global)

df_lokal = []
i = 30
while i > 0:
    df_lokal.append(df_global[len(df_global)-i])
    i -= 1
    
print(df_lokal)

# hasil fuzzy

fuzzy = []

# loop

i = len(df_global)
while i < len(df_pakai):
    
    # update dulu
    df_global.append(df_pakai[i])
    del df_lokal[0]
    df_lokal.append(df_global[-1])
    
    # fibonacci
    max_global = max(df_global)
    min_global = min(df_global)
    fib_global = abs(df_global[-1]-0.618*(max_global-min_global))/(max_global-0.618*(max_global-min_global))*100
    
    max_lokal = max(df_lokal)
    min_lokal = min(df_lokal)
    fib_lokal = abs(df_lokal[-1]-0.618*(max_lokal-min_lokal))/(max_lokal-0.618*(max_lokal-min_lokal))*100
    
    # fuzzy logic
    # Create the fuzzy variables and membership functions
    fibonacci_retracement_global = ctrl.Antecedent(np.arange(0, 101, 1), 'fibonacci_retracement_global')
    fibonacci_retracement_lokal = ctrl.Antecedent(np.arange(0, 101, 1), 'fibonacci_retracement_lokal')
    decision = ctrl.Consequent(np.arange(0, 101, 1), 'decision')
    
    
    # Define the membership functions for the variables
    fibonacci_retracement_global['close'] = fuzz.trimf(fibonacci_retracement_global.universe, [0, 0, 80])
    fibonacci_retracement_global['medium'] = fuzz.trimf(fibonacci_retracement_global.universe, [20, 50, 80])
    fibonacci_retracement_global['far'] = fuzz.trimf(fibonacci_retracement_global.universe, [80, 100, 100])
    
    fibonacci_retracement_lokal['close'] = fuzz.trimf(fibonacci_retracement_lokal.universe, [0, 0, 50])
    fibonacci_retracement_lokal['medium'] = fuzz.trimf(fibonacci_retracement_lokal.universe, [30, 50, 70])
    fibonacci_retracement_lokal['far'] = fuzz.trimf(fibonacci_retracement_lokal.universe, [50, 100, 100])
    
    decision['sell'] = fuzz.trimf(decision.universe, [0, 0, 50])
    decision['neutral'] = fuzz.trimf(decision.universe, [0, 50, 100])
    decision['buy'] = fuzz.trimf(decision.universe, [50, 100, 100])
    
    # Define the fuzzy rules to be updated as times goes on
    rules = [
        ctrl.Rule(fibonacci_retracement_global['close'] & fibonacci_retracement_lokal['close'], decision['buy']),
        ctrl.Rule(fibonacci_retracement_global['close'] & fibonacci_retracement_lokal['medium'], decision['buy']),
        ctrl.Rule(fibonacci_retracement_global['close'] & fibonacci_retracement_lokal['far'], decision['neutral']),
        
        ctrl.Rule(fibonacci_retracement_global['medium'] & fibonacci_retracement_lokal['close'], decision['buy']),
        ctrl.Rule(fibonacci_retracement_global['medium'] & fibonacci_retracement_lokal['medium'], decision['neutral']),
        ctrl.Rule(fibonacci_retracement_global['medium'] & fibonacci_retracement_lokal['far'], decision['sell']),
        
        ctrl.Rule(fibonacci_retracement_global['far'] & fibonacci_retracement_lokal['close'], decision['neutral']),
        ctrl.Rule(fibonacci_retracement_global['far'] & fibonacci_retracement_lokal['medium'], decision['sell']),
        ctrl.Rule(fibonacci_retracement_global['far'] & fibonacci_retracement_lokal['far'], decision['sell'])
    ]
    
    # Create the fuzzy control system
    decision_ctrl = ctrl.ControlSystem(rules)
    decision_calc = ctrl.ControlSystemSimulation(decision_ctrl)
    
    # Pass inputs and compute the decision
    decision_calc.input['fibonacci_retracement_global'] = fib_global
    decision_calc.input['fibonacci_retracement_lokal'] = fib_lokal
    
    # plotting
    garis_global = []
    garis_lokal = []
    sbx = []
    j = 0
    while j < len(df_global):
        sbx.append(j)
        garis_global.append(max_global-0.618*(max_global-min_global))
        garis_lokal.append(max_lokal-0.618*(max_lokal-min_lokal))
        j += 1
        
    
    plt.plot(sbx, df_global)
    plt.plot(sbx, garis_global)
    plt.plot(sbx, garis_lokal)
    plt.legend(["price", "fibonacci", "local fibonacci"])
    plt.show()
    time.sleep(0.25)
    
    # Compute the decision and place it in list
    decision_calc.compute()
    fuzzy.append(decision_calc.output['decision'])
    
    # loop control
    i += 1
    
print(fuzzy)