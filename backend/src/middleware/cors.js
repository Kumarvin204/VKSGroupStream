const cors = require('cors');
const config = require('../utils/config');

module.exports = () => {
  return cors({
    origin: (origin, callback) => {
      // Dynamically allow any origin making the request to prevent CORS errors on cloud deployments
      callback(null, true);
    },
    methods: ['GET', 'POST', 'DELETE'],
    credentials: true,
  });
};
