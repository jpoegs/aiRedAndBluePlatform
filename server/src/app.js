const express = require('express');
const app = express();

let games = {};

app.get('*', (req, res) => res.send('Hello, World!'));

app.listen(4040, () => console.log('Listening on port 4040!'));
