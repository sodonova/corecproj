#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import cufflinks as cf
import streamlit as st

# cf.set_config_file(theme='ggplot',sharing='public',offline=False)
cf.go_offline()
# pd.options.plotting.backend = 'plotly'

df = pd.read_csv("usage_data_week_11_1.csv", index_col=0)
# df.head()


# In[122]:

"""
# East Fitness usage at the Corec

Here at Purdue, our gym is the Cordova Recreation Center, also called the Corec. It's an excellent facility, but it's busy. After aggregating usage data over one week, here are some insights about the usage of East Fitness, the part of the facility that has squat racks and bench press stations.
"""


# get_ipython().run_cell_magic('capture', '', '# Initialize pandas datetime object from UTC epoch seconds recorded\n
df.loc[:, 'date_time'] = pd.to_datetime(df.loc[:,'date_time'],unit="s",utc=True)
df.loc[:, 'date_time'] = df.date_time.dt.tz_convert('EST')
# corec isn\'t open at 4, same data as the previous day
df.loc[df.date_time.dt.hour == 4, 'current_capacity'] = 0 # encoded wrong
df = df.reset_index(drop=True)

# df.loc[(df.name == \'Upper Gym\'),:]')


"""
## Our data
In general, our data look like this, with a current, total, and percent capacity, along with a time. You'll notice that my script scrapes the facility usage data every hour at 5 minutes past the hour.
"""
# In[123]:


eastdf = df.loc[df["name"] == 'East Fitness (Strength Equipment)'].copy()
eastdf.loc[:,'hour'] = eastdf.date_time.dt.hour
eastdf.loc[:,'day'] = eastdf.date_time.dt.day
eastdf.loc[:,'weekday'] = eastdf.date_time.dt.weekday
eastdf.loc[:,'weekday_name'] = eastdf.date_time.dt.day_name()


eastdf.head()


"""
One thing that you might not notice right away is that total capacity and percent capacity are not very useful in human terms. East Fitness certainly cannot hold 300 people exercising together, and it's pretty misleading to suggest that 40 people is only 14% capacity. For reference, East has around:
- 11 half squat racks
- 5 full squat racks
- 10 flat bench stations
- 2 deadlift pads
- 5 miscellaneous leg machines

That's 33 machines.
"""
# ## Figures and Trends
# So, when should you work out now that the corec is busy? Starting with the day of the week, we can see the broad pattern in the medians of occupancy per day. Saturday and Sunday are far and away the best days to work out.

# In[124]:


weekday = eastdf.groupby('weekday').median().reset_index()
fig = weekday.iplot(x='weekday', y='current_capacity', title= 'East Fitness median occupancy over days of the week', asFigure=True)
fig.update_xaxes(tickvals=[0,1,2,3,4,5,6],
                 ticktext=["Mon","Tue","Wed","Thr","Fri","Sat","Sun"])
st.plotly_chart(fig)


"""Moving to a more detailed view, we can see that Friday is a better option than it looks initially. Thanks to its smaller range and IQR, you're more likely to consistently get a workout with 37 people rather than be surprised by 85 people like on monday. (Hover over the figure to see points.)
"""
# In[125]:


weekdaydf = eastdf.loc[:,['current_capacity','weekday']].copy()
# plot = weekday.boxplot('current_capacity',by='weekday')
# plot = plot.set_xticklabels(["Mon","Tue","Wed","Thr","Fri","Sat","Sun"])
# weekdaydf.iplot('box',)
weekdaydf.weekday = weekdaydf.weekday.astype("category")
weekdaydf = weekdaydf.pivot(columns = 'weekday')

weekdaydf.columns = weekdaydf.columns.droplevel()
fig = weekdaydf.iplot('box', colors=['tomato'], title= 'East Fitness occupancy over days of the week', asFigure=True) # , xaxes={0:'Mon',1:"Tue",2:"Wed",3:"Thr",4:"Fri",5:"Sat",6:"Sun"}
fig.update_layout(showlegend=False)
fig.update_xaxes(tickvals=[0,1,2,3,4,5,6],
                 ticktext=["Mon","Tue","Wed","Thr","Fri","Sat","Sun"])
st.plotly_chart(fig)


"""We can also take a look at the time of day. This view of the data suggests that working out after 4pm (16:00) isn't the best idea.
"""
# In[126]:


# hour = eastdf.groupby('hour')
# hour.plot(x='hour', y='current_capacity')
# eastdf.boxplot('current_capacity',by='hour')

hourdf = eastdf.loc[:,['current_capacity','hour']].copy()

hourdf.hour = hourdf.hour.astype("category")
hourdf = hourdf.pivot(columns = 'hour')

hourdf.columns = hourdf.columns.droplevel()
fig = hourdf.iplot('box', colors=['tomato'], title='East Fitness occupancy on 24hr time', asFigure=True)
fig.update_layout(showlegend=False)
st.plotly_chart(fig)


"""Finally, we refine that last view by looking only at the medians. The distribution has a clear peak at 5pm (17). There also seems to be a pattern here of lower activity from 5am to 2pm (14), maybe because students are either sleeping or in class.
"""
# In[127]:


hourdf = eastdf.loc[eastdf.hour!=4,['current_capacity','hour']].copy()

meandf = hourdf.groupby('hour').median()
st.plotly_chart(meandf.iplot(kind='line', title='East Fitness median occupancy on 24hr time', asFigure=True))
