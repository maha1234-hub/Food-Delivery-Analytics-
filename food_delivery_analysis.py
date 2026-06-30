# ============================================================
# 🍔 Food Delivery Analytics — Advanced Project
# Tools: Python | Pandas | Matplotlib | Seaborn
# Author: Mahalakshmi P | Data Analytics
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': '#0F1115',
    'axes.facecolor': '#1A1D24',
    'text.color': '#F0F2F5',
    'axes.labelcolor': '#9BA1AC',
    'xtick.color': '#9BA1AC',
    'ytick.color': '#9BA1AC',
    'axes.edgecolor': '#2C3038',
    'grid.color': '#23262E',
    'grid.alpha': 0.5,
})

ORANGE = '#FF6B35'
GREEN  = '#06D6A0'
COLORS = ['#FF6B35','#06D6A0','#FFD23F','#EE4266','#3A86FF','#8338EC','#FB5607','#06A77D']

# ── 1. Dataset ───────────────────────────────────────────────
print("🍔 Loading Food Delivery dataset...")

cities       = ['Coimbatore','Chennai','Bangalore','Hyderabad','Mumbai']
cuisines     = ['South Indian','North Indian','Chinese','Fast Food','Biryani','Desserts','Pizza']
order_types  = ['Veg','Non-Veg']

np.random.seed(11)
n = 500
rows = []
for i in range(n):
    city = np.random.choice(cities)
    cuisine = np.random.choice(cuisines)
    order_type = np.random.choice(order_types, p=[0.55, 0.45])
    order_value = round(np.random.exponential(220) + 80, 2)
    delivery_time = int(np.clip(np.random.normal(32, 10), 10, 75))
    rating = round(np.clip(np.random.normal(4.1, 0.6), 1.0, 5.0), 1)
    discount_pct = np.random.choice([0, 10, 20, 30, 40], p=[0.25,0.25,0.25,0.15,0.10])
    hour = np.random.choice(range(24), p=_p if (_p:=np.array(
        [1,1,1,1,1,1,2,3,4,5,6,8,10,8,5,4,5,6,8,10,9,6,3,2]
    )/sum([1,1,1,1,1,1,2,3,4,5,6,8,10,8,5,4,5,6,8,10,9,6,3,2])).all() else None)
    is_late = 1 if delivery_time > 40 else 0
    rows.append([f'ORD{i+1:04d}', city, cuisine, order_type, order_value,
                  delivery_time, rating, discount_pct, hour, is_late])

df = pd.DataFrame(rows, columns=[
    'Order_ID','City','Cuisine','Order_Type','Order_Value',
    'Delivery_Time_Min','Rating','Discount_%','Hour','Late_Delivery'])

print(f"✅ Dataset: {len(df)} orders across {df['City'].nunique()} cities, "
      f"{df['Cuisine'].nunique()} cuisines\n")

# ── 2. Key Metrics ───────────────────────────────────────────
total_orders   = len(df)
total_revenue  = df['Order_Value'].sum()
avg_delivery   = df['Delivery_Time_Min'].mean()
avg_rating     = df['Rating'].mean()
late_pct       = df['Late_Delivery'].mean() * 100

print("── Global Summary ──────────────────────────────────────")
print(f"  🛵 Total Orders        : {total_orders:,}")
print(f"  💰 Total Revenue       : ₹{total_revenue:,.0f}")
print(f"  ⏱️  Avg Delivery Time   : {avg_delivery:.1f} min")
print(f"  ⭐ Avg Rating          : {avg_rating:.2f}")
print(f"  ⚠️  Late Delivery Rate  : {late_pct:.1f}%\n")

# ── 3. Dashboard ─────────────────────────────────────────────
fig = plt.figure(figsize=(20, 16), facecolor='#0F1115')
fig.suptitle('🍔  Food Delivery Analytics Dashboard',
             fontsize=24, fontweight='bold', color='#F0F2F5', y=0.98)

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# -- 1: Orders by Hour (Line chart - peak hours) --------------
ax1 = fig.add_subplot(gs[0, :2])
hourly = df.groupby('Hour').size().reindex(range(24), fill_value=0)
ax1.fill_between(hourly.index, hourly.values, alpha=0.3, color=ORANGE)
ax1.plot(hourly.index, hourly.values, color=ORANGE, linewidth=2.5, marker='o', markersize=4)
ax1.set_title('Orders by Hour of Day (Peak Time Analysis)', color='#F0F2F5', fontweight='bold', pad=10)
ax1.set_xlabel('Hour (24h)', color='#9BA1AC')
ax1.set_ylabel('Number of Orders', color='#9BA1AC')
ax1.set_xticks(range(0, 24, 2))
ax1.grid(True, alpha=0.3)

# -- 2: Revenue by City (Bar) ----------------------------------
ax2 = fig.add_subplot(gs[0, 2])
city_rev = df.groupby('City')['Order_Value'].sum().sort_values(ascending=False)
colors_c = [GREEN if v == city_rev.max() else COLORS[i] for i, v in enumerate(city_rev.values)]
ax2.barh(city_rev.index, city_rev.values, color=colors_c, height=0.6, edgecolor='#0F1115')
ax2.set_title('Total Revenue by City', color='#F0F2F5', fontweight='bold', pad=10)
ax2.set_xlabel('Revenue (₹)', color='#9BA1AC')

# -- 3: Cuisine Popularity (Pie) --------------------------------
ax3 = fig.add_subplot(gs[1, 0])
cuisine_counts = df['Cuisine'].value_counts()
wedges, texts, autotexts = ax3.pie(
    cuisine_counts, labels=cuisine_counts.index, autopct='%1.0f%%',
    colors=COLORS, startangle=90, pctdistance=0.75,
    wedgeprops=dict(edgecolor='#0F1115', linewidth=2))
for t in autotexts: t.set_fontsize(8); t.set_color('#0F1115')
for t in texts: t.set_fontsize(8); t.set_color('#F0F2F5')
ax3.set_title('Most Ordered Cuisines', color='#F0F2F5', fontweight='bold', pad=10)

# -- 4: Delivery Time Distribution (Histogram) -------------------
ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(df['Delivery_Time_Min'], bins=18, color='#3A86FF', edgecolor='#0F1115', alpha=0.85)
ax4.axvline(40, color='#EE4266', linestyle='--', linewidth=2, label='Late threshold (40 min)')
ax4.axvline(avg_delivery, color=GREEN, linestyle='--', linewidth=2, label=f'Avg: {avg_delivery:.0f} min')
ax4.set_title('Delivery Time Distribution', color='#F0F2F5', fontweight='bold', pad=10)
ax4.set_xlabel('Delivery Time (minutes)', color='#9BA1AC')
ax4.set_ylabel('Number of Orders', color='#9BA1AC')
ax4.legend(fontsize=8, facecolor='#1A1D24', labelcolor='#F0F2F5', edgecolor='#2C3038')

# -- 5: Rating vs Delivery Time (Scatter) -------------------------
ax5 = fig.add_subplot(gs[1, 2])
sc = ax5.scatter(df['Delivery_Time_Min'], df['Rating'], c=df['Order_Value'],
                 cmap='YlOrRd', alpha=0.7, s=35, edgecolors='none')
ax5.set_title('Rating vs Delivery Time (color = Order Value)', color='#F0F2F5', fontweight='bold', pad=10)
ax5.set_xlabel('Delivery Time (min)', color='#9BA1AC')
ax5.set_ylabel('Rating', color='#9BA1AC')
cbar = plt.colorbar(sc, ax=ax5, shrink=0.8)
cbar.ax.tick_params(colors='#9BA1AC', labelsize=7)

# -- 6: Veg vs Non-Veg orders by City (Stacked Bar) -----------------
ax6 = fig.add_subplot(gs[2, 0])
veg_city = df.groupby(['City','Order_Type']).size().unstack(fill_value=0)
veg_city = veg_city.reindex(columns=['Veg','Non-Veg'])
veg_city.plot(kind='bar', stacked=True, ax=ax6, color=[GREEN, ORANGE],
              edgecolor='#0F1115', width=0.6)
ax6.set_title('Veg vs Non-Veg Orders by City', color='#F0F2F5', fontweight='bold', pad=10)
ax6.set_xlabel('')
ax6.set_ylabel('Orders', color='#9BA1AC')
ax6.tick_params(axis='x', rotation=30)
ax6.legend(fontsize=8, facecolor='#1A1D24', labelcolor='#F0F2F5', edgecolor='#2C3038')

# -- 7: KPI Cards ----------------------------------------------------
ax7 = fig.add_subplot(gs[2, 1])
ax7.axis('off')
top_city = city_rev.idxmax()
kpis = [
    ('Total Orders',     f'{total_orders:,}',          '#3A86FF'),
    ('Total Revenue',    f'₹{total_revenue:,.0f}',     GREEN),
    ('Avg Rating',       f'{avg_rating:.2f} / 5',       '#FFD23F'),
    ('Late Delivery',    f'{late_pct:.1f}%',            '#EE4266'),
]
for i, (label, value, color) in enumerate(kpis):
    y = 0.85 - i * 0.22
    ax7.add_patch(mpatches.FancyBboxPatch(
        (0.05, y - 0.08), 0.9, 0.18, boxstyle='round,pad=0.02,rounding_size=0.02',
        facecolor=color + '22', edgecolor=color, linewidth=1.5,
        transform=ax7.transAxes))
    ax7.text(0.5, y + 0.02, value, transform=ax7.transAxes,
             ha='center', fontsize=12, fontweight='bold', color=color)
    ax7.text(0.5, y - 0.04, label, transform=ax7.transAxes,
             ha='center', fontsize=9, color='#9BA1AC')
ax7.set_title('Key KPIs', color='#F0F2F5', fontweight='bold', pad=10)

# -- 8: Avg Delivery Time Heatmap (City x Cuisine) -------------------
ax8 = fig.add_subplot(gs[2, 2])
pivot = df.pivot_table(values='Delivery_Time_Min', index='City', columns='Cuisine', aggfunc='mean')
sns.heatmap(pivot, ax=ax8, cmap='RdYlGn_r', linewidths=0.5, linecolor='#0F1115',
            annot=True, fmt='.0f', cbar_kws={'shrink': 0.8}, annot_kws={'fontsize': 7})
ax8.set_title('Avg Delivery Time: City x Cuisine', color='#F0F2F5', fontweight='bold', pad=10)
ax8.tick_params(colors='#9BA1AC', labelsize=7)
ax8.set_xlabel('')
ax8.set_ylabel('')

output_path = '/mnt/user-data/outputs/food_delivery_dashboard.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0F1115')
print(f"✅ Dashboard saved → {output_path}")

# ── 4. Insights ──────────────────────────────────────────────
peak_hour = hourly.idxmax()
best_cuisine = cuisine_counts.idxmax()
print("\n── 💡 Key Insights ─────────────────────────────────────")
print(f"  ⏰ Peak Order Hour      : {peak_hour}:00")
print(f"  🍽️  Most Popular Cuisine : {best_cuisine}")
print(f"  🏙️  Top Revenue City     : {top_city}")
print(f"  ⚠️  Late Delivery Rate   : {late_pct:.1f}%")
print("────────────────────────────────────────────────────────\n")

# ── 5. Export CSV ─────────────────────────────────────────────
summary = df.groupby('City').agg(
    Total_Orders=('Order_ID','count'),
    Total_Revenue=('Order_Value','sum'),
    Avg_Delivery_Time=('Delivery_Time_Min','mean'),
    Avg_Rating=('Rating','mean'),
    Late_Delivery_Rate=('Late_Delivery','mean')
).round(2)
summary['Late_Delivery_Rate'] = (summary['Late_Delivery_Rate'] * 100).round(1)
csv_path = '/mnt/user-data/outputs/food_delivery_summary.csv'
summary.to_csv(csv_path)
print(f"✅ Summary CSV → {csv_path}")
print(summary.to_string())
