const Game = require('./game')

class Manager {
  constructor() {
    this.games = {};
  }

  makeGame(id, seed) {
    this.games[id] = new Game(id, seed);
  }

  getGame(id) {
    return this.games[id];
  }

  removeGame(id) {
    let game = this.games[id];
    if (game) {
      delete this.games[id];
      return game.state;
    } else return undefined;
  }

}

module.exports = Manager;
