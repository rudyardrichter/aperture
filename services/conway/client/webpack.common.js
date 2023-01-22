const CopyPlugin = require("copy-webpack-plugin");
//const WasmPackPlugin = require("@wasm-tool/wasm-pack-plugin");
const path = require('path');

/*
    module.exports = {
        entry: "./bootstrap.js",
        output: {
            path: path.resolve(__dirname, "dist"),
            filename: "bootstrap.js",
        },
        mode: "development",
        plugins: [
            new CopyWebpackPlugin(['index.html'])
        ],
    };
*/

module.exports = {
    entry: './src/index.ts',
    experiments: {
        asyncWebAssembly: true,
    },
    // add rules to get the index.ts file to be able to import .wasm module
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    plugins: [
        new CopyPlugin({
            patterns: ['public/index.html'],
        }),
        //new WasmPackPlugin({
        //    crateDirectory: path.resolve(__dirname, "../wasm"),
        //})
    ],
    resolve: {
        extensions: ['.tsx', '.ts', '.js', '.wasm'],
        modules: ['node_modules'],
    },
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
    },
};
