import matplotlib.pyplot as plt

# Data
activations = ['ReLU', 'GELU', 'SiLU', 'tanh']
values = [52.62, 51, 61.83, 25]

# Colors: SiLU만 강조
colors = ['lightgray', 'lightgray', 'cornflowerblue', 'lightgray']

# Plot
plt.figure(figsize=(7, 5))
bars = plt.bar(activations, values, color=colors)

# Labels
plt.xlabel('Activation Function')
plt.ylabel('pred(|y - pred| ≤ 0.02)')
plt.ylim(0, 100)

# Value annotation
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f'{height:.2f}',
        ha='center',
        va='bottom',
        fontsize=10
    )

# Title
plt.title('Activation Function Comparison')

plt.tight_layout()
plt.show()
