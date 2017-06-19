ln -s /var/www/fx-calendar/config/supervisor.conf /etc/supervisor/conf.d/fx-calendar.conf

ln -s /var/www/fx-calendar/config/nginx.conf /etc/nginx/sites-enabled/fx-calendar

pip3 install -r requirements.txt