def get_style():
    return """
        <style>
        .stApp {
            background-color: #C8E6C9 !important;
        }
        .main .block-container {
            background-color: #C8E6C9 !important;
        }
        h1, h2, h3  {
            font-family: sans-serif !important;
            font-weight: 150 !important;
            color: #008a6b !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #B8DDB9 !important;
        }
        header[data-testid="stHeader"] {
            background-color: #C8E6C9 !important;
        }
        header[data-testid="stHeader"]::before {
            content: "Income Inequality";
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 24px;
            font-weight: bold;
            color: #008a6b;
        }
        .stTable, .dataframe {
            background-color: #FFFFFF !important;
            border: 1px solid #A5D6A7 !important;
            border-radius: 8px !important;
        }
        .stTable th, .dataframe th {
            background-color: #81C784 !important;
            color: #FFFFFF !important;
            font-weight: 500 !important;
            font-family: sans-serif !important;
            text-align: center !important;
        }
        .stTable td, .dataframe td {
            background-color: #F1F8E9 !important;
            color: #2E7D32 !important;
            font-family: sans-serif !important;
            text-align: center !important;
        }
        .stMarkdown p {
            font-size: 14px !important;
        }
        </style>
    """
