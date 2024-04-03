const path = require('path');
const webpack = require('webpack')
const BabiliPlugin = require("babili-webpack-plugin");

const paths = {
    src: {
        self:      __dirname + '/resources/',
        js:        __dirname + '/resources/js'
    },
    assets: {
        self:      __dirname + '/static/administration',
        js:        __dirname + '/static/administration/js'
    },
}

module.exports = {
    entry: {
        vendor: [paths.src.js + '/vendors.js']
    },
    output: {
        filename: '[name].bundle.js',
        path: paths.assets.js,
        library: '[name]_lib'
    },
    plugins: [
        new BabiliPlugin(),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Util: "exports-loader?Util!bootstrap/js/dist/util",
            Tab: "exports-loader?Tab!bootstrap/js/dist/tab",
            Modal: "exports-loader?Modal!bootstrap/js/dist/modal",
        }),
        new webpack.DllPlugin({
            path: paths.assets.js + '/[name]-manifest.json',
            name: '[name]_lib'
        })
    ]
}
