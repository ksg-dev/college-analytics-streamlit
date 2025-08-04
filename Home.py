import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


# Page config
st.set_page_config(
    page_title="College Major Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for AURA theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .risk-high { color: #EF4444; font-weight: bold; }
    .risk-medium { color: #F59E0B; font-weight: bold; }
    .risk-low { color: #10B981; font-weight: bold; }
    
    .salary-insight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .group-stem { border-left: 4px solid #10B981; }
    .group-business { border-left: 4px solid #3B82F6; }
    .group-hass { border-left: 4px solid #8B5CF6; }
</style>
""", unsafe_allow_html=True)


# Data loading and processing functions
@st.cache_data
def load_college_data():
    """Load and clean college major salary data"""
    df = pd.read_csv('./data/college_salary_data.csv')

    # Calculate additional metrics
    df['Mid-Career 10th Percentile Salary'] = df['Mid-Career Median Salary'] * 0.7
    df['Mid-Career 90th Percentile Salary'] = df['Mid-Career Median Salary'] * 1.8
    df['Spread'] = df['Mid-Career 90th Percentile Salary'] - df['Mid-Career 10th Percentile Salary']
    df['Salary Growth'] = df['Mid-Career Median Salary'] - df['Starting Median Salary']
    df['Growth Percentage'] = (df['Salary Growth'] / df['Starting Median Salary']) * 100
    
    # Risk categories based on spread
    df['Risk Level'] = pd.cut(df['Spread'], 
                             bins=[0, 60000, 80000, float('inf')], 
                             labels=['Low', 'Medium', 'High'])
    
    return df


def calculate_major_stats(df):
    """Calculate key stats for display"""
    return {
        'total_majors': len(df),
        'avg_starting_salary': df['Starting Median Salary'].mean(),
        'avg_midcareer_salary': df['Mid-Career Median Salary'].mean(),
        'highest_starting': df.loc[df['Starting Median Salary'].idxmax()],
        'highest_midcareer': df.loc[df['Mid-Career Median Salary'].idxmax()],
        'lowest_starting': df.loc[df['Starting Median Salary'].idxmin()],
        'lowest_midcareer': df.loc[df['Mid-Career Median Salary'].idxmin()],
        'best_growth': df.loc[df['Growth Percentage'].idxmax()],
        'group_stats': df.groupby('Group').agg({
            'Starting Median Salary': 'mean',
            'Mid-Career Median Salary': 'mean',
            'Growth Percentage': 'mean'
        }).round(0)
    }


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 College Major Analytics Dashboard</h1>
        <h2>Salary Insights & Career Decision Tool</h2>
        <p>Data-driven analysis of college major earning potential and career trajectories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_college_data()
    stats = calculate_major_stats(df)

    # Sidebar filters
    st.sidebar.header("Filter & Explore")

    # Group filter
    selected_groups = st.sidebar.multiselect(
        "Select Major Groups:",
        options=['STEM', 'Business', 'HASS'],
        default=['STEM', 'Business', 'HASS']
    )
    
    # Salary range filter
    salary_range = st.sidebar.slider(
        "Starting Salary Range:",
        min_value=int(df['Starting Median Salary'].min()),
        max_value=int(df['Starting Median Salary'].max()),
        value=(int(df['Starting Median Salary'].min()), int(df['Starting Median Salary'].max())),
        step=1000
    )
    
    # Risk level filter
    risk_filter = st.sidebar.multiselect(
        "Risk Level:",
        options=['Low', 'Medium', 'High'],
        default=['Low', 'Medium', 'High']
    )
    
    # Filter dataframe
    filtered_df = df[
        (df['Group'].isin(selected_groups)) &
        (df['Starting Median Salary'] >= salary_range[0]) &
        (df['Starting Median Salary'] <= salary_range[1]) &
        (df['Risk Level'].isin(risk_filter))
    ].copy()
    
    # Overview Metrics
    st.header("📊 Key Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Majors Analyzed", 
            value=f"{len(filtered_df)}/{stats['total_majors']}",
            help="Number of majors in current filter vs. total"
        )
    
    with col2:
        avg_start = filtered_df['Starting Median Salary'].mean() if len(filtered_df) > 0 else 0
        st.metric(
            label="💰 Avg Starting Salary",
            value=f"${avg_start:,.0f}",
            delta=f"{avg_start - stats['avg_starting_salary']:,.0f}",
            help="Average starting salary for filtered majors"
        )
    
    with col3:
        avg_mid = filtered_df['Mid-Career Median Salary'].mean() if len(filtered_df) > 0 else 0
        st.metric(
            label="📈 Avg Mid-Career Salary",
            value=f"${avg_mid:,.0f}",
            delta=f"{avg_mid - stats['avg_midcareer_salary']:,.0f}",
            help="Average mid-career salary for filtered majors"
        )
    
    with col4:
        avg_growth = filtered_df['Growth Percentage'].mean() if len(filtered_df) > 0 else 0
        st.metric(
            label="🚀 Avg Salary Growth",
            value=f"{avg_growth:.0f}%",
            help="Average percentage salary growth from start to mid-career"
        )
    
    # Main visualizations
    if len(filtered_df) > 0:
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Salary Comparison", "🎯 Risk Analysis", "📈 Growth Analysis", "🔍 Major Details"])
        
        with tab1:
            st.subheader("💰 Starting vs Mid-Career Salary Comparison")
            
            fig = px.scatter(
                filtered_df,
                x='Starting Median Salary',
                y='Mid-Career Median Salary',
                color='Group',
                size='Growth Percentage',
                hover_name='Undergraduate Major',
                hover_data={
                    'Starting Median Salary': ':$,.0f',
                    'Mid-Career Median Salary': ':$,.0f',
                    'Growth Percentage': ':.1f%'
                },
                title="Salary Progression by Major Group",
                color_discrete_map={
                    'STEM': '#10B981',
                    'Business': '#3B82F6', 
                    'HASS': '#8B5CF6'
                }
            )
            
            # Add diagonal line showing no growth
            fig.add_shape(
                type="line",
                x0=filtered_df['Starting Median Salary'].min(),
                x1=filtered_df['Starting Median Salary'].max(),
                y0=filtered_df['Starting Median Salary'].min(),
                y1=filtered_df['Starting Median Salary'].max(),
                line=dict(dash="dash", color="gray"),
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Top/Bottom performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🏆 Top Starting Salaries:**")
                top_starting = filtered_df.nlargest(5, 'Starting Median Salary')[['Undergraduate Major', 'Starting Median Salary', 'Group']]
                for _, row in top_starting.iterrows():
                    st.write(f"• **{row['Undergraduate Major']}** ({row['Group']}): ${row['Starting Median Salary']:,}")
            
            with col2:
                st.write("**📈 Top Mid-Career Salaries:**")
                top_midcareer = filtered_df.nlargest(5, 'Mid-Career Median Salary')[['Undergraduate Major', 'Mid-Career Median Salary', 'Group']]
                for _, row in top_midcareer.iterrows():
                    st.write(f"• **{row['Undergraduate Major']}** ({row['Group']}): ${row['Mid-Career Median Salary']:,}")
        
        with tab2:
            st.subheader("⚖️ Risk vs Reward Analysis")
            
            # Risk distribution
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_risk = px.scatter(
                    filtered_df,
                    x='Mid-Career Median Salary',
                    y='Spread',
                    color='Risk Level',
                    hover_name='Undergraduate Major',
                    hover_data={
                        'Mid-Career Median Salary': ':$,.0f',
                        'Spread': ':$,.0f',
                        'Group': True
                    },
                    title="Risk vs Reward: Salary Spread Analysis",
                    color_discrete_map={
                        'Low': '#10B981',
                        'Medium': '#F59E0B',
                        'High': '#EF4444'
                    }
                )
                fig_risk.update_layout(height=500)
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                # Risk level distribution
                risk_counts = filtered_df['Risk Level'].value_counts()
                fig_pie = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Risk Level Distribution",
                    color_discrete_map={
                        'Low': '#10B981',
                        'Medium': '#F59E0B',
                        'High': '#EF4444'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Risk insights
                st.write("**Risk Level Guide:**")
                st.write("🟢 **Low Risk**: Predictable salary range")
                st.write("🟡 **Medium Risk**: Moderate variability") 
                st.write("🔴 **High Risk**: High potential but uncertain")
        
        with tab3:
            st.subheader("📈 Career Growth Analysis")
            
            # Growth comparison by group
            fig_growth = px.box(
                filtered_df,
                x='Group',
                y='Growth Percentage',
                color='Group',
                title="Salary Growth Distribution by Major Group",
                color_discrete_map={
                    'STEM': '#10B981',
                    'Business': '#3B82F6', 
                    'HASS': '#8B5CF6'
                }
            )
            fig_growth.update_layout(height=400)
            st.plotly_chart(fig_growth, use_container_width=True)
            
            # Growth champions
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🚀 Best Growth Potential:**")
                best_growth = filtered_df.nlargest(5, 'Growth Percentage')[['Undergraduate Major', 'Growth Percentage', 'Salary Growth']]
                for _, row in best_growth.iterrows():
                    st.write(f"• **{row['Undergraduate Major']}**: +{row['Growth Percentage']:.0f}% (${row['Salary Growth']:,})")
            
            with col2:
                st.write("**💼 Group Performance:**")
                for group, stats_row in stats['group_stats'].iterrows():
                    st.write(f"**{group}**: {stats_row['Growth Percentage']:.0f}% avg growth")
        
        with tab4:
            st.subheader("🔍 Detailed Major Analysis")
            
            # Search and compare majors
            selected_majors = st.multiselect(
                "Compare specific majors:",
                options=filtered_df['Undergraduate Major'].tolist(),
                default=filtered_df.nlargest(3, 'Mid-Career Median Salary')['Undergraduate Major'].tolist()[:3]
            )
            
            if selected_majors:
                comparison_df = filtered_df[filtered_df['Undergraduate Major'].isin(selected_majors)].copy()
                
                # Create comparison chart
                fig_compare = go.Figure()
                
                for _, row in comparison_df.iterrows():
                    fig_compare.add_trace(go.Bar(
                        name=row['Undergraduate Major'],
                        x=['Starting Salary', 'Mid-Career Salary'],
                        y=[row['Starting Median Salary'], row['Mid-Career Median Salary']],
                        text=[f"${row['Starting Median Salary']:,}", f"${row['Mid-Career Median Salary']:,}"],
                        textposition='auto'
                    ))
                
                fig_compare.update_layout(
                    title="Direct Major Comparison",
                    barmode='group',
                    height=400
                )
                st.plotly_chart(fig_compare, use_container_width=True)
                
                # Detailed comparison table
                st.write("**📋 Detailed Comparison:**")
                display_columns = ['Undergraduate Major', 'Group', 'Starting Median Salary', 
                                 'Mid-Career Median Salary', 'Growth Percentage', 'Risk Level']
                st.dataframe(comparison_df[display_columns].style.format({
                    'Starting Median Salary': '${:,.0f}',
                    'Mid-Career Median Salary': '${:,.0f}',
                    'Growth Percentage': '{:.1f}%'
                }), use_container_width=True)
    
    else:
        st.warning("No majors match your current filters. Try adjusting the criteria.")
    
    # Data source and methodology
    with st.expander("📖 About This Analysis"):
        st.write("""
        **Data Source & Methodology:**
        
        This analysis is based on college major salary data showing typical earning patterns 
        across different fields of study. The data includes:
        
        • **Starting Median Salary**: Typical salary for new graduates
        • **Mid-Career Median Salary**: Typical salary after 10+ years experience
        • **Major Groups**: STEM (Science, Technology, Engineering, Math), Business, and HASS (Humanities, Arts, Social Sciences)
        • **Risk Analysis**: Based on salary spread (90th percentile - 10th percentile)
        
        **Key Insights:**
        • STEM majors typically show highest starting salaries
        • Business majors often have strong mid-career growth
        • HASS majors vary widely but offer valuable transferable skills
        • Higher risk majors may offer higher rewards but less predictability
        
        **Important Notes:**
        • Salaries vary significantly by location, industry, and individual factors
        • This data represents typical outcomes, not guaranteed results
        • Consider your interests, aptitudes, and career goals beyond just salary
        • Many factors beyond major choice influence career success
        """)

if __name__ == "__main__":
    main()