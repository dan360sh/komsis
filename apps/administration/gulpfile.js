// Общие модули
var path            = require('path');
var gulp            = require('gulp');
var notify          = require("gulp-notify");          // Обработчик ошибок
var sourcemaps      = require('gulp-sourcemaps');
var rename          = require('gulp-rename');          // Переименование файла
var concat          = require('gulp-concat');          // Конкатенация
var plumber         = require('gulp-plumber');         // Обработчик ошибок
var watch           = require('gulp-watch');           // Просмотр изменений

// Работа с SASS
var sass            = require('gulp-sass');            // Компилятор Sass
var autoprefixer    = require('gulp-autoprefixer');

// Работа с JS
var uglify          = require('gulp-uglify');          // Минификация JS файла

// Работа с SVG
var svgstore        = require('gulp-svgstore');        // Объединение SVG в спрайт
var svgmin          = require('gulp-svgmin');          // SVG минификация
var cheerio         = require('gulp-cheerio');         // Работа с атрибутами


// Пути к исходным файлам
var paths = {
    src: {
        self:      './resources',
        sass:      './resources/sass',
        svg:       './resources/svg'
    },
    assets: {
        self:      './static/administration',
        css:       './static/administration/css',
        images:    './static/administration/images'
    },
    node: 'node_modules/',
    html: './public/'
}


/* Sass компиляция
---------------------------------------*/
gulp.task('sass', function () {
    // Компиляция библиотек
    gulp
        .src([
            paths.node        +'bootstrap/scss/bootstrap.scss',
            paths.src.sass    +'/lib/*.+(scss|sass)',
        ])
        .pipe(plumber({
            errorHandler: notify.onError("<%= error.message %>")
        }))
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(autoprefixer('last 2 version'))
        .pipe(concat('vendor.css'))
        .pipe(gulp.dest(paths.assets.css));

    // Компиляция всего остального
    gulp
        .src([
                 paths.src.sass    +'/**/*.+(scss|sass)',
            '!'+ paths.src.sass    +'/lib/*.+(scss|sass)'
        ])
        .pipe(plumber({
            errorHandler: notify.onError("<%= error.message %>")
        }))
        .pipe(sourcemaps.init())
        // .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
        .pipe(autoprefixer('last 2 version'))
        .pipe(sourcemaps.write('./', { sourceRoot: '/source' }))
        .pipe(gulp.dest(paths.assets.css))
});


/* Объединение SVG файлов
---------------------------------------*/
gulp.task('svg', function () {
    gulp
        .src(paths.src.svg    +'/**/*.svg', { base: 'src/sprite' })
        .pipe(plumber({
            errorHandler: notify.onError("<%= error.message %>")
        }))
        .pipe(svgmin({
            js2svg: {
                pretty: true
            }
        }))
        .pipe(rename(function (path) {
            var name = path.dirname.split(path.sep);
            name.push(path.basename);
        }))
        .pipe(svgstore({ inlineSvg: true }))
        .pipe(cheerio({
            run: function ($) {
                $('svg').attr('style', 'display:none');
            },
            parserOptions: { xmlMode: true }
        }))
        .pipe(gulp.dest(paths.assets.images));
});

gulp.task('watch', function () {
    gulp.watch (paths.src.sass    + '/**/*.+(scss|sass)', ['sass']);
    gulp.watch (paths.src.svg     + '/**/*.svg', ['svg']);
});

gulp.task('default', ['sass', 'watch']);
