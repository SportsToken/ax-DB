const db = require("../models");
const Tutorial = db.tutorials;

// Retrieve all Tutorials from the database.
exports.findAll = (req, res) => {
    const title = req.query._id;
    var condition = title
      ? { title: { $regex: new RegExp(title), $options: "i" } }
      : {};

    Tutorial.find(condition)
      .then((data) => {
        res.send(data);
      })
      .catch((err) => {
        res.status(500).send({
          message:
            err.message || "Some error occurred while retrieving tutorials.",
        });
      });
};

