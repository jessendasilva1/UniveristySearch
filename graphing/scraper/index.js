// importing playwrite and fs module
const playwrite = require('playwright');
const fs = require('fs');
const { exit } = require('process');

// gets list of all course calendar urls (eg. https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/acct/)
async function get_subjects() {
    
    const browser = await playwrite.chromium.launch({
        headless: true
    });

    const page = await browser.newPage();           // creating new page
    await page.goto('https://calendar.uoguelph.ca/undergraduate-calendar/course-descriptions/');
    const list = await page.$eval('.az_sitemap', headerElm => {
       const data = [];
       const subject_names = new Object();
       const ul_lists = []
       const listElms = headerElm.getElementsByTagName('li');
      for (let key in listElms) {
          let element = {html: listElms[key].innerHTML, text: listElms[key].innerText}
          ul_lists.push(element);
      }
      // eliminate all unmatched list elements to get only the urls needed.
      ul_lists.forEach(elm => {
          const domain = "https://calendar.uoguelph.ca"
          if(elm && elm.html && elm.html.includes('<a href="/undergraduate-calendar/course-descriptions/')) {
              
              const subject_code = elm.text.match(/\((.*)\)/).pop();
              const subject_name = elm.text.substring(0, elm.text.indexOf('(')).trim();
              subject_names[subject_code] = subject_name;
              data.push({url: domain + elm.html.split(/"([^;]+)"/)[1], subject: subject_names});
          }
      })
       return data;
    });
    await browser.close();
    
    return list;
}

function getCourseArr(texts) {
    const search_terms = [
        'Prerequisite(s): ', 'Restriction(s): ', 'Equate(s): ', 
        'Offering(s): ', 'Department(s): ', 'Location(s): '
    ]
   
    // Iterate each course's fields and remove search_terms if they appear.
    // Add each semi-cleaned field to an array, tab delimit null entries
    let course_arr = [];
    texts.forEach(course => {
        
        let index = 0;
        course.forEach(field => {
            if (index < 2) {
                course_arr.push(field + '\t');
            }
            else {
                let temp = field;
                let isMatched = false;
                for(let i = 0; i < search_terms.length; i++) {
                    if (!isMatched && temp.includes(search_terms[i])) {
                        temp = temp.replace(search_terms[i], '');
                        course_arr.push(temp+'\t');
                        isMatched = true;
                        break;
                    }
                }
                if (!isMatched)
                {
                    course_arr.push('\t')
                }
            }
            index++;
        });
        course_arr.push('\n');
    })
    return course_arr;
}

async function eachCourse(url){
    
    const newBrowser = await playwrite.chromium.launch({
        headless: true,
        timeout: 60000
    });
    const page = await newBrowser.newPage();
    await page.goto(url);
    
    console.log('scraping: ', url)
    const no_indent_list = page.locator('.courseblock');
    const texts = await no_indent_list.evaluateAll(list => list.map(
        element => {
            if (element) {
                // Grab all div elements within a courseblock (incldues empty divs)
                const list = element.getElementsByTagName('div');
                data = [];
                for (let key in list) {
                    if (list[key].innerText != undefined)
                        data.push(list[key].innerText.trim());
                }
                return data;
            }
        })
    );
    
    

    // await page.waitForTimeout(5000);
    await newBrowser.close();
    return texts;
}

// recursive batch function which forces the async scrape to have a max of
// batchSize concurrent actions in the event queue.
function start_batch_scrape(subject_list, start, batchSize, numSubjects) {
    let result = false;
    if(start < subject_list.length) {
        result = true;
    }
    if (result)
    {
        let new_list = [];
        let i = 0;
        while(i < batchSize && start + i < numSubjects) {
            new_list.push(subject_list[start + i].url)
            i++;
        }
        start += i;
        let curIndex = 0
        new_list.forEach((url) => {
            eachCourse(url).then(course => {
                list = getCourseArr(course)
                
                fs.appendFileSync(fileName, list.join(''),
                        {encoding: 'utf-8'})
                curIndex++;
                if(curIndex == new_list.length) {
                    start_batch_scrape(subject_list, start, batchSize, numSubjects);
                }
            });
        })
        
    }
}

// main function for scrapping
async function main(){
    
    const batchSize = 1;
    const subject_list =  await get_subjects();
    
    const numSubjects = subject_list.length;
    let currIndex = 0;
    let cont = true;
    
    const subject_name_list = [];
    subject_list.forEach(elem => {
        subject_name_list.push(elem.subject);
    })
    
    fs.appendFileSync(subjectFileName, JSON.stringify(...subject_name_list),
                        {encoding: 'utf-8'})
    start_batch_scrape(subject_list, currIndex, batchSize, numSubjects);
}
if (process.argv[2] == undefined || process.argv[3] == undefined) {
    console.error("Missing Input File Argument");
    exit(1);
}

const fileName = process.argv[2];
const subjectFileName = process.argv[3];
main();

