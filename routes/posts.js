const express = require('express')
const router = express.Router();
const Post = require('../models/Post')

// routes
router.get('/posts', (req, res) => {
    res.send("we are on posts")
})



module.exports = router;

