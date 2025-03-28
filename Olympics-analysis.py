#!/usr/bin/env python
# coding: utf-8

# In[220]:


import pandas as pd
import numpy as np


# In[221]:


df = pd.read_csv('athlete_events.csv')
region_df =pd.read_csv('noc_regions.csv')


# In[4]:


df.tail()


# In[5]:


df.shape


# In[6]:


df = df[df['Season'] == 'Summer']


# In[7]:


df.shape


# In[8]:


df.tail()


# In[9]:


region_df


# In[224]:


df = df.merge(region_df,on='NOC',how='left')


# In[11]:


df.tail()


# In[12]:


df['region'].unique().shape


# In[13]:


df.isnull().sum()


# In[235]:


df.duplicated().sum()


# In[234]:


df.drop_duplicates(inplace=True)


# In[236]:


df['Medal'].value_counts()


# In[237]:


pd.get_dummies(df['Medal']).astype(int)#OHE 


# In[18]:


df.shape


# In[238]:


df = pd.concat([df,pd.get_dummies(df['Medal']).astype(int)],axis=1)#Horizontal concat


# In[260]:


print(df.columns)


# In[21]:


df.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()


# In[22]:


df[(df['NOC']=='IND') & (df['Medal']=='Gold')] #Team wise medal count 


# In[23]:


#we need to correct the count of medal i.e,1medal/country ->team wins
medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])


# In[24]:


medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()


# In[29]:


medal_tally.head()


# In[58]:


medal_tally[medal_tally['NOC'] == 'IND']


# In[26]:


medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']


# In[27]:


medal_tally


# In[38]:


years = df['Year'].unique().tolist()# for extracting year and showing year wise medal count


# In[39]:


years.sort()


# In[40]:


years.insert(0,'Overall')


# In[41]:


years


# In[47]:


country = np.unique(df['region'].dropna().values).tolist()


# In[48]:


country.sort()


# In[49]:


country.insert(0,'Overall')


# In[50]:


country


# In[78]:


def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall'  and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country !='Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country =='Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country !='Overall':
        temp_df = medal_df[(medal_df['Year' ] == int(year)) & (medal_df['region']== country)]
     
    
    if  flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    
    print(x)


# In[80]:


fetch_medal_tally(year='1900',country='India')


# In[52]:


medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])


# In[60]:


medal_df[(medal_df['Year' ] == 2016) & (medal_df['region']=='India')]


# In[ ]:





# In[ ]:





# # Overall Aanlysis
# - No. of editions
# - No. of cities
# - No. of events/sports
# - No. of athletes
# - particilating nations

# In[81]:


df


# In[ ]:


#find top statistics


# In[83]:


df['Year'].unique().shape#1906 olympics are not considered by IOC


# In[84]:


df['Year'].unique().shape[0] - 1


# In[85]:


df['City'].unique().shape[0]


# In[86]:


df['City'].unique()


# In[87]:


df['Sport'].unique()


# In[88]:


df['Event'].unique().shape


# In[90]:


df['Name'].unique().shape


# In[91]:


df['region'].unique().shape


# In[92]:


#Participating Nations over time
df.head()


# In[105]:


nations_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')


# In[106]:


nations_over_time


# In[107]:


nations_over_time = nations_over_time.rename(columns={'Year':'Edition','count':'No of countries'})


# In[108]:


import plotly.express as px
fig = px.line(nations_over_time,x='Edition',y='No of countries')
fig.show()


# In[109]:


#Event over time
Events_over_time = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')


# In[110]:


Events_over_time


# In[141]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[142]:


x = df.drop_duplicates(['Year','Event','Sport'])


# In[143]:


x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc = 'count').fillna(0).astype('int')


# In[151]:


plt.figure(figsize=(20,20))
sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)


plt.xticks(rotation=45, ha="right")



# In[ ]:





# In[192]:


#most sucessful athletes 
def most_successsful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    
    if sport !='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    return temp_df['Name'].value_counts().reset_index().rename(columns={'Name':'Athlete_name','count':'Medal_count'}).head(15).merge(df,left_on='Athlete_name',right_on='Name',how='left')[['Athlete_name','Medal_count','Sport','region']].drop_duplicates('Athlete_name')


# In[173]:


#to find most sucessful player need to count medals and remove nan values
temp_df = df.dropna(subset='Medal')


# In[193]:


most_successsful(df,'Gymnastics')


# In[ ]:





# In[ ]:


# Country wise Aanlysis
- Countrywise medal tally per year(line plot)
-what country are good at heatmap
- Most successful Athletes(Top 10)


# In[194]:


temp_df=df.dropna(subset=['Medal'])
temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)


# In[200]:


new_df = temp_df[temp_df['region'] == 'USA']
final_df=new_df.groupby('Year').count()['Medal'].reset_index()


# In[201]:


fig = px.line(final_df, x='Year',y = 'Medal')
fig.show()


# In[ ]:


#heatmap


# In[ ]:


temp_df=df.dropna(subset=['Medal'])
temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)


# In[207]:


new_df = temp_df[temp_df['region'] == 'UK']
plt.figure(figsize=(20,20))
sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)

plt.xticks(rotation=45, ha="right")


# In[ ]:


#top 10 athletes country wise


# In[211]:


def most_successsful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    
    temp_df = temp_df[temp_df['region']== country ]
    x = temp_df['Name'].value_counts().reset_index().rename(columns={'Name':'Athlete_name','count':'Medal_count'}).head(15).merge(df,left_on='Athlete_name',right_on='Name',how='left')[['Athlete_name','Medal_count','Sport','region']].drop_duplicates('Athlete_name')
    return x


# In[214]:


most_successsful_countrywise(df,'USA')


# In[ ]:





# In[ ]:





# # Athletes-wise analysis
# 

# In[250]:


#distribution graph acc to age of athlete
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt


# In[228]:


athlete_df = df.drop_duplicates(subset = ['Name','region'])


# In[258]:


x1 = athlete_df['Age'].dropna().tolist()
x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna().tolist()
x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna().tolist()
x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna().tolist()
data=[x1,x2,x3,x4]
label=['Overall Age','Gold Medalist','Silver Medalist','Bronz Medalist']


# In[261]:


sns.kdeplot(x1, label='Overall')
sns.kdeplot(x2, label='Gold Medalist')
sns.kdeplot(x3, label='Silver Medalist')
sns.kdeplot(x4, label='Bronze Medalist')

plt.legend() # Add a legend
plt.xlabel('Age distribution')
plt.show()    # Show the plot


# In[ ]:





# In[ ]:


#


# In[303]:


x=[]
name=[]
for sport in famous_sports:
    temp_df=athlete_df[athlete_df['Sport']== sport]
    x.append (temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
    name.append(sport)


# In[ ]:


fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)


# In[ ]:


fig.show()


# In[266]:


df['Sport'].unique()


# In[301]:


famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War','Athletics', 'Ice Hockey', 'Swimming','Badminton', 'Sailing',
                'Gymnastics',
       'Art Competitions','Handball', 'Weightlifting','Wrestling','Water Polo', 'Hockey','Archery', 'Volleyball','Table Tennis','Golf']


# In[ ]:





# In[ ]:


#weight vs height graph for specific sport filtered on Medal,sex


# In[267]:


athlete_df['Medal'].fillna('No Medal',inplace = True)


# In[278]:


plt.figure(figsize=(10,10))
temp_df = athlete_df[athlete_df['Sport']=='Athletics']
sns.scatterplot(x='Weight', y='Height', data=temp_df,hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
plt.title('Weight vs Height of Athletics Players')
plt.xlabel('Weight (kg)')
plt.ylabel('Height (cm)')

plt.show()


# In[ ]:


import plotly.express as px


# In[282]:


men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()


# In[295]:


final = men.merge(women,on='Year')
final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)


# In[300]:


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))

# Plot lines for Male and Female
plt.plot(final["Year"], final["Male"], label="Male", linestyle="-")
plt.plot(final["Year"], final["Female"], label="Female", linestyle="-")

# Labels and Title
plt.xlabel("Year")
plt.ylabel("Number of Athletes")
plt.title("Male vs Female Athletes Over the Years")

# Grid, Legend, and Show
plt.legend()

