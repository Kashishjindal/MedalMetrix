import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('data:image/jpeg;base64,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')
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis' )
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in" + str(selected_year) + "Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) + "Overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) + "performance in " + str(selected_year) + "Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(editions)

    with col2:
        st.subheader("Hosts")
        st.title(cities)

    with col3:
        st.subheader("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Nations")
        st.title(nations)
    with col3:
        st.subheader("Athletes")
        st.title(athletes)


    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)

    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + "excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot =True)
    st.pyplot(fig)

    st.title('Top 10 athletes of ' + selected_country)
    top10_df =helper.most_successsful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete-wise Analysis':
    st.title('Distribution of Age')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna().tolist()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().tolist()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().tolist()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().tolist()

    data = [x1, x2, x3, x4]
    labels = ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist']

    fig = ff.create_distplot(data, labels, show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Ice Hockey', 'Swimming', 'Badminton',
                     'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Archery',
                     'Volleyball', 'Table Tennis', 'Golf']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age wrt Sports(Gold Medalist')
    st.plotly_chart(fig)



    st.title("Weight vs Height ")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)

    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots(figsize=(10, 10))

    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df, hue='Medal', style='Sex', s=100, ax=ax)
    ax.set_title('Weight vs Height ')
    ax.set_xlabel('Weight (kg)')
    ax.set_ylabel('Height (cm)')
    st.pyplot(fig)

    st.title('Men VS Women participation Over the years')
    final =  helper.men_vs_wome(df)
    fig = px.line(final,x="Year",y=['Male','Female'])
    st.plotly_chart(fig)

