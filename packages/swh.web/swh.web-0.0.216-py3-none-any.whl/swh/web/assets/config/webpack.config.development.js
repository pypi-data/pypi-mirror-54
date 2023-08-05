/**
 * Copyright (C) 2018-2019  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */

// webpack configuration for compiling static assets in development mode

// import required node modules and webpack plugins
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const RobotstxtPlugin = require('robotstxt-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin').CleanWebpackPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const FixSwhSourceMapsPlugin = require('./webpack-plugins/fix-swh-source-maps-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const GenerateWebLabelsPlugin = require('./webpack-plugins/generate-weblabels-webpack-plugin');
const ProgressBarPlugin = require('progress-bar-webpack-plugin');

const loadedMathJaxJsFiles = require('./mathjax-js-files');

// are we running webpack-dev-server ?
const isDevServer = process.argv.find(v => v.includes('webpack-dev-server'));
// webpack-dev-server configuration
const devServerPort = 3000;
const devServerPublicPath = 'http://localhost:' + devServerPort + '/static/';
// set publicPath according if we are using webpack-dev-server to serve
// our assets or not
const publicPath = isDevServer ? devServerPublicPath : '/static/';

const nodeModules = path.resolve(__dirname, '../../../../node_modules/');

// collect all bundles we want to produce with webpack
var bundles = {};
const bundlesDir = path.join(__dirname, '../src/bundles');
fs.readdirSync(bundlesDir).forEach(file => {
  bundles[file] = ['bundles/' + file + '/index.js'];
});

// common loaders for css related assets (css, sass, less)
let cssLoaders = [
  MiniCssExtractPlugin.loader,
  {
    loader: 'cache-loader'
  },
  {
    loader: 'css-loader',
    options: {
      sourceMap: !isDevServer
    }
  },
  {
    loader: 'postcss-loader',
    options: {
      ident: 'postcss',
      sourceMap: !isDevServer,
      plugins: [
        // lint swh-web stylesheets
        require('stylelint')({
          'config': {
            'extends': 'stylelint-config-standard',
            'rules': {
              'indentation': 4,
              'font-family-no-missing-generic-family-keyword': null,
              'no-descending-specificity': null
            },
            'ignoreFiles': ['node_modules/**/*.css',
                            'swh/web/assets/src/thirdparty/**/*.css']
          }
        }),
        // automatically add vendor prefixes to css rules
        require('autoprefixer')(),
        require('postcss-normalize')(),
        require('postcss-reporter')({
          clearReportedMessages: true
        })
      ]
    }
  }
];

// webpack development configuration
module.exports = {
  // use caching to speedup incremental builds
  cache: true,
  // set mode to development
  mode: 'development',
  // use eval source maps when using webpack-dev-server for quick debugging,
  // otherwise generate source map files (more expensive)
  devtool: isDevServer ? 'eval' : 'source-map',
  // webpack-dev-server configuration
  devServer: {
    clientLogLevel: 'warning',
    port: devServerPort,
    publicPath: devServerPublicPath,
    // enable to serve static assets not managed by webpack
    contentBase: path.resolve('./swh/web/'),
    // we do not use hot reloading here (as a framework like React needs to be used in order to fully benefit from that feature)
    // and prefere to fully reload the frontend application in the browser instead
    hot: false,
    inline: true,
    historyApiFallback: true,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    compress: true,
    stats: 'errors-only',
    overlay: {
      warnings: true,
      errors: true
    }
  },
  // set entries to the bundles we want to produce
  entry: bundles,
  // assets output configuration
  output: {
    path: path.resolve('./swh/web/static/'),
    filename: 'js/[name].[chunkhash].js',
    chunkFilename: 'js/[name].[chunkhash].js',
    publicPath: publicPath,
    // each bundle will be compiled as a umd module with its own namespace
    // in order to easily use them in django templates
    library: ['swh', '[name]'],
    libraryTarget: 'umd'
  },
  // module resolving configuration
  resolve: {
    // alias pdfjs to its minified version
    alias: {
      'pdfjs-dist': 'pdfjs-dist/build/pdf.min.js'
    },
    // configure base paths for resolving modules with webpack
    modules: [
      'node_modules',
      path.resolve(__dirname, '../src')
    ]
  },
  stats: 'errors-warnings',
  // module import configuration
  module: {
    rules: [
      {
      // Preprocess all js files with eslint for consistent code style
      // and avoid bad js development practices.
        enforce: 'pre',
        test: /\.js$/,
        exclude: /node_modules/,
        use: [{
          loader: 'eslint-loader',
          options: {
            configFile: path.join(__dirname, '.eslintrc'),
            ignorePath: path.join(__dirname, '.eslintignore'),
            cache: true,
            emitWarning: true
          }
        }]
      },
      {
      // Use babel-loader in order to use es6 syntax in js files
      // but also advanced js features like async/await syntax.
      // All code get transpiled to es5 in order to be executed
      // in a large majority of browsers.
        test: /\.js$/,
        exclude: /node_modules/,
        use: [
          {
            loader: 'cache-loader'
          },
          {
            loader: 'babel-loader',
            options: {
              presets: [
                // use env babel presets to benefit from es6 syntax
                ['@babel/preset-env', {
                  // Do not transform es6 module syntax to another module type
                  // in order to benefit from dead code elimination (aka tree shaking)
                  // when running webpack in production mode
                  'loose': true,
                  'modules': false
                }]
              ],
              plugins: [
              // use babel transform-runtime plugin in order to use aync/await syntax
                ['@babel/plugin-transform-runtime', {
                  'regenerator': true
                }],
                // use other babel plugins to benefit from advanced js features (es2017)
                '@babel/plugin-syntax-dynamic-import'
              ],
              env: {
                test: {
                  plugins: ['istanbul']
                }
              }
            }
          }]
      },
      // expose jquery to the global context as $ and jQuery when importing it
      {
        test: require.resolve('jquery'),
        use: [{
          loader: 'expose-loader',
          options: 'jQuery'
        }, {
          loader: 'expose-loader',
          options: '$'
        }]
      },
      // expose highlightjs to the global context as hljs when importing it
      {
        test: require.resolve('highlight.js'),
        use: [{
          loader: 'expose-loader',
          options: 'hljs'
        }]
      },
      {
        test: require.resolve('js-cookie'),
        use: [{
          loader: 'expose-loader',
          options: 'Cookies'
        }]
      },
      // css import configuration:
      //  - first process it with postcss
      //  - then extract it to a dedicated file associated to each bundle
      {
        test: /\.css$/,
        use: cssLoaders
      },
      // sass import configuration:
      //  - generate css with sass-loader
      //  - process it with postcss
      //  - then extract it to a dedicated file associated to each bundle
      {
        test: /\.scss$/,
        use: cssLoaders.concat([
          {
            loader: 'sass-loader',
            options: {
              sourceMap: !isDevServer
            }
          }
        ])
      },
      // less import configuration:
      //  - generate css with less-loader
      //  - process it with postcss
      //  - then extract it to a dedicated file associated to each bundle
      {
        test: /\.less$/,
        use: cssLoaders.concat([
          {
            loader: 'less-loader',
            options: {
              sourceMap: !isDevServer
            }
          }
        ])
      },
      // web fonts import configuration
      {
        test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      }, {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      }, {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      }, {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      }, {
        test: /\.otf(\?v=\d+\.\d+\.\d+)?$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/'
          }
        }]
      }, {
        test: /\.png$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'img/thirdParty/'
          }
        }]
      }
    ],
    // tell webpack to not parse minified pdfjs file to speedup build process
    noParse: [path.resolve(nodeModules, 'pdfjs-dist/build/pdf.min.js')]
  },
  // webpack plugins
  plugins: [
    // cleanup previously generated assets
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: ['**/*', '!xml', '!xml/*', '!img', '!img/*',
                                     '!img/logos', '!img/logos/*', '!img/icons',
                                     '!img/icons/*']
    }),
    // needed in order to use django_webpack_loader
    new BundleTracker({
      filename: './swh/web/static/webpack-stats.json'
    }),
    // for generating the robots.txt file
    new RobotstxtPlugin({
      policy: [{
        userAgent: '*',
        disallow: '/api/'
      }]
    }),
    // for extracting all stylesheets in separate css files
    new MiniCssExtractPlugin({
      filename: 'css/[name].[chunkhash].css',
      chunkFilename: 'css/[name].[chunkhash].css'
    }),
    // fix generated asset sourcemaps to workaround a Firefox issue
    new FixSwhSourceMapsPlugin(),
    // define some global variables accessible from js code
    new webpack.DefinePlugin({
      __STATIC__: JSON.stringify(publicPath)
    }),
    // needed in order to use bootstrap 4.x
    new webpack.ProvidePlugin({
      Popper: ['popper.js', 'default'],
      Alert: 'exports-loader?Alert!bootstrap/js/dist/alert',
      Button: 'exports-loader?Button!bootstrap/js/dist/button',
      Carousel: 'exports-loader?Carousel!bootstrap/js/dist/carousel',
      Collapse: 'exports-loader?Collapse!bootstrap/js/dist/collapse',
      Dropdown: 'exports-loader?Dropdown!bootstrap/js/dist/dropdown',
      Modal: 'exports-loader?Modal!bootstrap/js/dist/modal',
      Popover: 'exports-loader?Popover!bootstrap/js/dist/popover',
      Scrollspy: 'exports-loader?Scrollspy!bootstrap/js/dist/scrollspy',
      Tab: 'exports-loader?Tab!bootstrap/js/dist/tab',
      Tooltip: 'exports-loader?Tooltip!bootstrap/js/dist/tooltip',
      Util: 'exports-loader?Util!bootstrap/js/dist/util'
    }),
    // needed in order to use pdf.js
    new webpack.IgnorePlugin(/^\.\/pdf.worker.js$/),
    new CopyWebpackPlugin([{
      from: path.resolve(nodeModules, 'pdfjs-dist/build/pdf.worker.min.js'),
      to: path.resolve(__dirname, '../../static/js/')
    }]),
    new GenerateWebLabelsPlugin({
      outputType: 'json',
      exclude: ['mini-css-extract-plugin',
                'bootstrap-loader'],
      srcReplace: {
        './node_modules/pdfjs-dist/build/pdf.min.js':
        './node_modules/pdfjs-dist/build/pdf.js',
        './node_modules/admin-lte/dist/js/adminlte.min.js':
        './node_modules/admin-lte/dist/js/adminlte.js'
      },
      licenseOverride: {
        './swh/web/assets/src/thirdparty/jquery.tabSlideOut/jquery.tabSlideOut.js': {
          'spdxLicenseExpression': 'GPL-3.0',
          'licenseFilePath': './swh/web/assets/src/thirdparty/jquery.tabSlideOut/LICENSE'
        }
      },
      additionalScripts: Object.assign(
        {
          'js/pdf.worker.min.js': [
            {
              'id': 'pdfjs-dist/build/pdf.worker.js',
              'path': './node_modules/pdfjs-dist/build/pdf.worker.js',
              'spdxLicenseExpression': 'Apache-2.0',
              'licenseFilePath': './node_modules/pdfjs-dist/LICENSE'

            }
          ],
          '/jsreverse/': [
            {
              'id': 'jsreverse',
              'path': '/jsreverse/',
              'spdxLicenseExpression': 'AGPL-3.0-or-later',
              'licenseFilePath': './LICENSE'
            }
          ]
        },
        loadedMathJaxJsFiles
      )
    }),
    new ProgressBarPlugin({
      format: chalk.cyan.bold('webpack build of swh-web assets') + ' [:bar] ' + chalk.green.bold(':percent') + ' (:elapsed seconds)',
      width: 50
    })
  ],
  // webpack optimizations
  optimization: {
    // ensure the vendors bundle gets emitted in a single chunk
    splitChunks: {
      cacheGroups: {
        vendors: {
          test: 'vendors',
          chunks: 'all',
          name: 'vendors',
          enforce: true
        }
      }
    }
  },
  // disable webpack warnings about bundle sizes
  performance: {
    hints: false
  }
};
