import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV
checkout1 = pd.read_csv("checkout_1.csv")

# Criar o gráfico
plt.figure()
plt.plot(checkout1["time"], checkout1["today"], label="Today")
plt.plot(checkout1["time"], checkout1["avg_last_week"], label="Avg Last Week")
plt.plot(checkout1["time"], checkout1["avg_last_month"], label="Avg Last Month")

plt.legend()
plt.xticks(rotation=90)
plt.title("Checkout 1 - Sales per Hour Comparison")
plt.xlabel("Hour")
plt.ylabel("Number of Sales")
plt.tight_layout()

# Salvar a imagem
plt.savefig("checkout_1_sales_comparison.png")
plt.close()
