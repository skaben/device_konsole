const path = require('path');

//const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: 'js/bundle.js'
  },
  module: {
    rules: [
      // images
      {
				test: /\.(png|gif|jpg|svg)$/,
				loader: 'file-loader',
				options: {
					outputPath: "images",
				},
      },
      // fonts 
      {
        test: /\.(eot|svg|ttf|woff|woff2)$/,
        use: [
          {
            loader: 'file-loader?name=./assets/fonts/[name].[ext]'
          },
        ]
      },
      // styles
      {
      test: /\.scss$/,
      loader: 'style-loader!css-loader!sass-loader'
      /*
      use: [
				MiniCssExtractPlugin.loader,
				{
					loader: 'css-loader',
        },
				{
          loader: 'sass-loader',
          options: {
						sourceMap: true,
					}
				}
      ]
      */
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      title: 'Konsole',
      template: './src/index.html',
    }),
    /*
		new MiniCssExtractPlugin({
			filename: 'css/style.css'
    }),
    */
  ],
  devServer: {
    contentBase: path.join(__dirname, 'src'),
    compress: true,
    port: 9000
  }
};
