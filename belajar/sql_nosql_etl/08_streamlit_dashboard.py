"""
Streamlit Dashboard - membaca dari REPORTING DB (cepat).
Bukan dari MASTER DB (yang lambat karena perlu JOIN banyak tabel).
"""

import sqlite3
import os
import pandas as pd
import streamlit as st

BASE = os.path.dirname(os.path.abspath(__file__))
REPORTING_DB = os.path.join(BASE, 'data/reporting.db')


@st.cache_data(ttl=60)
def load_data(query):
    conn = sqlite3.connect(REPORTING_DB)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.set_page_config(page_title='Borma Sales Dashboard', layout='wide')
st.title('📊 Borma Retail Dashboard')
st.markdown('Data dari **Reporting DB** (pre-aggregated, fast)')

tab1, tab2, tab3, tab4 = st.tabs([
    'Penjualan per Cabang', 'Penjualan per Kategori',
    'Metode Pembayaran', 'Top Produk',
])

with tab1:
    st.subheader('Penjualan Harian per Cabang')

    dates = load_data('SELECT DISTINCT date FROM daily_sales_by_branch ORDER BY date')
    if not dates.empty:
        selected_date = st.selectbox('Pilih Tanggal', dates['date'].tolist(), key='date_branch')
        df_branch = load_data(f'''
            SELECT branch_name, total_sales, transaction_count
            FROM daily_sales_by_branch
            WHERE date = '{selected_date}'
            ORDER BY total_sales DESC
        ''')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_branch, use_container_width=True, hide_index=True)
        with col2:
            st.bar_chart(df_branch.set_index('branch_name')['total_sales'])
    else:
        st.warning('Jalankan dulu: python 06_etl_pipeline.py')

with tab2:
    st.subheader('Penjualan per Kategori')

    df_cat = load_data('''
        SELECT category_name, SUM(total_sales) as total,
               SUM(qty_sold) as total_qty
        FROM daily_sales_by_category
        GROUP BY category_name
        ORDER BY total DESC
    ''')
    if not df_cat.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_cat, use_container_width=True, hide_index=True)
        with col2:
            st.bar_chart(df_cat.set_index('category_name')['total'])
    else:
        st.warning('Jalankan dulu: python 06_etl_pipeline.py')

with tab3:
    st.subheader('Metode Pembayaran')

    df_pay = load_data('''
        SELECT payment_method, SUM(total_amount) as total,
               SUM(transaction_count) as jumlah_transaksi
        FROM payment_method_summary
        GROUP BY payment_method
        ORDER BY total DESC
    ''')
    if not df_pay.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_pay, use_container_width=True, hide_index=True)
        with col2:
            st.bar_chart(df_pay.set_index('payment_method')['total'])
    else:
        st.warning('Jalankan dulu: python 06_etl_pipeline.py')

with tab4:
    st.subheader('Top 10 Produk (Bulan Ini)')

    df_top = load_data('''
        SELECT month, product_name, category_name,
               qty_sold, total_revenue, rank
        FROM top_products
        WHERE rank <= 10
        ORDER BY month DESC, rank ASC
    ''')
    if not df_top.empty:
        st.dataframe(df_top, use_container_width=True, hide_index=True)
    else:
        st.warning('Jalankan dulu: python 06_etl_pipeline.py')

st.divider()
st.caption(f'Data source: {REPORTING_DB} | Auto-refresh tiap 60 detik')
