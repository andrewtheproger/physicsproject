const webpack = require('webpack');
const DuplicatePackageCheckerPlugin = require("duplicate-package-checker-webpack-plugin");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({ // <-- key to reducing React's size
        'process.env': {
          'NODE_ENV': JSON.stringify('production')
        }
      }),
      new DuplicatePackageCheckerPlugin(), //dedupe similar code
      new UglifyJsPlugin(), //minify everything
    ]
  }
};
