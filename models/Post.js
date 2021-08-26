const mongoose = require('mongoose')

const PostSchema = mongoose.Schema({
    _id: String,
    _name: String,
    _hist: Array
})

module.exports = mongoose.model('Posts', PostSchema)