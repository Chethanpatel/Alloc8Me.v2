import streamlit as st
import pandas as pd
import json
from streamlit_option_menu import option_menu
import base64
from fpdf import FPDF
from io import BytesIO

st.set_page_config(
    page_title="Alloc8Me",
    page_icon= 'multimedia/logo.png',
    layout="wide"
)

# hide_default_format = """
#        <style>
#        #MainMenu {visibility: hidden; }
#        footer {visibility: hidden;}
#        </style>
#        """
# st.markdown(hide_default_format, unsafe_allow_html=True)

# Use HTML and CSS to center-align the title
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-top: -50px;
        margin-bottom: 20px;
    }
    .tagline {
        text-align: center;
        font-size: 15px;
        font-weight: italics;
        margin-top: -10px;
        margin-bottom: 10px;   
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: white;
        text-align: right;
        padding: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    .footer a {
        color: white;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="title">Alloc8Me</div>
    <div class="tagline"> Know your Chances, Find your Perfect College Fit</div>
    <div class="footer"><a href="https://www.linkedin.com/in/chethanpatelpn" target="_blank"> Developed by Chethan Patel  </a></div>
    
""", unsafe_allow_html=True)

generate_option_entry = False
generate_probable_colleges = False

disclaimer_text = """ Alloc8Me predictions are based purely on KCET 2023 cutoff data published by Karnataka Examination Authority, Bengaluru. Please use the information provided as guidance, as admission outcomes can vary each year based on multiple factors.
"""

class PDF(FPDF):
    def __init__(self, header_title, disclaimer_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_title = header_title
        self.disclaimer_text = disclaimer_text

    def header(self):
        self.set_font('Times', 'B', 12)
        self.cell(0, 10, self.header_title, 0, 1, 'C')
        
    def footer(self):
        self.set_y(-10)
        self.set_font('Times', 'I', 8)
        col_width = (self.w - 2 * self.l_margin) / 6
        
        # # # Line separator
        # self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())

        # Footer content
        self.cell(col_width, 8, 'Developed by Chethan Patel', 0, 0, 'L', link='https://github.com/Chethanpatel')
        self.cell(col_width, 8, 'Email', 0, 0, 'C', link='mailto:helpfromchethan@gmail.com')
        self.cell(col_width, 8, 'LinkedIn', 0, 0, 'C', link='https://www.linkedin.com/in/chethanpatelpn')
        self.cell(col_width, 8, 'Portfolio', 0, 0, 'C', link='https://chethanpatelpn.netlify.app/')
        self.cell(col_width, 8, 'YouTube', 0, 0, 'C', link='https://www.appopener.com/yt/vb38mqp9c')
        self.cell(col_width, 8, 'Medium', 0, 0, 'C', link='https://medium.com/@chethanpatel')
        self.cell(col_width, 8, ' %s ' % self.page_no(), 0, 0, 'L')

        # # Line separator
        # self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())

        # Disclaimer
        self.set_y(-20)
        self.set_x(self.l_margin)
        self.set_font('Times', 'B', 8)
        self.multi_cell(self.w - 2 * self.l_margin, 5, f"Disclaimer: {self.disclaimer_text}", 0, 'L')

    def table(self, df):
        effective_page_width = self.w - 2 * self.l_margin
        col_widths = [5, 75, 55, 15]
        if generate_option_entry == True:
            col_widths = [5, 75, 55, 15]  # Custom column widths
        if generate_option_entry == True:
            col_widths = [10, 75, 55, 15]
        col_width_proportions = [w / sum(col_widths) for w in col_widths]
        col_widths_actual = [effective_page_width * prop for prop in col_width_proportions]
        row_height = self.font_size * 1.5

        # Print column headers
        self.set_font('Times', 'B', 8)
        for col, width in zip(df.columns, col_widths_actual):
            self.cell(width, row_height, str(col), border=1, ln=0, align='L')
        self.ln(row_height)

        # Print rows
        self.set_font('Times', '', 6)
        for row in df.itertuples(index=False):
            for value, width in zip(row, col_widths_actual):
                self.cell(width, row_height, str(value), border=1, ln=0, align='L')
            self.ln(row_height)

# Load JSON files and extract lists
def load_json(file_path, key):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data[key]

category_options = load_json('./dropdown/unique_category.json', 'Category')
city_options = load_json('./dropdown/unique_city.json', 'City') 
course_options = load_json('./dropdown/unique_courses.json', 'Course')
institution_options = load_json('./dropdown/unique_institutions.json', 'Institution')

# Load dataframe
df = pd.read_csv('./assets/dataset.csv')

# hide_default_format = """
#        <style>
#        #MainMenu {visibility: hidden; }
#        footer {visibility: hidden;}
#        </style>
#        """
# st.markdown(hide_default_format, unsafe_allow_html=True)


# # Sidebar for selecting the key feature
# key_feature = st.sidebar.selectbox(
#     'Select Key Feature',
#     [
#         'Home',
#         'Generate the Probable College List',
#         'Show Exact Cutoff Information',
#         'Generate the Expert Option Entry List',
#         'Compute Rank Difference'
#     ],
#     index=0  # Default to 'Home'
# )

key_feature = option_menu(None, ["Home", "Probable Colleges",  "Cutoff Info", 'Expert Option Entry', 'Rank Difference'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": 5, "background-color": "#1a3e66"},
        "icon": {"color": "white", "font-size": "10px"}, 
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#"},
        "nav-link-selected": { "background-color": "#ff4b4b" }
        }
)

# ["Home", "Generate the Probable College List",  "Show Exact Cutoff Information", 'Generate the Expert Option Entry List', 'Compute Rank Difference']
# ["Home", "Probable Colleges",  "Cutoff Info", 'Expert Option Entry', 'Rank Diff']

# Home page content
if key_feature == 'Home':
    # Path to your GIF file
    gif_path = "multimedia/Alloc8Me.gif"

    # Read the GIF file and encode it as a base64 string

    def get_gif_base64(gif_path):
        with open(gif_path, "rb") as gif_file:
            gif_bytes = gif_file.read()
            encoded_gif = base64.b64encode(gif_bytes).decode("utf-8")
        return encoded_gif

    encoded_gif = get_gif_base64(gif_path)

    # Display the GIF using HTML and base64 encoding
    html_code = f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/gif;base64,{encoded_gif}" width="720">
    </div>
    """

    st.markdown(html_code, unsafe_allow_html=True)
         
    # # Add custom HTML content to the sidebar
    # sidebar_html = """
    # <style>
    # .sidebar-section {
    #     margin-bottom: 20px;
    # }
    # .sidebar-section h2 {
    #     color: blue;
    #     margin-bottom: 5px;
    # }
    # .sidebar-section p {
    #     color: black;
    # }
    # </style>

    # <div class="sidebar-section">
    #     <h2>1. Generate the Probable College List</h2>
    #     <p>
    #         Alloc8Me predicts colleges where you have a strong chance of admission based on your rank,
    #         selected branches, locations, and category. It also identifies colleges where your chances are
    #         lower, providing insight into realistic college options.
    #     </p>
    # </div>
    # <div class="sidebar-section">
    #     <h2>2. Show Exact Cutoff Information</h2>
    #     <p>
    #         Alloc8Me displays detailed cutoff trends for your selected college, branches, and category.
    #         This helps you understand the competitiveness of colleges over the years, aiding in informed
    #         decision-making during admissions.
    #     </p>
    # </div>
    # <div class="sidebar-section">
    #     <h2>3. Generate the Expert Option Entry List</h2>
    #     <p>
    #         Alloc8Me generates a recommended list of preferences for your option entry process. These
    #         suggestions are backed by historical data and expert insights, maximizing your chances of
    #         securing admission in preferred colleges.
    #     </p>
    # </div>
    # <div class="sidebar-section">
    #     <h2>4. Compute Rank Difference b/w your Rank and Cut-Off</h2>
    #     <p>
    #         Alloc8Me calculates the difference between your rank and the cutoff rank of selected college.
    #         It categorizes colleges as high or low probability options, providing clarity on the feasibility
    #         of securing admission for the selected college.
    #     </p>
    # </div>
    # """

    # st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)
    

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.subheader("Generate the Probable College List")
    #     st.info("""
    #         Alloc8Me predicts colleges where you have a strong chance of admission based on your rank,
    #         selected branches, locations, and category. It also identifies colleges where your chances are
    #         lower, providing insight into realistic college options.
    #     """)
    # with col2:
    #     st.subheader("Show Exact Cutoff Information")
    #     st.info("""
    #         Alloc8Me displays detailed cutoff trends for your selected college, branches, and category.
    #         This helps you understand the competitiveness of colleges over the years, aiding in informed
    #         decision-making during admissions.
    #     """)
    # col3, col4 = st.columns(2)
    # with col3:
    #     st.subheader("Generate the Expert Option Entry List")
    #     st.info("""
    #         Alloc8Me generates a recommended list of preferences for your option entry process. These
    #         suggestions are backed by historical data and expert insights, maximizing your chances of
    #         securing admission in preferred colleges.
    #     """)
    # with col4:
    #     st.subheader("Compute Rank Difference b/w your Rank and Cut-Off")
    #     st.info("""
    #         Alloc8Me calculates the difference between your rank and the cutoff rank of selected college.
    #         It categorizes colleges as high or low probability options, providing clarity on the feasibility
    #         of securing admission for the selected college.
    #     """)

# Define mappings from category-specific columns
category_mappings = {
    '1G': 'Category-1',
    '1K': 'Category-1',
    '1R': 'Category-1',
    '2AG': 'Category-2A',
    '2AK': 'Category-2A',
    '2AR': 'Category-2A',
    '2BG': 'Category-2B',
    '2BK': 'Category-2B',
    '2BR': 'Category-2B',
    '3AG': 'Category-3A',
    '3AK': 'Category-3A',
    '3AR': 'Category-3A',
    '3BG': 'Category-3B',
    '3BK': 'Category-3B',
    '3BR': 'Category-3B',
    'GM': 'Category-GM',
    'GMK': 'Category-GM',
    'GMR': 'Category-GM',
    'SCG': 'Category-SC',
    'SCK': 'Category-SC',
    'SCR': 'Category-SC',
    'STG': 'Category-ST',
    'STK': 'Category-ST',
    'STR': 'Category-ST'
}

# Feature: Generate the Probable College List
if key_feature == 'Probable Colleges':
    generate_probable_colleges = True
    st.subheader("Generate the Probable College List")
    st.write("""
        Alloc8Me predicts colleges where you have a strong chance of admission based on your rank,
        selected branches, locations, and category. It also identifies colleges where your chances are
        lower, providing insight into realistic college options.
    """)
    
    # Load dataframe
    df = pd.read_csv('./assets/dataset.csv')

    rank = st.sidebar.number_input('Enter Rank', min_value=1)
    branches = st.sidebar.multiselect('Select Branch(es)', options=course_options)
    locations = st.sidebar.multiselect('Select Location(s)', options=city_options)
    category = st.sidebar.selectbox('Select Category', options=category_options)

    # Get the mapped category column based on the selected category
    category_column = category_mappings[category]

    # Filter the DataFrame based on the selected options
    filtered_df = df[
        (df['City'].isin(locations) if locations else True) &
        (df['Course'].isin(branches) if branches else True) &
        (df[f'{category_column}_max'].notna())
    ]

    probable_list = filtered_df[
    ((filtered_df[f'{category_column}_max'] >= rank) & 
     (filtered_df[f'{category_column}_max'] > 0) & 
     (filtered_df[f'{category_column}_max'] != 0) & 
     (filtered_df['AvgCutoffRank'] >= rank))
    ]
    
  
    not_probable_list = filtered_df[
    ((filtered_df[f'{category_column}_max'] < rank) & 
     (filtered_df[f'{category_column}_max'] > 0) & 
     (filtered_df[f'{category_column}_max'] != 0 & (filtered_df['AvgCutoffRank'] > 0))) 
    ]
    
    probable_list = probable_list[['Institution', 'Course', 'City']]
    not_probable_list = not_probable_list[['Institution', 'Course', 'City']]
    
    probable_list.insert(0, ' ', range(1, len(probable_list) + 1))
    not_probable_list.insert(0, ' ', range(1, len(not_probable_list) + 1))
    

    # Display information message
    if len(probable_list) == 0 and len(not_probable_list) == 0:
        st.info("No colleges found based on the selected criteria.")

    # Display probable and not probable lists
    if len(probable_list) > 0:
        st.write("### High Probability Colleges")
        st.dataframe(probable_list[[' ', 'Institution', 'Course', 'City']].style.set_properties(**{'max-height': '300px', 'overflow-y': 'auto'}), hide_index = True)
        header_title = "Probable College List"
        pdf = PDF(header_title, disclaimer_text)
        pdf.add_page()
        pdf.table(probable_list)

        # Save the PDF to a BytesIO object
        pdf_buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="Probable College List.pdf",
            mime="application/pdf"
        )
    else:
        st.write("No colleges found in the high probability list.")
        


    st.write("### Low Probability Colleges")
    if len(not_probable_list) > 0:
        st.dataframe(not_probable_list[[' ', 'Institution', 'Course', 'City']].style.set_properties(**{'max-height': '300px', 'overflow-y': 'auto'}), hide_index = True)
        
        header_title = "Non-Probable College List"
        pdf = PDF(header_title, disclaimer_text)
        pdf.add_page()
        pdf.table(not_probable_list)

        # Save the PDF to a BytesIO object
        pdf_buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="Non-Probable College List.pdf",
            mime="application/pdf"
        )
    else:
        st.write("No colleges found in the low probability list.")
        
    
        

# Feature: Show Exact Cutoff Information
if key_feature == 'Cutoff Info':
    st.subheader("Show Exact Cutoff Information")
    st.write("""
        Alloc8Me displays detailed cutoff trends for your selected college, branches, and category.
        This helps you understand the competitiveness of colleges over the years, aiding in informed
        decision-making during admissions.
    """)

    # Load dataframe
    df = pd.read_csv('./assets/dataset.csv')
    
    # Load JSON file containing institution courses
    with open('./dropdown/institutions_courses.json', 'r') as file:
        institution_courses = json.load(file)

    # Get list of colleges from the JSON keys
    colleges = list(load_json('./dropdown/unique_institutions.json', 'Institution'))

    # Sidebar dropdown for selecting college
    selected_college = st.sidebar.selectbox('Select College', colleges)

    # Dropdown for selecting branches based on selected college
    if selected_college:
        branches = institution_courses[selected_college]
        selected_branch = st.sidebar.selectbox('Select Branch', branches)
        category = st.sidebar.selectbox('Select Category', options=category_options)
        st.sidebar.write(f"Selected Branch: {selected_branch}")

    # # Sidebar inputs
    # selected_college = st.sidebar.selectbox('Select College', options=institution_options)
    # selected_branch = st.sidebar.selectbox('Select Branch', options=course_options)
    
    # Get the mapped category column based on the selected category
    category_column = category_mappings[category]

    # Filter the DataFrame based on the selected college and branch
    filtered_df = df[(df['Institution'] == selected_college) & (df['Course'] == selected_branch)]

    # Display data
    if not filtered_df.empty:
        filtered_df_display = filtered_df[['Institution','Course', f'{category_column}_min', f'{category_column}_max']]
        filtered_df_display.replace(0, 'NA', inplace=True)
        filtered_df_display.reset_index(drop=True, inplace=True)  # Reset the index without adding it as a column
        st.write(f"### Cutoff Information for {selected_branch} at {selected_college}")
        st.dataframe(filtered_df_display, hide_index = True)
        keyIndicator = True
    else:
        st.warning("No data available for the selected college and branch.")
        keyIndicator = False
        
    if keyIndicator == True:
        # Add key indicator for category_min and category_max columns
        st.info(f"""
            **Key Indicators:**
            - `{category_column}_min`: Minimum rank required for admission in the selected category.
            - `{category_column}_max`: Maximum rank up to which admission was granted in the selected category.
        """)
# Feature: Generate the Expert Option Entry List
if key_feature == 'Expert Option Entry':
    generate_option_entry = True
    st.subheader("Generate the Expert Option Entry List")
    st.write("""
        Alloc8Me generates a recommended list of preferences for your option entry process. These
        suggestions are backed by historical data and expert insights, maximizing your chances of
        securing admission in preferred colleges.
    """)

    # Sidebar inputs
    selected_rank = st.sidebar.number_input('Enter Rank', min_value=1)
    selected_branches = st.sidebar.multiselect('Select Branch(es)', options=course_options)
    selected_cities = st.sidebar.multiselect('Select City', options=city_options)
    selected_category = st.sidebar.selectbox('Select Category', options=category_options)

    # Get the mapped category column based on the selected category
    category_column = category_mappings[selected_category]
    
    # Load the option entry data (replace with your CSV file path)
    df = pd.read_csv('./dataset/option_entry.csv')

    # Calculate the cutoff rank threshold
    cutoff_rank_threshold = selected_rank + 100000  # Adjusted value based on your requirements

    # Filter the DataFrame based on the selected criteria
    if selected_branches:
        branch_filter = df['Course'].isin(selected_branches)
    else:
        branch_filter = df.index.notna()  # Select all if branches are not selected

    if selected_cities:
        city_filter = df['City'].isin(selected_cities)
    else:
        city_filter = df.index.notna()  # Select all if cities are not selected

    filtered_df = df[
        branch_filter &
        city_filter &
        (df[f'{category_column}_max'] < cutoff_rank_threshold) &
        (df[f'{category_column}_max'] > 0)
    ]

    # Sort by average cutoff rank
    filtered_df_sorted = filtered_df.sort_values(by='AvgCutoffRank')

    # Display the option entry list
    if not filtered_df_sorted.empty:
        st.write(f"### Recommended Option Entry List for Category {selected_category}")
        filtered_df_display = filtered_df_sorted[['Institution', 'Course', 'City']].reset_index(drop=True)
        filtered_df_display.insert(0, 'Choice', range(1, len(filtered_df_display) + 1))
        st.dataframe(filtered_df_display, hide_index = True)
        
        
        # header_title = f"Recommended Option Entry List, According to your rank {selected_rank}, branch(es) {selected_branches}, and Categoty {selected_category} "
        
        header_title ="Recommended Option Entry List"
        pdf = PDF(header_title, disclaimer_text)
        pdf.add_page()
        pdf.table(filtered_df_display)

        # Save the PDF to a BytesIO object
        pdf_buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_output)
        pdf_buffer.seek(0)

        st.download_button(
            label="Download Recommended Option Entry List",
            data=pdf_buffer,
            file_name="Recommended Option Entry List.pdf",
            mime="application/pdf"
        )
        
    else:
        st.warning("No colleges found matching the criteria.")

# Feature: Compute Rank Difference
if key_feature == 'Rank Difference':
    st.subheader("Compute Rank Difference")
    st.write("""
        Alloc8Me calculates the difference between your rank and the cutoff rank of selected colleges.
        This helps you understand the feasibility of securing admission based on historical data.
    """)
    
    # Load dataframe
    df = pd.read_csv('./assets/dataset.csv')

    # Load JSON file containing institution courses
    with open('./dropdown/institutions_courses.json', 'r') as file:
        institution_courses = json.load(file)

    # Get list of colleges from the JSON keys
    colleges = list(load_json('./dropdown/unique_institutions.json', 'Institution')
)

    # Sidebar dropdown for selecting college
    selected_college = st.sidebar.selectbox('Select College', colleges)

    # Dropdown for selecting branches based on selected college
    if selected_college:
        branches = institution_courses[selected_college]
        selected_branch = st.sidebar.selectbox('Select Branch', branches)
        category = st.sidebar.selectbox('Select Category', options=category_options)
        selected_rank = st.sidebar.number_input('Enter Your Rank', min_value=1)
        st.sidebar.write(f"Selected Branch: {selected_branch}")

    # Get the mapped category column based on the selected category
    category_column = category_mappings[category]

    # Filter the DataFrame based on the selected college and branch
    filtered_df = df[(df['Institution'] == selected_college) & (df['Course'] == selected_branch)]

    # Compute rank difference
    if not filtered_df.empty:
        # Calculate rank difference
        filtered_df['Rank_Difference'] = filtered_df[f'{category_column}_max'] - selected_rank

        # Display data
        filtered_df_display = filtered_df[['Institution', 'Course', f'{category_column}_max', 'Rank_Difference']]
        filtered_df_display.replace(0, 'NA', inplace=True)
        filtered_df_display.reset_index(drop=True, inplace=True)  # Reset the index without adding it as a column
        st.write(f"### Rank Difference for {selected_branch} at {selected_college}")
        st.dataframe(filtered_df_display, hide_index = True)

        # Determine admission chances
        min_rank_diff = filtered_df['Rank_Difference'].min()
        if min_rank_diff > 0:
            st.warning(f"Hurray! You might get a seat. Your best rank difference is {min_rank_diff}.")
        else:
            st.warning(f"Oops! Less chance of getting a seat. Your best rank difference is {min_rank_diff}.")

        keyIndicator = True
    else:
        st.warning("No data available for the selected college and branch.")
        keyIndicator = False

    if keyIndicator:
        # Add key indicator for category_min and category_max columns
        st.info(f"""
            **Key Indicators:**
            - `{category_column}_max`: Maximum rank up to which admission was granted in the selected category.
            - `Rank_Difference`: Difference between your rank and the cutoff rank. A negative value indicates a higher chance of admission.
        """)

