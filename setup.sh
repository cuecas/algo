echo "Creating virtual environment..."
python3 -m venv virtualenv

echo "Entering on environment..."
source virtualenv/bin/activate

echo "Installing dependencies..."
pip3 install -r requirements.txt
