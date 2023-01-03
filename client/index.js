const express = require('express');

const app = express();
const directory = '/dist';
app.use(express.static(__dirname + directory));

const port = process.env.PORT || 4000;
app.listen(port, function () {
    console.log('Listening on', port);
});