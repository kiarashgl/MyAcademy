ssh ubuntu@myacademysut.ir
cd ~/MyAcademy
git pull --rebase origin master
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --no-input
python manage.py collectstatic
sudo systemctl gunicorn restart
