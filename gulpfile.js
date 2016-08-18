'use strict';

var gulp = require('gulp'),
	$ = require('gulp-load-plugins')(),
	del = require('del'),
	destDir = 'dist/',
	config = 'app.yaml';

gulp.task('default', ['build']);

gulp.task('build', ['clean-dist'], function(){
	return gulp.src(
		[
			'html/**/*.html',
			'html/images/*',
			'**/*.py',
			'app.yaml'

		],
		{base: './'})
		.pipe($.if(isIndexHtml, $.usemin({
			js: [$.ngAnnotate(), $.uglify(), $.rev()],
			jslib: [$.rev()],
			css: [$.minifyCss(), 'concat', $.rev()]
		})))
		.pipe(gulp.dest(destDir));
})

gulp.task('clean-dist', function () {
	return del(destDir);
});

function isIndexHtml (file) {
	return file.path.match('index\\.html$');
}
