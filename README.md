# authorization-flask_react_Tailwind

## command
npx create-react-app frontend


# frontend
## replacement
Move the contents of 「for_frontend」 to 「frontend」.
Move 「index.html」 to 「frontend/public」.
and replace them.

## install
npm install react-router-dom
npm install tailwindcss
npm install url-loader --save-dev

## command
npx tailwindcss init
npx webpack
    yes


# backend
## install
pip install flask-cors

## command
flask db init

flask db migrate -m ""
flask db upgrade

