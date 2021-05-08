### Exec Streamlit
# cd path/to/dir
# streamlit run main.py

### Install Streamlit Library
# sudo apt-get update
# sudo pip3 install --upgrade pip
# sudo pip3 install --upgrade streamlit

### Import Packages
import streamlit as st
import time

# import numpy as np
# import pandas as pd
# from PIL import Image

### Basic Syntax
st.title("Streamlit 超入門")
st.write("Practce Codes!")

### Progress Bar
latest_iteration = st.empty() # make box with empty contents
bar = st.progress(0)          # make progress bar with 0

for i in range(100):
  latest_iteration.text(f"Waiting {i+1}%")
  bar.progress(i+1)           # update progress bar
  time.sleep(0.01)            # sleep duration until the next iteration

"Done"                        # Appear once loop was completed

time.sleep(0.3)               # Wait 0.3 sec until disappear
latest_iteration.text = ""    # <=Do not work
bar = ""                      # <=Do not work

### Prepare & Show Data
# df = pd.DataFrame(
#   {
#     "R1": [1,2,3,4],
#     "R2": [10,20,30,40],
#     "R3": [11,21,31,41]
#   }
# )
# st.write(df)
# st.dataframe(df.style.highlight_max(axis=0), width=300, height=200)
# st.table(df.style.highlight_max(axis=0))

### Show comment
# """
# ```python
# import streamlit as st
# import numpy as np
# import pandas as pd
# ```
# """

### Prepare & Show Random Data
# df = pd.DataFrame(
#   # 20 x 3 の配列の乱数
#   np.random.rand(20, 3),
#   # Positional Argument must follows Keyword Argument
#   columns=["a","b","c"]
# )
# st.write(df)
# st.line_chart(df)
# st.area_chart(df)
# st.bar_chart(df)

### Prepare & Show Mapping Data
# df = pd.DataFrame(
#   np.random.rand(100, 2)/[50,50] + [35.69, 139.70],
#   columns=["lat","lon"]
# )
# st.map(df)

### Prepare & Show Image under Condition
# if st.checkbox("Show Image"):
#   img = Image.open("/home/tkanayama/Works/02_Development/00_Personal/python/streamlit/img/face.jpg")
#   st.image(img, caption="Kohei Imanishi", use_column_width=True)

### Interative Widgets
# hoby = st.text_input("Please write your hoby:")
# "Your favorite hoby is", hoby, "."

# option = st.selectbox(
#   "Please select your favorite numbers:",
#   list(range(1,11))
# )
# "Your favorite numbers is", option, "."

# condition = st.slider("How is your condition?", 0, 100, 50)
# "Your condition:", condition

### Interative Widgets @ SideBar
# option_side = st.sidebar.selectbox(
#   "Please select your favorite numbers:",
#   list(range(1,10))
# )
# "Your favorite numbers is", option_side, "."

# condition_side = st.sidebar.slider("How is your conditiion?", 0, 100, 50)
# "Condition:", condition_side

### Layout: 2 Columns
left_column, right_column = st.beta_columns(2)

button = left_column.button("Display on Right Column")
if button:
  right_column.write("Right Column")

### Layout: Expander (Toggle)
expander = st.beta_expander("Inquiry1")
expander.write("Tokyo Office: 03-3515-2511")
expander.write("Osaka Office: XX-XXXX-XXXX")
expander = st.beta_expander("Inquiry2")
expander.write("Taipei Office: XX-XXXX-XXXX")
expander.write("Shanghai Office: XX-XXXX-XXXX")
expander = st.beta_expander("Inquiry3")
expander.write("Singapore Office: XX-XXXX-XXXX")
expander.write("Munbai Office: XX-XXXX-XXXX")

