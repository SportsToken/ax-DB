const express = require('express');
const app = express();
const mongoose = require('mongoose')
require('dotenv/config');

const postsRoute = require('./routes/posts');

// routes
app.get('/', (req, res) => {
    res.send("we are home")
})

app.post("/posts", (req, res) => {
    res.send("we are on posts");
});


mongoose.connect(
    process.env.DB_CONNECTION,  
    {useNewUrlParser: true},
    () => console.log('connect to db')
);

app.listen(3000)