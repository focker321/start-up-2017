var fs = require('fs');
var cheerio = require('cheerio');
var request = require('sync-request');
var async = require("async");

url_base = 'http://link.springer.com';

response = request('GET', url_base);

disciplines = []
subdisciplines = []

var $ = cheerio.load(response.getBody());
$('ol.disciplines > li').each(function(i, elem) {
    discipline = $(this);
    dis_url = discipline.find('a').attr('href');
    dis_name = discipline.text().trim();
    
    disciplines.push({name: dis_name, url: dis_url, parent: ''});
});

for(i = 0; i<disciplines.length; i++) {
    console.log(disciplines[i].name);
    request_discipline(url_base+disciplines[i].url, disciplines[i].name);
}

function request_discipline(url, parent) {
    response = request('GET', url);
    $ = cheerio.load(response.getBody());
    sub_dis = $('#sub-discipline-facet');
    all_sub_url = sub_dis.find('a.all').attr('href');
    request_subdiscipline(url_base+all_sub_url, parent)
}

function request_subdiscipline(url, parent) {
    response = request('GET', url);
    $ = cheerio.load(response.getBody());
    $('ol > li').each(function(i, elem) {
        subdiscipline = $(this);
        sub_name = subdiscipline.find('span.facet-title').text().trim();
        sub_url = subdiscipline.find('a.facet-link').attr('href');
        
        if (sub_name.length > 0) {
            console.log(sub_name);
            subdisciplines.push({name: sub_name, url: sub_url, parent: parent});
        }
    });
    
    next_url = $('a.next').attr('href')
    if (next_url) {
        console.log('.......... next >');
        request_subdiscipline(url_base+next_url, parent);
    }
}

categories = disciplines.concat(subdisciplines);
fs.writeFile('categories.json', JSON.stringify(categories, null, 4), function(err){
    console.log('Categories successfully written!');
    console.log(categories.length);
});