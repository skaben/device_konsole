const path = require('path');

module.exports = {
  entry: './src/index.js',
  mode: 'development',
  output: {
    path: path.resolve(__dirname),
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: path.join(__dirname, 'src'),
    compress: true,
    port: 9000
  }
};
