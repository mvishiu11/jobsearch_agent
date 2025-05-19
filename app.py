
from flask import Flask, render_template_string
import markdown

app = Flask(__name__)

# Markdown content
markdown_content = """
# Candidate Preferences
- **Position Level**: Mid+
- **Desired Salary**: 16k PLN or more
- **Location Preference**: Open to working in Warsaw or remotely
- **Tech Stack Comfort**: Python-oriented

---

# Job Opportunities
1. **[Senior Software Engineer with Python at CodiLime](https://jobs.codilime.com/jobs/5929709-senior-software-engineer-with-python)**
   - **Salary**: 20,500 - 27,500 PLN + VAT B2B
   - **Work Type**: Fully remote

2. **[Mid Python Developer at Proexe.pl](https://proexe-eu.breezy.hr/p/32b77e02e599)**
   - **Salary**: 16,000 - 22,000 PLN net B2B
   - **Work Type**: Remote or hybrid in Warsaw

3. **[Senior Python Developer at Luxoft](https://career.luxoft.com/jobs/senior-python-developer-14529)**
   - **Salary**: Not specified but likely competitive
   - **Work Type**: Remote

4. **[Mid/Senior Python (Django) Developer at Sunscrapers](https://sunscrapers.com/careers/job-offers/mid-senior-python-django-developer/)**
   - **Salary**: Details not listed
   - **Work Type**: Warsaw or remote

---

# Interview Preparation Resources
1. **[LiveCareer: Interview Preparation Guide and Resources](https://www.livecareer.com/resources/interviews)**
   - Description: Stressed about interviewing? We understand this part of the job-search process to be the most challenging, so you don't have to go it alone.

2. **[10 Resources to Help You Rock Your Job Interview - Idealist](https://www.idealist.org/en/careers/resources-to-help-rock-your-job-interview)**
   - Description: Landing an interview can be a huge relief. However, preparation is key to sealing the deal.

3. **[Job Interview Prep Guide: How to Prepare for an Interview | Glassdoor](https://www.glassdoor.com/blog/guide/the-ultimate-job-interview-preparation-guide/)**
   - Description: This guide shows you how to use Glassdoor as a resource for interview preparation with common questions.

4. **[30+ Best Tips on How to Prepare for a Job Interview | The Muse](https://www.themuse.com/advice/the-ultimate-interview-guide-30-prep-tips-for-job-interview-success)**
   - Description: Discover over 30 tips on how to prepare for a job interview, from salary questions to video interview backgrounds.

5. **[10 online resources that help you prep for the hardest interview questions](https://www.theladders.com/career-advice/10-online-resources-that-help-you-prep-for-the-hardest-interview-questions)**
   - Description: A collection of online resources to help you tackle the hardest interview questions.

---

# 14-Day Interview Preparation Plan
| Day | Focus                                   | Resource |
|-----|----------------------------------------|----------|
| 1   | Coding Drill (LeetCode Style)         | Python Coding Problems on LeetCode |
| 2   | Behavioral Prep                        | LiveCareer: Interview Preparation Guide and Resources |
| 3   | System Design Session                  | System Design Interview Strategies on Glassdoor |
| 4   | Company Research                       | Job Interview Prep Guide: Glassdoor |
| 5   | Coding Drill (LeetCode Style)         | Top 50 Python Problems on LeetCode |
| 6   | Behavioral Prep                        | 30+ Best Tips on How to Prepare for a Job Interview |
| 7   | System Design Session                  | How to Approach System Design Interviews |
| 8   | Company Research                       | CodiLime Company Overview and Projects |
| 9   | Coding Drill (LeetCode Style)         | Data Structures & Algorithms Practice on LeetCode |
| 10  | Behavioral Prep                        | 10 Resources to Help You Rock Your Job Interview |
| 11  | System Design Session                  | System Design Patterns Reference |
| 12  | Company Research                       | Proexe Company Review and Job Expectations |
| 13  | Coding Drill (LeetCode Style)         | Mock Interviews with Peers |
| 14  | Final Behavioral Prep                  | Idealist: 10 Resources to Help Rock Your Job Interview |

---
"""

@app.route('/')
def index():
    html_content = markdown.markdown(markdown_content, extensions=['tables'])
    return render_template_string('<html><body>{{ content|safe }}</body></html>', content=html_content)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
