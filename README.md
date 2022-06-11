# Recei-Keep-Flask

A Python/Flask, PostgreSQL, React based Project that allows Users to upload pictures of, ideally, their receipts. Users will be able to set Tags on their uploaded receipts, for example, if the receipt was from a gas station, the user will be able to create a new tag for the specific gas station, or a wider topic covering tag like "Gas". Letting the user create new tags and tag their receipts allows for easy search/filtering/organization. Eventually the user will be able to make separate "Lists" of their receipts, to have even more organization.

Users will be able to upload any type of picture that they want, however, for this project specifically, Receipts would be the most ideal type of media that is uploaded.

I will most definitely be revisiting this idea in the future once I've gained professional work experience and with a much wider knowledge base.

Disclaimer The uploaded photos will NOT be used to retrieve personal information, or extract any type of information at all. This is purely a personal side project for me to learn more about Backend Development/DB's/Auth + have some functional project that I can use in the future possibly.

To use (Nobody should be able to use since they dont have the secret key for the app.config nor the passcode for the postgre db):
clone the repo and create two terminals

In the first terminal: <br>
cd backend <br>
python app.py <br>
(That should get the backend server up and running)

In second terminal: <br>
cd frontend2 <br>
npm start <br> 


<h1> Login Page </h1>
<img src="https://user-images.githubusercontent.com/91567133/173208454-ede1e889-d137-4175-9921-4ce6989342c2.png" width="400" height="350">




<h1> Registration Page </h1>
<img src="https://user-images.githubusercontent.com/91567133/173208409-96580396-8ade-44db-81e2-bb800cb309ff.png" width="400" height="350">

<br>

After that, the website should be pulled up in your home browser (I can't guarantee that everything will work properly.) <br>
TODO: <br
Create Search function <br>
Allow password resets <br>
Minor QA checking <br>
Unit tests for the backend <br>
