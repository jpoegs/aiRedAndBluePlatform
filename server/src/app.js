const express = require('express');
const app = express();

const Manager = require('./manager');

let manager = new Manager();

app.use(function (req,res,next) {
  console.log('/' + req.method + ' ' + req.url);
  next();
});

app.route('/game/:gameId/')
  // Starting a game
  .post(function (req, res) {
    gameId = req.params.gameId;
    if (!manager.getGame(gameId)) {
      manager.makeGame(gameId, req.query.seed);
      res.sendStatus(201);
    } else res.sendStatus(409);
  })
  // Observing a game
  .get(function (req, res) {
    gameId = req.params.gameId;
    game = manager.getGame(gameId);
    if (game) {
      res.status(201).send(game.state);
    } else res.sendStatus(404);
  })
  // Removing a game
  .delete(function (req, res) {
    // TODO: Check if game is in progress
    game = manager.removeGame(req.params.gameId);
    if (game)
      res.status(200).send(game.state);
    else res.sendStatus(404);
  });

app.listen(4040, () => console.log('Listening on port 4040!'));
