# Data_Dashboard_2

✨ Compiled a new Data Analysis and Visualization project using Python libraries like Pandas and Plotly . 

📑 Data Retrieval and Cleaning :
In this project case two different databases were used named ' Microsoft Stock Prices ' and ' Google Stock Prices ' and were collected from Kaggle . Used pd.merge() function to merge both the datasets and pd.datetime for the date column . Dataset merge type was outer that means every input was merged rather than merging the common values under a specific column which happens in inner merge . As both the datasets were not of the same size so I needed to get the value of the common datetime domain and initialized the same time in both datasets . 

📊 Data Visualization :
Used Plotly as the ploting software . As Plotly is more easy to imply than Matplotlib and Seaborn I had less bugs and it also consumed less time. 

📈 Visualization Platform :
Used Streamlit again for the web app platform . Used st.sidebars to get a sidebar where the multiselect and selectbox filters were used for Time series and Volum graph . 

🐱 Github Deployment :
Streamlit web apps can be deployed using hosting services . As I intended that others should experience the dashboard themselves I deployed it using GitHub repo with the hosting of streamlit community cloud . 
