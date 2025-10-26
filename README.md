# Proyecto_msih

1. clona este repositorio coloca : git clone https://github.com/Jhoel-zcq/Proyecto_msih.git

2. como el proyecto esta en la carpeta mish, muevete a ella con: cd mish 

3. crea el entorno virtual con: python -m venv venv     (si no, funciona con python, haslo cn python.exe, pues ese es el interprete que uso)

4. activa el entorno virtual con: .\venv\Scripts\activate
o si eres de mac y/o linux con: source venv/bin/activate

5. intala los requirements con: pip install -r requirements.txt

6. crea la base de datos local : python manage.py migrate

7. puedes crear tu superusuario con: python manage.py createsuperuser

8. corre el server : python manage.py runserver (si no, funciona con python, haslo cn python.exe, pues ese es el interprete que uso)