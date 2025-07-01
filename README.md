## Steps to Run

```bash
git clone https://github.com/RahulAnkola/Sustainability-API
cd Sustainability-API

python -m venv venv
source venv/bin/activate          # macOS/Linux
# or venv\Scripts\activate        # Windows

pip install -r requirements.txt
python manage.py runserver

cd frontend
npm install
npm start
