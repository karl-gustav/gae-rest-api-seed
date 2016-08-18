var rp = require('request-promise');
var cookie = rp.jar();

var data = {
    item: null,
    subItem: null,
    subSubItem: null
};

module.exports = rp.get({
    method: 'GET',
    uri: 'http://localhost:8080/_ah/login?email=test%40example.com&action=Login',
    jar: cookie
})
.then(log('Login OK'))
.then(function() {
    return rp({
        method: 'POST',
        uri: 'http://localhost:8080/rest/items',
        body: {
            text: 'text1'
        },
        jar: cookie,
        json: true
    })
    .then(storeInData('item'))
    .then(log('Create item OK'));
})
.then(function() {
    return rp({
        method: 'POST',
        uri: 'http://localhost:8080/rest/items/' + data.item.id + '/subitems',
        body: {
            text: 'text2'
        },
        jar: cookie,
        json: true
    })
    .then(storeInData('subItem'))
    .then(log('Create subItem OK'));
})
.then(function() {
    return rp({
        method: 'POST',
        uri: 'http://localhost:8080/rest/items/' + data.subItem.id + '/subitems/' + data.subItem.id + '/subsubitems',
        body: {
            text: 'text3'
        },
        jar: cookie,
        json: true
    })
    .then(storeInData('subSubItem'))
    .then(log('Create subSubItem OK'));
})
.then(function() {
    return rp({
        method: 'GET',
        uri: 'http://localhost:8080/rest/items/' + data.item.id + '/subitems/' + data.subItem.id + '/subsubitems/' + data.subSubItem.id,
        jar: cookie,
        json: true
    })
    .then(log('Get subSubItem OK'));
})
.then(function() {
    data.subSubItem.text = "superText"
    return rp({
        method: 'PUT',
        uri: 'http://localhost:8080/rest/items/' + data.item.id + '/subitems/' + data.subItem.id + '/subsubitems/' + data.subSubItem.id,
        body: data.subSubItem,
        jar: cookie,
        json: true
    })
    .then(function(subSubItem) {
        if (subSubItem.text !== "superText") {
            throw Error('Change not successful');
        }
    })
    .then(log('Update subSubItem OK'));
})
.then(function() {
    return rp({
        method: 'GET',
        uri: 'http://localhost:8080/rest/items/' + data.item.id + '/subitems/' + data.subItem.id + '/subsubitems',
        jar: cookie,
        json: true
    })
    .then(log('Get subSubItems OK'));
})
.then(function() {
    return rp({
        method: 'DELETE',
        uri: 'http://localhost:8080/rest/items/' + data.item.id + '/subitems/' + data.subItem.id + '/subsubitems/' + data.subSubItem.id,
        jar: cookie
    })
    .then(log('Delete subSubItem OK'));
})
.catch(function(err) {
    console.log('ERROR:', err.message)
});

function storeInData(key) {
    return function(value) {
        data[key] = value;
    }
}

function log(msg) {
    return function(data) {
        console.log(msg);
        return data;
    };
}

function moreThanOne(list) {
    if (list.length > 0) {
        return list;
    }
    throw Error('Zero items in list')

}