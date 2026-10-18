from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)

def normalize_name(name):
    # The two files spell the same college with different spaces and punctuation
    return re.sub(r'[^a-z0-9]', '', str(name).lower())

df_newcolleges = pd.read_csv('newcolleges2.csv')
# Collapse stray line breaks and double spaces so each college appears once in the dropdown
df_newcolleges['College Name'] = df_newcolleges['College Name'].str.split().str.join(' ')
# Same program is written in different cases (e.g. "Computer Engineering" and "COMPUTER ENGINEERING")
df_newcolleges['Program Name'] = df_newcolleges['Program Name'].str.split().str.join(' ').str.upper()

df_ncdata = pd.read_csv('ncdata.csv')
df_ncdata['name_key'] = df_ncdata['Name of Institute'].apply(normalize_name)

# Category shown in the dropdown -> closing rank column in newcolleges2.csv
CATEGORY_COLUMNS = {
    'OPEN': 'Open Rank',
    'SC': 'SC Rank',
    'ST': 'ST Rank',
    'SEBC': 'SEBC Rank',
    'EWS': 'EWS Rank',
    'TFWS': 'TFWS Rank',
}

# Chance thresholds, as a ratio of closing rank to the student's rank
SAFE_RATIO = 1.2    # closing rank at least 20% beyond your rank
REACH_RATIO = 0.9   # closing rank up to 10% better than your rank is still worth a try

def get_college_names():
    if 'College Name' in df_newcolleges.columns:
        college_names = sorted(df_newcolleges['College Name'].unique().tolist())
    else:
        college_names = []
    return college_names

def get_program_names():
    if 'Program Name' in df_newcolleges.columns:
        program_names = sorted(df_newcolleges['Program Name'].unique().tolist())
    else:
        program_names = []
    return program_names

def save_feedback(name, email, organization, message):
    with open('feedback.txt', 'a') as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Organization: {organization}\n")
        file.write(f"Message: {message}\n\n")

    return "Feedback saved successfully!"

@app.route('/')
def home():
    college_names = get_college_names()
    program_names = get_program_names()
    return render_template('index.html', college_names=college_names, program_names=program_names)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    method = request.form.get('method', '')
    if method == 'college_pref':
        user_college = request.form.get('college', '')
        recommended_colleges = recommend_by_college(user_college)
    elif method == 'rank_program':
        user_rank = request.form.get('rank', '').strip()
        user_program = request.form.get('program', '')
        user_category = request.form.get('category', 'OPEN')
        if not user_rank.isdigit() or int(user_rank) == 0:
            recommended_colleges = "Please enter a valid rank."
        elif user_category not in CATEGORY_COLUMNS:
            recommended_colleges = "Please select a valid category."
        else:
            user_rank = int(user_rank)
            recommended_colleges = recommend_by_rank_program(user_rank, user_program, user_category)
    else:
        recommended_colleges = "Invalid method selected."
    
    return recommended_colleges

def recommend_by_college(user_college):
    user_college = ' '.join(user_college.split()).lower()
    if 'College Name' in df_newcolleges.columns:
        filtered_colleges = df_newcolleges[df_newcolleges['College Name'].str.lower() == user_college]
    else:
        filtered_colleges = pd.DataFrame(columns=df_newcolleges.columns)
    html_table = filtered_colleges.to_html(index=False, classes="college-table")
    return html_table

def get_chance(closing_rank, user_rank):
    # Lower rank is better, so a closing rank well beyond yours means a safer seat
    if closing_rank >= user_rank * SAFE_RATIO:
        return 'Safe'
    elif closing_rank >= user_rank:
        return 'Moderate'
    return 'Reach'

def recommend_by_rank_program(user_rank, user_program, user_category):
    rank_column = CATEGORY_COLUMNS[user_category]
    user_program = ' '.join(user_program.split()).lower()

    # '******' (no seat in this quota) becomes NaN and is dropped
    closing_ranks = pd.to_numeric(df_newcolleges[rank_column], errors='coerce')
    mask = (df_newcolleges['Program Name'].str.lower() == user_program) & (closing_ranks >= user_rank * REACH_RATIO)

    results = df_newcolleges.loc[mask, ['College Name', 'Program Name']].copy()
    results['Closing Rank'] = closing_ranks[mask].astype(int)
    results['Chance'] = results['Closing Rank'].apply(lambda r: get_chance(r, user_rank))
    # Most competitive college you can aim for comes first
    results = results.sort_values('Closing Rank')

    return render_template('results_table.html', results=results.to_dict('records'),
                           category=user_category, user_rank=user_rank)

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    organization = request.form['organization']
    message = request.form['message']

    response = save_feedback(name, email, organization, message)
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/college_info/<college_name>')
def college_info(college_name):
    college_data = df_ncdata[df_ncdata['name_key'] == normalize_name(college_name)]
    if college_data.empty:
        return render_template('college_info.html', college_info=[], college_name=college_name)
    else:
        # Get college information in vertical format
        college_info = []
        for index, row in college_data.iterrows():
            college_info.append({
                'field': 'Name of Institute',
                'value': row['Name of Institute']
            })
            college_info.append({
                'field': 'Address',
                'value': row['Address']
            })
            college_info.append({
                'field': 'Contact No',
                'value': row['contact no']
            })
            college_info.append({
                'field': 'Email ID',
                'value': row['email id']
            })
            college_info.append({
                'field': 'Website',
                'value': row['website']
            })
            college_info.append({
                'field': 'District',
                'value': row['district']
            })
            college_info.append({
                'field': 'Hostel',
                'value': row['hostel']
            })
            college_info.append({
                'field': 'Mess',
                'value': row['mess']
            })
            college_info.append({
                'field': 'Transportation',
                'value': row['transportaion']
            })
            college_info.append({
                'field': 'Tuition Fees (Boys)',
                'value': row['tution fees (boys)']
            })
            college_info.append({
                'field': 'Tuition Fees (Girls)',
                'value': row['tution fees (girls)']
            })

        return render_template('college_info.html', college_info=college_info)

if __name__ == '__main__':
    app.run(debug=True)
