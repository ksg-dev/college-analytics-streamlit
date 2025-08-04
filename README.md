# 🎓 College Major Analytics Dashboard
 
 An interactive Streamlit application for analyzing college major salary data and providing 
 personalized career guidance based on data-driven insights.
 
## Features
- 📊 Comprehensive salary analysis across major groups (STEM, Business, HASS)
- ⚖️ Risk vs reward analysis with salary spread calculations
- 📈 Career growth potential visualization  
- 🎯 Personalized career recommendations based on priorities
- 🧠 Personality-based major matching
- 🔍 Interactive major comparison tools
- 📱 Mobile-responsive design with AURA theme integration
 
## Data Sources
Based on college major salary survey data including:
- Starting median salaries for new graduates
- Mid-career median salaries (10+ years experience)
- Major category groupings (STEM, Business, HASS)
- Job satisfaction and work-life balance metrics
- Career growth outlook projections
 
## Quick Start
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Place your college_salary_data.csv in the data/ folder
4. Run the app: `streamlit run main.py`
 
## Live Demo
[Deploy to Streamlit Cloud for easy sharing]
 
## Key Insights
- STEM majors typically offer highest starting salaries
- Business majors show strong mid-career growth potential
- HASS majors vary widely but offer valuable transferable skills
- Work-life balance and job satisfaction vary significantly by field

## Technical Implementation
- **Data Processing**: Pandas for data manipulation and analysis
- **Visualization**: Plotly for interactive charts and graphs
- **UI Framework**: Streamlit with custom CSS theming
- **Analytics**: Risk analysis, growth calculations, personalized scoring

Built with ❤️ for data-driven career decisions  
Part of the AURA Portfolio Project Evolution Series

---

### Data structure expected in college_salary_data.csv:
Undergraduate Major,Starting Median Salary,Mid-Career Median Salary,Group
Computer Science,55900,95000,STEM
Business Management,43000,72000,Business
Psychology,35900,60400,HASS
etc...

### Enhancement opportunities:
- Integration with live job market APIs
- Machine learning recommendation engine
- Geographic salary variation analysis
- Industry-specific breakdowns
- Alumni outcome tracking
- Skills gap analysis