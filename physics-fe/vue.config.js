const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin

module.exports = {
  productionSourceMap: false,

  configureWebpack: {
    mode: 'production',
    plugins: [
      // new BundleAnalyzerPlugin(),
    ],
    optimization: {
      minimize: true,
      namedModules: true,
      namedChunks: true,
      moduleIds: 'named',
      chunkIds: 'named',
      splitChunks: {
        minSize: 10000,
        maxSize: 200000,
      },
    }
  },
};
