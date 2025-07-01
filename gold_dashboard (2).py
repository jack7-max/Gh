
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objs as go
import yfinance as yf

# إعداد الصفحة مع تصميم داكن
st.set_page_config(page_title="GoldSmart Pro", layout="wide", page_icon="💰")

# CSS مخصص لتنسيق جذاب وخلفية سوداء
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: gold;
}
table {
    color: white !important;
}
thead th {
    background-color: #1c1f26 !important;
}
tbody td {
    background-color: #1c1f26 !important;
}
.metric-label {
    color: white !important;
}
div[data-testid="metric-container"] {
    background-color: #1c1f26;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# عنوان الموقع
st.markdown("<h1 style='text-align: center;'>💰 GoldSmart Pro - التحليل الموسمي للذهب</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #aaa;'>تحليل شهري وسعري احترافي باستخدام الذكاء الاصطناعي</h4>", unsafe_allow_html=True)
st.markdown("---")

# تحميل بيانات الذهب
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * 5)
data = yf.download("GC=F", start=start, end=end)
data = data[['Close']].dropna().reset_index()
data.columns = ['Date', 'Price']
data['Month'] = data['Date'].dt.month

# التأثيرات الموسمية
seasonal_effects = {
    1: 1.008576, 2: 0.996684, 3: 1.016732, 4: 1.019485,
    5: 1.016862, 6: 1.006577, 7: 1.026193, 8: 1.011332,
    9: 0.977220, 10: 0.991212, 11: 0.968613, 12: 0.994965
}

months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
          "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

# جدول موسمي
table_data = []
for i in range(1, 13):
    effect = seasonal_effects.get(i, 1)
    signal = '📈 Bullish' if effect > 1 else '📉 Bearish'
    table_data.append({
        "📅 الشهر": months[i-1],
        "📊 التأثير الموسمي": round(effect, 6),
        "🔍 الاتجاه": signal
    })

df_season = pd.DataFrame(table_data)

# عرض السعر الحالي والاتجاه الشهري
col1, col2 = st.columns(2)
col1.metric("🔸 السعر الحالي", f"{data['Price'].iloc[-1]:,.2f} USD")
this_month = datetime.date.today().month
signal = '📈 Bullish' if seasonal_effects[this_month] > 1 else '📉 Bearish'
col2.metric("📆 هذا الشهر", f"{months[this_month - 1]}", delta=signal)

# جدول التحليل الموسمي
st.markdown("### 📅 الاتجاهات الموسمية السنوية")
st.dataframe(df_season.style.set_table_styles([
    {'selector': 'thead', 'props': [('background-color', '#1c1f26')]},
    {'selector': 'tbody', 'props': [('background-color', '#1c1f26')]},
]))

# رسم بياني
st.markdown("### 📉 تطور سعر الذهب خلال السنوات الأخيرة")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['Date'], y=data['Price'],
    line=dict(color='gold', width=2),
    name='Gold Price'
))
fig.update_layout(
    plot_bgcolor='#0e1117',
    paper_bgcolor='#0e1117',
    font=dict(color='white'),
    title='📊 Gold Price Over Time',
    xaxis_title='📆 التاريخ',
    yaxis_title='💲 السعر بالدولار'
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2025 GoldSmart AI | تصميم عصري مدعوم بالذكاء الاصطناعي</div>", unsafe_allow_html=True)
