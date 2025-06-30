## Steps to Run

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv venv
source venv/bin/activate          # macOS/Linux
# or venv\Scripts\activate        # Windows

pip install -r requirements.txt
python manage.py runserver

cd frontend
npm install
npm start
