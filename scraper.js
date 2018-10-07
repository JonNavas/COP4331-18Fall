const cheerio = require('cheerio')
const request = require('request');

request({
    method: 'GET',
    url: 'http://catalog.ucf.edu/content.php?catoid=3&navoid=174&returnto=portfolio&in_portfolio=1'
}, (err, res, body) => {

    if (err) return console.error(err);

    let $ = cheerio.load(body);

    let courses = $('#courseprefix');

    let prefixes = courses.children();

    prefixes.each(function (i, e) {
        //console.log(e.attribs.value);
        
    });



});