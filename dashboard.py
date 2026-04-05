# mengimport library yang akan digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')

# membuat fungsi untuk membuat daily_total_rents_df
def create_daily_total_rents_df(df):
    daily_rents_df = df[['dteday', 'cnt']].copy()
    daily_rents_df.rename(columns={
        'dteday': 'rent_date',
        'cnt': 'total_rent'
    }, inplace=True)

    return daily_rents_df

# membuat fungsi untuk membuat daily_casual_rents_df 
def create_daily_casual_rents_df(df):
    daily_casual_df = df[['dteday', 'casual']].copy()
    daily_casual_df.rename(columns={
        'dteday': 'rent_date',
        'casual' : 'casual_count'
    }, inplace=True)

    return daily_casual_df

# membuat fungsi untuk membuat daily_registered_rents_df
def create_daily_registered_rents_df(df):
    daily_registered_df = df[['dteday', 'registered']].copy()
    daily_registered_df.rename(columns={
        'dteday': 'rent_date',
        'registered' : 'registered_count'
    }, inplace=True)

    return daily_registered_df

# membuat fungsi untuk membuat rent_byseason_df
def create_rent_byseason_df(df):
    rent_byseason_df = df.groupby(by='season').cnt.sum().sort_values(ascending=False).reset_index()
    map_season = {
        1: 'spring',
        2: 'summer',
        3: 'fall',
        4: 'winter'
    }
    rent_byseason_df['season'] = rent_byseason_df['season'].map(map_season)
    return rent_byseason_df

# membuat fungsi untuk membuat rent_byweather_df
def create_rent_byweather_df(df):
    rent_byweather_df = df.groupby(by='weathersit').cnt.sum().sort_values(ascending=False).reset_index()
    map_weather = {
        1: 'clear',
        2: 'mist/cloudy',
        3: 'light rain',
        4: 'heavy rain'
    }
    rent_byweather_df['weathersit'] = rent_byweather_df['weathersit'].map(map_weather)
    return rent_byweather_df

# membuat fungsi untuk membuat rent_bymonth_df
def create_rent_bymonth_df(df):
    rent_bymonth_df = df.groupby(by='mnth').cnt.sum().reset_index()
    map_month = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Des'
    }
    rent_bymonth_df['mnth'] = rent_bymonth_df['mnth'].map(map_month)
    return rent_bymonth_df

# membuat fungsi untuk membuat rent_byworkingday_df
def create_rent_byworkingday_df(df):
    rent_byholiday_df = df.groupby(by='workingday').agg({
        'casual': 'sum',
        'registered':  'sum'
    }).reset_index()
    map_workingday = {
        0 : 'weekend/holiday',
        1 : 'workingday'
    }
    rent_byholiday_df['workingday'] = rent_byholiday_df['workingday'].map(map_workingday)
    return rent_byholiday_df


# membuat fungsi untuk membuat rent_bytemp_df
def create_rent_bytemp_df(df):
    rent_bytemp_df = df.groupby(by='cat_temp').cnt.sum().reset_index()
    rent_bytemp_df['cat_temp'] = pd.Categorical(rent_bytemp_df['cat_temp'], categories=['very low', 'low', 'medium', 'high', 'very high'], ordered=True)
    return rent_bytemp_df

# membuat fungsi untuk membuat rent_byhum_df
def create_rent_byhum_df(df):
    rent_byhum_df = df.groupby(by='cat_hum').cnt.sum().reset_index()
    rent_byhum_df['cat_hum'] = pd.Categorical(rent_byhum_df['cat_hum'], categories=[ 'low', 'medium', 'high'], ordered=True)
    return rent_byhum_df

# membuat fungsi untuk membuat rent_bywind_df
def create_rent_bywind_df(df):
    rent_bywind_df = df.groupby(by='cat_wind').cnt.sum().reset_index()
    rent_bywind_df['cat_wind'] = pd.Categorical(rent_bywind_df['cat_wind'], categories=['low', 'medium', 'high'], ordered=True)
    return rent_bywind_df

# memuat berkas day_df.csv sebagai dataframe
all_df = pd.read_csv('day_df.csv')

# memastikan kolom dteday bertipe datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# membuat filter dengan widget date input pada bagian sidebar
max_date = all_df['dteday'].max()
min_date = all_df['dteday'].min()

with st.sidebar:

    # mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

# menyimpan dataframe yang telah difilter
main_df = all_df[(all_df['dteday'] >= str(start_date)) & (all_df['dteday'] <= str(end_date))]

# membuat dataframe untuk membuat visualisasi data
daily_total_rent_df = create_daily_total_rents_df(main_df)
daily_casual_rent_df = create_daily_casual_rents_df(main_df)
daily_registered_rent_df = create_daily_registered_rents_df(main_df)
byseason_df = create_rent_byseason_df(main_df)
byweather_df = create_rent_byweather_df(main_df)
bymonth_df = create_rent_bymonth_df(main_df)
byworkingday_df = create_rent_byworkingday_df(main_df)
bytemp_df = create_rent_bytemp_df(main_df)
byhum_df = create_rent_byhum_df(main_df)
bywind_df = create_rent_bywind_df(main_df)

# menambahkan header pada dashboard
st.header('Bike Sharing Dashboard :sparkles:')

# menampilkan informasi total rent, avg daily rent, casual, registered dalam bentuk metric 
st.subheader('Daily Rents')

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rent = daily_total_rent_df.total_rent.sum()
    st.metric('Total rents', value=total_rent)

with col2:
    avg_rent = round(daily_total_rent_df.total_rent.mean(), 2)
    st.metric('Avg daily rents', value=avg_rent)

with col3:
    total_registered = daily_registered_rent_df.registered_count.sum()
    st.metric('Total registered', value=total_registered)

with col4:
    total_casual = daily_casual_rent_df.casual_count.sum()
    st.metric('Total casual', value=total_casual)

# menampilkan informasi jumlah sewa sepeda setiap hari
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_total_rent_df['rent_date'],
    daily_total_rent_df['total_rent'],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# menampilkan informasi jumlah sewa sepeda berdasarkan hari kerja dan perbandingan user casual dan registered
st.subheader('User Analysis')
col1, col2 = st.columns([3, 2])

with col1:
    x = np.arange(len(byworkingday_df['workingday']))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 6))

    bars1 = ax.bar(x - width/2, byworkingday_df['casual'], width, 
               label='Casual', color='#D3D3D3')
    bars2 = ax.bar(x + width/2, byworkingday_df['registered'], width, 
               label='Registered', color='#90CAF9')

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=14)

    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=14)

    ax.set_title('Number Rent by Workingday', loc='center', fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(byworkingday_df['workingday'])
    ax.legend()
    ax.tick_params(axis='x', labelsize=17)
    ax.tick_params(axis='y', labelsize=12)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        [total_casual, total_registered],
        labels = ['Casual', 'Registered'],
        autopct ='%1.1f%%',
        colors = ['#D3D3D3', '#90CAF9'],
        startangle = 90,
        textprops = {'fontsize': 15}
    )
    ax.set_title('Casual vs Registered', loc='center', fontsize=20)
    plt.tight_layout()
    st.pyplot(fig)

# menampilkan informasi rata-rata sewa sepeda berdasarkan musim dan bulan
st.subheader('Time Based Pattern')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9", '#D3D3D3', '#D3D3D3', '#D3D3D3']
    sns.barplot(
        y='cnt',
        x='season',
        data=byseason_df.sort_values(by='cnt', ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of Rents by Season', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9"]
    sns.barplot(
        y='cnt',
        x='mnth',
        data=bymonth_df,
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of Rents by Month', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)

# menampilkan informasi berdasarkan suhu, kelembaban, kecepatan angin dan cuaca
st.subheader('Environmental Factors')
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9"]
    sns.barplot(
        y='cnt',
        x='cat_temp',
        data=bytemp_df,
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of rents by temperature', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9"]
    sns.barplot(
        y='cnt',
        x='cat_hum',
        data=byhum_df,
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of rents by humidity', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9"]
    sns.barplot(
        y='cnt',
        x='cat_wind',
        data=bywind_df,
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of rents by windspeed', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    colors = [ "#90CAF9", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y='cnt',
        x='weathersit',
        data=byweather_df.sort_values(by='cnt', ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title('Number of rents by weather', loc='center', fontsize=40)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=25)
    st.pyplot(fig)