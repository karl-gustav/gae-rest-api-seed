"use strict"

'use strict';

var gulp = require('gulp'),
	$ = require('gulp-load-plugins')(),
	sourceDir = './',
	destDir = 'dist/',
	config = 'app.yaml';

gulp.task('default', ['build']);

gulp.task('build', function (cb) {
	$.runSequence('clean-dist', [
		'use-min'
	],
	cb)
});

gulp.task('use-min', function(){
	return gulp.src(
		[
				sourceDir + 'html/**/*.html',
				sourceDir + 'html/images/*',
				sourceDir + '**/*.py',
				sourceDir + 'appengine_config.py',
				sourceDir + 'app.yaml',
				sourceDir + 'main.py'

		],
		{base: sourceDir})
		.pipe($.if(isIndexHtml, $.usemin({
			js: [$.ngAnnotate(), $.uglify(), $.rev()],
			jslib: [$.rev()],
			css: [$.minifyCss(), 'concat', $.rev()]
		})))
		.pipe(gulp.dest(destDir));
})

gulp.task('clean-dist', function () {
	return gulp.src(destDir, {read: false})
		.pipe($.clean({force: true}));
});

function isIndexHtml (file) {
	return file.path.match('index\\.html$');
}
