import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def load_data():
    df = pd.read_csv('combined_data.csv')
    return df

# фільтр
def filter_data(df, indicator, region, week_range, year_range):
    filtered_df = df[
        (df['area'] == int(region)) &
        (df['Week'].between(week_range[0], week_range[1])) &
        (df['Year'].between(year_range[0], year_range[1]))
    ]
    if indicator == "Всі показники":
        return filtered_df[['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']]
    else:
        return filtered_df[['Year', 'Week', indicator]]


def main():
    st.title("Візуалізація даних NOAA")

    # Завантажую дані
    df = load_data()

    # Скидання фільтрів
    if st.button("Скинути фільтри"):
        st.session_state.clear()
        st.session_state["indicator"] = "Всі показники"
        st.session_state["region"] = "Вінницька"
        st.session_state["week_range"] = (1, 52)
        st.session_state["year_range"] = (1981, 2023)
        st.rerun()
    
    col1, col2 = st.columns([1, 3])

    # елементи в першій колонці
    with col1:
        # випадалка для показників
        indicator = st.selectbox(
            "Оберіть показник",
            options=["Всі показники", "VCI", "TCI", "VHI"],
            index=0,
            key="indicator"
        )

        # випадалка для регіонів
        regions = {
            "Вінницька": "1", "Волинська": "2", "Дніпропетровська": "3",
            "Донецька": "4", "Житомирська": "5", "Закарпатська": "6",
            "Запорізька": "7", "Івано-Франківська": "8", "Київська": "9",
            "Кіровоградська": "10", "Луганська": "11", "Львівська": "12",
            "Миколаївська": "13", "Одеська": "14", "Полтавська": "15",
            "Рівенська": "16", "Сумська": "17", "Тернопільська": "18",
            "Харківська": "19", "Херсонська": "20", "Хмельницька": "21",
            "Черкаська": "22", "Чернівецька": "23", "Чернігівська": "24",
            "Крим": "25", "Київ": "26", "Севастополь": "27"
        }
        region = st.selectbox(
            "Оберіть регіон",
            options=list(regions.keys()),
            index=0,
            key="region"
        )

        # слайдер для тижнів
        week_range = st.slider(
            "Оберіть діапазон тижнів",
            min_value=1,
            max_value=52,
            value=(1, 52),
            key="week_range"
        )

        # слайдер для років
        year_range = st.slider(
            "Оберіть діапазон років",
            min_value=1981,
            max_value=2023,
            value=(1981, 2023),
            key="year_range"
        )

        # сортую
        sort_asc = st.checkbox("Сортувати за зростанням", value=False)
        sort_desc = st.checkbox("Сортувати за спаданням", value=False)

    # фільтр
    filtered_df = filter_data(df, indicator, regions[region], week_range, year_range)

    # сортую
    if sort_asc and sort_desc:
        st.warning("Обрано обидва типи сортування. Дані відображені без сортування.")
    elif sort_asc:
        filtered_df = filtered_df.sort_values(by=indicator if indicator != "Всі показники" else "Year", ascending=True)
    elif sort_desc:
        filtered_df = filtered_df.sort_values(by=indicator if indicator != "Всі показники" else "Year", ascending=False)

    # 
    with col2:
        tabs = st.tabs(["Таблиця", "Графік", "Порівняння"])

        # таблиця
        with tabs[0]:
            st.subheader("Відфільтровані дані")
            st.dataframe(filtered_df)

        # графік
        with tabs[1]:
            if indicator != "Всі показники":
                st.subheader(f"Часовий ряд {indicator} для {region}")
                fig, ax = plt.subplots(figsize=(10, 6))
                filtered_df.plot(x='Week', y=indicator, ax=ax, color='blue', legend=False)
                ax.set_xlabel("Тижні")
                ax.set_ylabel(indicator)
                ax.set_title(f"{indicator} за {year_range[0]}-{year_range[1]}")
                st.pyplot(fig)
            else:
                st.warning("Оберіть конкретний показник для візуалізації.")

        # порівнюємо
        with tabs[2]:
            if indicator != "Всі показники":
                st.subheader(f"Порівняння {indicator} по областях")
                comparison_df = df[
                    (df['Week'].between(week_range[0], week_range[1])) &
                    (df['Year'].between(year_range[0], year_range[1]))
                ]
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.boxplot(x='area', y=indicator, data=comparison_df, ax=ax)
                ax.set_xlabel("Області (номери)")
                ax.set_ylabel(indicator)
                ax.set_title(f"Порівняння {indicator} по всіх областях")
                plt.axvline(x=int(regions[region])-1, color='red', linestyle='--', label=region)
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning("Оберіть конкретний показник для порівняння.")

if __name__ == "__main__":
    main()
