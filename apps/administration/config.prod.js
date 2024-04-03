const path = require('path');
const webpack = require('webpack');
const BabiliPlugin = require("babili-webpack-plugin");
const tinyPngWebpackPlugin = require('tinypng-webpack-plugin');

// Стандартные пути
const paths = {
    src: {
        self:      './resources/',
        js:        './resources/js',
        sass:      './resources/sass',
        images:    './resources/images'
    },
    assets: {
        self:      './static/administration',
        js:        './static/administration/js',
        css:       './static/administration/css',
        images:    './static/administration/images'
    },
}

module.exports = {
    entry: {
        main: [paths.src.js + '/index.js',]
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, paths.assets.js),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules|bower_components)/,
                loader: "babel-loader",
                options: {
                    cacheDirectory: true,
                    presets: ['es2017'],
                    plugins: [
                        require('babel-plugin-transform-object-rest-spread'),
                        'transform-runtime'
                    ]
                }
            },

            // Минификация картинок
            {
                test: /\.(gif|png|jpe?g)$/i,
                exclude: /(node_modules|bower_components)/,
                loaders: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '../images/[name].[ext]?[hash]',
                            publicPath: paths.assets.images
                        }
                    },
                    'image-webpack-loader'
                ]
            }
        ]
    },
    plugins: [
        // Минификация откомпилированного файла
        new BabiliPlugin(),

        // Глобальное подключение jquery
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
        }),

        new webpack.DllReferencePlugin({
            context: '.',
            manifest: require(paths.assets.js + '/vendor-manifest.json')
        }),

        // Минификация картинок
        new tinyPngWebpackPlugin({
            key: [
                'vdNQsRcaq1jqKKexKikVRpH2XZCR899o',
                'H5jueMufbG7zvACNHrMVO_Bsdx7asbkO',
                '-GTyp8jVYveO3A7EvOcjoHKfVT96QmVw',
                '_LM_GoX2k65ea8cyHjLr9CvMW8kHmW1O'
            ],
            relativePath: paths.assets.images,
            ext: ['jpeg', 'jpg', 'png']
        })
    ]
}
