const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  const target = process.env.API_PROXY_TARGET;
  if (target) {
    app.use(createProxyMiddleware(['/api', '/vc/api'], { target, changeOrigin: true }));
  }
};
