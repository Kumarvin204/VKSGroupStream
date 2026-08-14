const cors = require('cors');
const config = require('../utils/config');

module.exports = () => {
  return cors({
    origin: config.CORS_ORIGIN,
    methods: ['GET', 'POST', 'DELETE'],
    credentials: true,
  });
};
