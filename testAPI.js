require('./tests/testItemAPI')
.then(function() {
    return require('./tests/testSubItemAPI');
})
.then(function() {
    return require('./tests/testSubSubItemAPI');
});

