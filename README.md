# How to Use

## 1. Clone the repository
```bash
git clone https://github.com/Milan-TJ/QRGenerator.git
cd QRGenerator
```

## 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
# Activate it:
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txtpip install -r requirements.txt
```
(If there’s no requirements.txt, install manually:)
```bash
pip install django qrcode pillow
```

## 4. Run database migrations
```bash
python manage.py migrate
```

## 5. Start the development server
```bash
python manage.py runserver
```

