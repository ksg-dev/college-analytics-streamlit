import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


st.set_page_config(
    page_title="Career Guidance",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS (matching AURA theme)
st.markdown("""
<style>
    .guidance-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .recommendation-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #10B981;
        backdrop-filter: blur(10px);
    }
    
    .risk-recommendation {
        border-left-color: #F59E0B;
    }
    
    .growth-recommendation {
        border-left-color: #3B82F6;
    }
    
    .personality-match {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Enhanced data loading w career insights (sample data added)
@st.cache_data
def load_enhanced_college_data():
    """Load college data w additional career guidance features (sample data)"""
    data = {
        # Enhanced features for career guidance
        'Job_Satisfaction_Score': [
            7.2, 8.1, 6.8, 7.5, 7.8, 8.3, 7.9, 6.9, 7.6, 7.8,
            7.4, 7.1, 8.2, 8.5, 7.0, 7.7, 8.9, 7.9, 8.1, 7.3,
            7.1, 7.2, 6.9, 7.4, 7.8, 7.0, 7.6, 6.8, 7.7, 7.9,
            7.3, 7.0, 6.8, 8.0, 7.8, 8.2, 8.1, 7.4, 8.3, 8.1,
            7.5, 7.8, 7.9, 7.6, 7.2, 8.0, 7.1, 7.6, 7.5, 8.3
        ],
        'Work_Life_Balance': [
            6.5, 6.8, 7.2, 7.8, 6.9, 8.1, 7.1, 6.2, 6.5, 7.0,
            7.0, 7.5, 6.8, 7.2, 6.8, 7.0, 8.5, 6.9, 8.0, 7.1,
            6.3, 7.5, 7.3, 7.2, 7.8, 7.2, 7.9, 7.0, 6.9, 7.1,
            7.4, 7.6, 6.8, 7.3, 6.7, 8.3, 7.8, 7.6, 8.2, 7.4,
            7.2, 7.9, 8.1, 7.7, 7.5, 8.4, 7.3, 7.6, 7.5, 8.1
        ],
        'Job_Growth_Outlook': [
            'Moderate', 'High', 'Moderate', 'Low', 'Moderate', 'Low', 'High', 'Moderate',
            'High', 'High', 'High', 'Low', 'Very High', 'Very High', 'Moderate', 'Moderate',
            'Moderate', 'High', 'Low', 'High', 'Moderate', 'Low', 'Low', 'Moderate',
            'Moderate', 'High', 'Low', 'High', 'High', 'Very High', 'Low', 'Low',
            'Moderate', 'High', 'High', 'Low', 'High', 'Moderate', 'Low', 'High',
            'Low', 'Moderate', 'Low', 'Low', 'Low', 'Low', 'Moderate', 'Low', 'Moderate', 'Moderate'
        ]
    }

    base_df = pd.read_csv('./data/college_salary_data.csv')
    enh_data = pd.DataFrame(data)

    # Add Enhanced Data
    df = base_df.join(enh_data)

    # Calculate additional metrics
    df['Mid-Career 10th Percentile Salary'] = df['Mid-Career Median Salary'] * 0.7
    df['Mid-Career 90th Percentile Salary'] = df['Mid-Career Median Salary'] * 1.8
    df['Spread'] = df['Mid-Career 90th Percentile Salary'] - df['Mid-Career 10th Percentile Salary']
    df['Salary Growth'] = df['Mid-Career Median Salary'] - df['Starting Median Salary']
    df['Growth Percentage'] = (df['Salary Growth'] / df['Starting Median Salary']) * 100
    
    # Risk categories
    df['Risk Level'] = pd.cut(df['Spread'], 
                             bins=[0, 60000, 80000, float('inf')], 
                             labels=['Low', 'Medium', 'High'])
    
    # Career satisfaction composite score
    df['Career_Satisfaction_Score'] = (
        df['Job_Satisfaction_Score'] * 0.4 + 
        df['Work_Life_Balance'] * 0.3 + 
        df['Mid-Career Median Salary'] / 10000 * 0.3
    ).round(1)
    
    return df


def get_personality_recommendations():
    """Career recommendations based on personality types"""
    return {
        'Analytical': {
            'description': 'Detail-oriented, logical thinkers who enjoy problem-solving',
            'recommended_majors': ['Computer Science', 'Mathematics', 'Physics', 'Economics', 'Engineering'],
            'strengths': ['Problem-solving', 'Data analysis', 'Critical thinking'],
            'growth_areas': ['Communication', 'Leadership', 'Creativity']
        },
        'Creative': {
            'description': 'Innovative, artistic individuals who value self-expression',
            'recommended_majors': ['Drama', 'Film', 'Graphic Design', 'Architecture', 'English', 'Music'],
            'strengths': ['Innovation', 'Communication', 'Adaptability'],
            'growth_areas': ['Technical skills', 'Financial planning', 'Structure']
        },
        'People-Oriented': {
            'description': 'Empathetic individuals who enjoy helping and working with others',
            'recommended_majors': ['Psychology', 'Education', 'Nursing', 'Sociology', 'Communications', 'Hospitality & Tourism'],
            'strengths': ['Teamwork', 'Communication', 'Empathy'],
            'growth_areas': ['Technical skills', 'Data analysis', 'Business acumen']
        },
        'Business-Minded': {
            'description': 'Strategic thinkers focused on efficiency and results',
            'recommended_majors': ['Business Management', 'Finance', 'Marketing', 'Economics', 'Accounting'],
            'strengths': ['Leadership', 'Strategic thinking', 'Negotiation'],
            'growth_areas': ['Technical skills', 'Creativity', 'Work-life balance']
        }
    }

def calculate_major_score(row, priorities):
    """Calculate weighted score based on user priorities"""
    score = 0

    # Normalize salary to prevent bias toward high earners (30k-110k range)
    salary_normalized = (row['Mid-Career Median Salary'] - 30000) / 80000
    salary_normalized = max(0, min(1, salary_normalized))  # Clamp to 0-1
    
    # Normalize growth percentage (typical range 0-200%)
    growth_normalized = row['Growth Percentage'] / 200
    growth_normalized = max(0, min(1, growth_normalized))  # Clamp to 0-1
    
    # Satisfaction is already on 0-10 scale, normalize to 0-1
    satisfaction_normalized = row['Career_Satisfaction_Score'] / 10
    
    # Apply weights - ensure they add up to 1.0
    total_weight = priorities['salary'] + priorities['growth'] + priorities['satisfaction']
    if total_weight > 0:
        salary_weight = priorities['salary'] / total_weight
        growth_weight = priorities['growth'] / total_weight
        satisfaction_weight = priorities['satisfaction'] / total_weight
        
        score = (salary_normalized * salary_weight + 
                growth_normalized * growth_weight + 
                satisfaction_normalized * satisfaction_weight)
    else:
        # Equal weighting if no priorities set
        score = (salary_normalized + growth_normalized + satisfaction_normalized) / 3
    
    return score


def main():
    # Header
    st.markdown("""
    <div class="guidance-header">
        <h1>🎯 Career Guidance & Decision Tool</h1>
        <h2>Personalized Major Recommendations</h2>
        <p>Find the right major based on your priorities, personality, and career goals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_enhanced_college_data()
    personality_types = get_personality_recommendations()
    
    # Career Assessment Section
    st.header("🧭 Career Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Your Priorities")
        st.write("Rate the importance of each factor (0-100%):")
        
        salary_priority = st.slider(
            "💰 Salary/Financial Security",
            min_value=0, max_value=100, value=30,
            help="How important is earning potential to you?"
        )
        
        growth_priority = st.slider(
            "📈 Career Growth Potential", 
            min_value=0, max_value=100, value=25,
            help="How important is rapid career advancement?"
        )
        
        satisfaction_priority = st.slider(
            "😊 Job Satisfaction & Work-Life Balance",
            min_value=0, max_value=100, value=45,
            help="How important is enjoying your work and having work-life balance?"
        )
        
        # Normalize priorities to 100%
        total_priority = salary_priority + growth_priority + satisfaction_priority
        if total_priority > 0:
            priorities = {
                'salary': (salary_priority / total_priority) * 100,
                'growth': (growth_priority / total_priority) * 100,
                'satisfaction': (satisfaction_priority / total_priority) * 100
            }
        else:
            priorities = {'salary': 33.3, 'growth': 33.3, 'satisfaction': 33.3}
        
        # Show immediate impact of priority changes
        st.write("**Your Priority Breakdown:**")
        st.write(f"💰 Salary Focus: {priorities['salary']:.1f}%")
        st.write(f"📈 Growth Focus: {priorities['growth']:.1f}%")
        st.write(f"😊 Satisfaction Focus: {priorities['satisfaction']:.1f}%")
    
    with col2:
        st.subheader("🧠 Personality Type")
        selected_personality = st.selectbox(
            "Which best describes you?",
            options=list(personality_types.keys()),
            help="Select the personality type that best matches your preferences"
        )
        
        if selected_personality:
            personality_info = personality_types[selected_personality]
            st.markdown(f"""
            <div class="personality-match">
                <h4>{selected_personality} Type</h4>
                <p>{personality_info['description']}</p>
                <strong>Your Strengths:</strong>
                <ul>
                    {''.join([f'<li>{strength}</li>' for strength in personality_info['strengths']])}
                </ul>
                <strong>Recommended Fields:</strong>
                <ul>
                    {''.join([f'<li>{field}</li>' for field in personality_info['recommended_majors'][:5]])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add refresh button for immediate feedback
        if st.button("🔄 Update Recommendations", help="Click to see how your changes affect the recommendations"):
            st.rerun()
    
    # Calculate personalized recommendations
    df['Personalized_Score'] = df.apply(lambda row: calculate_major_score(row, priorities), axis=1)
    
    # Personality-based filtering
    personality_majors = personality_types[selected_personality]['recommended_majors']
    personality_bonus = 0.3  # Increased to 30% bonus for personality match
    
    # # Debug: Show personality matching
    # st.write(f"**🧠 Personality Type: {selected_personality}**")
    # st.write(f"**Recommended Major Types:** {', '.join(personality_majors)}")
    
    personality_matches = []
    for idx, row in df.iterrows():
        major_name = row['Undergraduate Major']
        is_match = False
        
        # Improved matching logic - check for key terms
        for rec_major in personality_majors:
            if (rec_major.lower() in major_name.lower() or 
                major_name.lower() in rec_major.lower() or
                any(word in major_name.lower() for word in rec_major.lower().split())):
                is_match = True
                personality_matches.append(major_name)
                break
        
        if is_match:
            # Apply significant bonus for personality match
            df.at[idx, 'Personalized_Score'] = min(1.0, df.at[idx, 'Personalized_Score'] + personality_bonus)
    
    # Show which majors got personality bonuses
    if personality_matches:
        st.write(f"**🎯 Personality Matches Found:** {', '.join(personality_matches[:5])}")
    else:
        st.warning("No exact personality matches found - recommendations based on priorities only")
    
    # Don't cap at 1.0 yet - let personality matches stand out
    df['Personalized_Score'] = df['Personalized_Score'].clip(upper=1.5)  # Allow higher scores for personality matches
    
    # Top Recommendations
    st.header("🌟 Your Personalized Recommendations")
    
    top_recommendations = df.nlargest(10, 'Personalized_Score')
    
    # Debug information to show what's affecting rankings
    with st.expander("🔍 See How Rankings Are Calculated"):
        st.write("**Priority Weights:**")
        st.write(f"- Salary: {priorities['salary']:.1f}%")
        st.write(f"- Growth: {priorities['growth']:.1f}%") 
        st.write(f"- Satisfaction: {priorities['satisfaction']:.1f}%")
        
        st.write("**Top 5 Scoring Breakdown:**")
        debug_df = top_recommendations.head(5)[['Undergraduate Major', 'Group', 'Mid-Career Median Salary', 
                                                'Growth Percentage', 'Career_Satisfaction_Score', 'Personalized_Score']]
        st.dataframe(debug_df.style.format({
            'Mid-Career Median Salary': '${:,.0f}',
            'Growth Percentage': '{:.1f}%',
            'Career_Satisfaction_Score': '{:.1f}/10',
            'Personalized_Score': '{:.3f}'
        }))
        
        if personality_matches:
            st.write(f"**Personality Bonus Applied To:** {', '.join(personality_matches)}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recommendation chart
        fig_rec = px.bar(
            top_recommendations.head(8),
            x='Personalized_Score',
            y='Undergraduate Major',
            color='Group',
            title='Top Major Recommendations for You',
            orientation='h',
            color_discrete_map={
                'STEM': '#10B981',
                'Business': '#3B82F6',
                'HASS': '#8B5CF6'
            }
        )
        fig_rec.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_rec, use_container_width=True)
    
    with col2:
        st.write("**🏆 Your Top 5 Matches:**")
        for i, (_, row) in enumerate(top_recommendations.head(5).iterrows(), 1):
            match_percentage = row['Personalized_Score'] * 100
            st.write(f"""
            **{i}. {row['Undergraduate Major']}** ({row['Group']})
            - Match: {match_percentage:.0f}%
            - Starting: ${row['Starting Median Salary']:,}
            - Mid-Career: ${row['Mid-Career Median Salary']:,}
            - Satisfaction: {row['Career_Satisfaction_Score']}/10
            """)
    
    # Detailed Analysis Tabs
    st.header("📊 Detailed Analysis")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Priority Analysis", "💼 Career Outlook", "🔍 Major Deep Dive"])
    
    with tab1:
        st.subheader("How Your Priorities Affect Recommendations")
        
        # Show how different priorities would change recommendations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**💰 If Salary Was Your Top Priority:**")
            salary_focused = df.nlargest(5, 'Mid-Career Median Salary')[['Undergraduate Major', 'Mid-Career Median Salary']]
            for _, row in salary_focused.iterrows():
                st.write(f"• {row['Undergraduate Major']}: ${row['Mid-Career Median Salary']:,}")
        
        with col2:
            st.write("**📈 If Growth Was Your Top Priority:**")
            growth_focused = df.nlargest(5, 'Growth Percentage')[['Undergraduate Major', 'Growth Percentage']]
            for _, row in growth_focused.iterrows():
                st.write(f"• {row['Undergraduate Major']}: +{row['Growth Percentage']:.0f}%")
        
        with col3:
            st.write("**😊 If Satisfaction Was Your Top Priority:**")
            satisfaction_focused = df.nlargest(5, 'Career_Satisfaction_Score')[['Undergraduate Major', 'Career_Satisfaction_Score']]
            for _, row in satisfaction_focused.iterrows():
                st.write(f"• {row['Undergraduate Major']}: {row['Career_Satisfaction_Score']}/10")
        
        # Priority visualization
        st.subheader("Your Priority Breakdown")
        fig_priorities = px.pie(
            values=[priorities['salary'], priorities['growth'], priorities['satisfaction']],
            names=['Salary', 'Growth', 'Satisfaction'],
            title="Your Career Priority Weights"
        )
        st.plotly_chart(fig_priorities, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Career Outlook Analysis")
        
        # Job growth outlook analysis
        outlook_counts = df.groupby(['Group', 'Job_Growth_Outlook']).size().reset_index(name='count')
        
        fig_outlook = px.bar(
            outlook_counts,
            x='Group',
            y='count',
            color='Job_Growth_Outlook',
            title='Job Growth Outlook by Major Group',
            color_discrete_map={
                'Very High': '#10B981',
                'High': '#22C55E',
                'Moderate': '#F59E0B',
                'Low': '#EF4444'
            }
        )
        st.plotly_chart(fig_outlook, use_container_width=True)
        
        # Satisfaction vs Salary scatter
        fig_sat_sal = px.scatter(
            df,
            x='Career_Satisfaction_Score',
            y='Mid-Career Median Salary',
            color='Group',
            size='Work_Life_Balance',
            hover_name='Undergraduate Major',
            title='Career Satisfaction vs Salary (size = work-life balance)',
            color_discrete_map={
                'STEM': '#10B981',
                'Business': '#3B82F6',
                'HASS': '#8B5CF6'
            }
        )
        st.plotly_chart(fig_sat_sal, use_container_width=True)
    
    with tab3:
        st.subheader("🔍 Deep Dive: Major Comparison")
        
        # Select majors for detailed comparison
        selected_majors = st.multiselect(
            "Select majors to compare in detail:",
            options=df['Undergraduate Major'].tolist(),
            default=top_recommendations.head(3)['Undergraduate Major'].tolist()
        )
        
        if selected_majors:
            comparison_df = df[df['Undergraduate Major'].isin(selected_majors)].copy()
            
            # Radar chart for multi-factor comparison
            categories = ['Starting Salary (normalized)', 'Mid-Career Salary (normalized)', 
                         'Job Satisfaction', 'Work-Life Balance', 'Growth %']
            
            fig_radar = go.Figure()
            
            for _, row in comparison_df.iterrows():
                values = [
                    (row['Starting Median Salary'] - df['Starting Median Salary'].min()) / (df['Starting Median Salary'].max() - df['Starting Median Salary'].min()) * 10,
                    (row['Mid-Career Median Salary'] - df['Mid-Career Median Salary'].min()) / (df['Mid-Career Median Salary'].max() - df['Mid-Career Median Salary'].min()) * 10,
                    row['Job_Satisfaction_Score'],
                    row['Work_Life_Balance'], 
                    row['Growth Percentage'] / 10
                ]
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=row['Undergraduate Major']
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title="Multi-Factor Comparison (0-10 scale)"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # Detailed comparison table
            display_cols = ['Undergraduate Major', 'Group', 'Starting Median Salary', 'Mid-Career Median Salary',
                          'Job_Satisfaction_Score', 'Work_Life_Balance', 'Job_Growth_Outlook', 'Personalized_Score']
            
            styled_df = comparison_df[display_cols].style.format({
                'Starting Median Salary': '${:,.0f}',
                'Mid-Career Median Salary': '${:,.0f}',
                'Job_Satisfaction_Score': '{:.1f}/10',
                'Work_Life_Balance': '{:.1f}/10',
                'Personalized_Score': '{:.1%}'
            })
            
            st.dataframe(styled_df, use_container_width=True)
    
    # Action Plan
    st.header("🎯 Your Action Plan")
    
    top_choice = top_recommendations.iloc[0]
    
    st.markdown(f"""
    <div class="recommendation-card">
        <h3>🏆 Top Recommendation: {top_choice['Undergraduate Major']}</h3>
        <p><strong>Why this matches you:</strong></p>
        <ul>
            <li>Aligns with your {selected_personality.lower()} personality type</li>
            <li>Matches your priority balance (Salary: {priorities['salary']:.0f}%, Growth: {priorities['growth']:.0f}%, Satisfaction: {priorities['satisfaction']:.0f}%)</li>
            <li>Strong career outlook: {top_choice['Job_Growth_Outlook']} growth potential</li>
            <li>Good work-life balance score: {top_choice['Work_Life_Balance']:.1f}/10</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="recommendation-card growth-recommendation">
            <h4>📈 Next Steps</h4>
            <ul>
                <li>Research {top_choice['Group']} programs at target schools</li>
                <li>Connect with professionals in {top_choice['Undergraduate Major']}</li>
                <li>Look for internships or job shadowing opportunities</li>
                <li>Consider related minors or double majors</li>
                <li>Build relevant skills early (see growth areas for {selected_personality} types)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="recommendation-card risk-recommendation">
            <h4>⚠️ Consider Also</h4>
            <ul>
                <li><strong>Backup Options:</strong> {', '.join(top_recommendations.iloc[1:4]['Undergraduate Major'].tolist())}</li>
                <li><strong>Skill Development:</strong> {', '.join(personality_types[selected_personality]['growth_areas'])}</li>
                <li><strong>Risk Level:</strong> {top_choice['Risk Level']} salary variability</li>
                <li><strong>Location Impact:</strong> Salaries vary significantly by region</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()