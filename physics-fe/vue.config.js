const webpack = require("webpack");
const DuplicatePackageCheckerPlugin = require("duplicate-package-checker-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
// const CompressionPlugin = require("compression-webpack-plugin");

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        // <-- key to reducing React's size
        "process.env": {
          NODE_ENV: JSON.stringify("production")
        }
      }),
      new DuplicatePackageCheckerPlugin(), //dedupe similar code
      new UglifyJsPlugin() //minify everything
      // new CompressionPlugin({
      //   asset: "[path].gz[query]",
      //   algorithm: "gzip",
      //   test: /\.js$|\.css$|\.html$/,
      //   threshold: 10240,
      //   minRatio: 0.8
      // })
    ]
  }
};
