// importing playwrite and fs module
const playwrite = require('playwright');
const fs = require('fs');
const { table } = require('console');
const { match } = require('assert');
const { parse } = require('path');
const path = require('path');


/* 
* Main URL for all the degree programs: https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/
* One of: 
*	https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/#programstext (list of all programs)
*	OR
* 	https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/#requirementstext (distribution requirements)
*/

// gets list of all degree urls (e.g https://calendar.uoguelph.ca/undergraduate-calendar/degree-programs/bachelor-applied-science-basc/)
async function getDegreeURLs() {

	const browser = await playwrite.chromium.launch({
        headless: true
    });
    
	const page = await browser.newPage();           // creating new page
    await page.goto('https://calendar.uoguelph.ca//undergraduate-calendar/degree-programs/');

	// goes to the above URL and grabs all the Degree programs URLs that Guelph offers
	// Finds the div with class-name ".sitemap" and returns a list of elements to "headerElm"
    const list = await page.$eval('.sitemap', headerElm => {
       const data = [];
       const ul_lists = []
	   // finds all the li elements that have the degree URLs
       const listElms = headerElm.getElementsByTagName('li');
      for (let key in listElms) {
          ul_lists.push(listElms[key].innerHTML);
      }
      // eliminate all unmatched list elements to get only the urls needed.
      ul_lists.forEach(elm => {
          const domain = "https://calendar.uoguelph.ca"
          if(elm && elm.includes('<a href="/undergraduate-calendar/degree-programs/')) {
              data.push(domain + elm.split(/"([^;]+)"/)[1])
          }
      })
       return data;
    });
	await browser.close();
    return list;
}

/* goes to each degree URL and gets each courses URL offered for that degree and returns and object
* for each degrees course
* i.e Bachelor of Applied Science (B.A.Sc.)
* @ returns
* {
        "name": "Bachelor of Applied Science (B.A.Sc.)",
        "links": [
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/applied-human-nutrition-ahn/",
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/child-studies-cstu/",
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/family-studies-human-development-fshd/",
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/applied-human-nutrition-ahn/",
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/child-studies-cstu/",
            "https://calendar.uoguelph.ca/undergraduate-calendar/programs-majors-minors/family-studies-human-development-fshd/"
        ]
    },
*/ 
async function getDegreeLinks(url){
	// returning promises to ensure each page is completed in order.
	return new Promise(async (resolve) => {
		const browser = await playwrite.chromium.launch({
			headless: true,
			timeout: 60000
		});

 		// creating new page
		const page = await browser.newPage();          
		await page.goto(url);
		try{
			const list = await page.$eval('.sitemap, #contentarea', headerElm => {
				var programs = {
					name: '',
					degreeCode: '',
					links: [] 
				};
				const ul_lists = [];
				// grabs all li and h1 elements in list
				const listElms = headerElm.getElementsByTagName('li');
				const title = headerElm.getElementsByTagName('h1');
				const regex = /\((.*?)\)/;
				var matchedStrings = regex.exec(title[0].innerText);	
				if(matchedStrings !== null){
					programs.degreeCode	= matchedStrings[1];
				}
				programs.name = title[0].innerText;
			   	for (let key in listElms) {
					ul_lists.push(listElms[key].innerHTML);
			   	}
				
			   	// eliminate all unmatched list elements to get only the urls needed.
				if(ul_lists.length && programs.name){
					ul_lists.forEach(function(elm){
						const domain = "https://calendar.uoguelph.ca"
						if(elm && elm.includes('<a href="/undergraduate-calendar/programs-majors-minors/')) {
							programs.links.push(domain + elm.split(/"([^;]+)"/)[1] + "#requirementstext");
						} 
					})
				}
				return programs;
			});
			// checks if a degree doesn't have any programs. i.e Bachelor of Arts and Sciences (B.A.S.)
			// and puts the website URL instead of each programs URL
			if(list.links.length == 0){
				list.links.push(url);
			}
			await browser.close();
			resolve(list);
		} catch(e){
			console.log(e);
			await browser.close();
		}
	})
}

async function createURLFile(degreeProgramsListFileOut){

	return new Promise(async (resolve, reject)=>{

		const masterList = [];
		const degreeList = await getDegreeURLs(); // get degree URLs

		// passes each of the 14 degree programs URL
		degreeList.forEach(url => {
			masterList.push(getDegreeLinks(url));      //
		});

		// once all 14 URLs have been parsed, write to the JSON file
		const file = fs.openSync(degreeProgramsListFileOut, 'w')
		fs.close(file, (err) => {
			if (err)
			console.error("Failed to close file,", err)
		});

		await Promise.all(masterList)
			.then((result) => {

				fs.appendFileSync(degreeProgramsListFileOut, JSON.stringify(result, null, 4), function (err) {
					if (err) throw err;
				});
			})
			.catch((e) => {
				console.log("error: " + e);
			});
		resolve(degreeProgramsListFileOut)
	});
}

// Get each degree major requirements
async function getDegreeMajorRequirements(url){

	// returning promises to ensure each page is completed in order.
	const browser = await playwrite.chromium.launch({
		headless: true
	});

	// creating new page
	const page = await browser.newPage();
	await page.goto(url);
	console.log('Scraping:', url)
	try{
		const newUrl = await page.$eval('.sitemap, #tabs', divElm => {
			const programs = {
				url: ''
			};

			// grabs all tab list in HTML doc
			const listElms = divElm.getElementsByTagName('ul');
			for (let key in listElms) {
				if(listElms[key].innerHTML && listElms[key].innerHTML.includes('<a href=')){
					programs.url = listElms[key].innerHTML.split('\n')[4].split(' ')[1].replace("href=","").replaceAll('"',"")
				}
			}
			return programs;
		});
		await browser.close();

		return newUrl;

	} catch(e){
		await browser.close();
	}
}

// read all degree urls from file called degreeProgramsList.json
async function readDegreeURL(degreeProgramsListFileOut){

	const file = await createURLFile(degreeProgramsListFileOut)      // create a file with all degree URLs

	return new Promise(((resolve, reject) => {           // readFile - all URL for degree programs
		fs.readFile(file, "utf8", (err, jsonString) => {
			if (err) {
				reject(err)
				return;
			}
			resolve(jsonString);
		});
	}))
}

async function getDegreeRequirementsLink(degreeProgramsListFileOut, fileName){

	const data = await readDegreeURL(degreeProgramsListFileOut)          // read ./degreeProgramsList.json file
	const jsonObj = JSON.parse(data)             // converting string object to JSON

	for(let i = 0; i < jsonObj.length;i++){
		for(let j = 0; j < jsonObj[i].links.length;j++){
			const url = jsonObj[i].links[j]
			const modify = await getDegreeMajorRequirements(url)
			// console.log(typeof modify)
			if(typeof modify === 'undefined'){
				delete jsonObj[i].links[j]
			}else{
				jsonObj[i].links[j] = url + modify.url
			}
		}
	}

	fs.writeFile(fileName, JSON.stringify(jsonObj,null,4), (error) => {
		if (error) throw error;
	});
}


// read all degree urls from file called degreeProgramsRequirementsLinks.json
async function readDegreeURLRequirements(degreeLinksFileOut){

	// const file = './scraper/degreeProgramsList.json'      // create a file with all degree URLs
	return new Promise(((resolve, reject) => {           // readFile - all URL for degree programs
		fs.readFile(degreeLinksFileOut, "utf8", (err, jsonString) => {
			if (err) {
				reject(err)
				return;
			}
			resolve(jsonString);
		});
	}))
}

// Goes to each degree course URL and grabs all the courses required for that major
async function getDegreeCourses(dCode, url, name){

	// returning promises to ensure each page is completed in order.
	return new Promise(async (resolve) => {
		const browser = await playwrite.chromium.launch({
			headless: true
		});

		// creating new page
		const page = await browser.newPage();
		if(typeof url === 'string'){
			await page.goto(url);
		}else{
			return [];
		}
		try{
			// add course name to the list
			const list = await page.$eval('#contentarea', headerElm => {
				var program = {
					degreeName: '',
					degreeCode: '',
					majorName: '',
					majorCode: '',
					requiredCourses: [],
					totalRequiredWeight: 0,
					totalElectiveWeight: 0,
					electives: [],
					//courses: []
				}
				const temp = headerElm.querySelectorAll('header, h2, table');
				for(i = 0; i < temp.length; i++){
					const masterDuplicateCheckArray = [];
					if(temp[i].innerHTML){
						if(temp[i].innerHTML.includes('<h1')){
							const field =  temp[i].innerText;
							let majorName = field.split('(', 2)[0].trim();
							let majorCode = /\(([^\)]+)\)/.exec(field)[1].trim();
							program.majorName = majorName;
							program.majorCode = majorCode;
						}
						// only look for a Major header and the table immediately after it.
						// add more coverage as we go. 
						const regexCourse = new RegExp(/(?:[A-Z]{3,4}\*[0-9]{4,4})$/g); 
						const regexWeight = new RegExp(/\d{1,1}\.?\d{1,2}/);
						const regexOrCourse = new RegExp(/^(or ([A-Z]{3,4}\*[0-9]{4,4}))/gm);
						// Parses the table underneath the header that includes the text "Major"
						if(temp[i].innerText.includes("Major") && temp[i + 1]){
							// gets the next table below the Major header element
							
							const majorTable = temp[i+1].innerText.split("\n");
							let electiveCheck = false;
							
							// splits each table row by \t delimeter
							for(j = 0; j < majorTable.length; j++){
								const eachRequirement = majorTable[j].split('\t');
								// checks of the table element rows are tab delimited
								if(eachRequirement.length > 1){
									// for each string gathered from the table row, i.e "SPAN*1100\tIntroductory Spanish I\t0.50",
									eachRequirement.forEach(string => {
										// checks if the string is just a course code, i.e CIS*3760
										if(regexCourse.test(string)){
											// if the string includes an "or", grab the previous course and put them both in a nested
											// list, indicating a choice
											if(string.includes('or')){
												let lastCourse = program.requiredCourses.pop();
												let tempArray = [];
												tempArray.push(lastCourse);
												let tempString = string.match(regexCourse);
												if(!masterDuplicateCheckArray.includes(tempString[0])){
													tempArray.push(tempString[0]);
													program.requiredCourses.push(tempArray);
													masterDuplicateCheckArray.push(tempString[0]);
												}
											} else {
												// masterDuplicateCheckArray just checks for duplicate course codes being added. No nice
												// way of checking nesting arrays with includes()
												if(!masterDuplicateCheckArray.includes(string)){
													program.requiredCourses.push(string);
													masterDuplicateCheckArray.push(string);
												}
											}
										}
										// checks for only a weight code, since it should always be 4 characters, and able to be 
										// converted to a float 
										else if(regexWeight.test(string) && !string.includes("electives") && string.length == 4){
											if(parseFloat(string)){
												if(electiveCheck){
													program.totalElectiveWeight += parseFloat(string);
													electiveCheck = false;
												} else {
													program.totalRequiredWeight += parseFloat(string);
												}
											} 
												
										}
										// checks if the current table row is an elective, adds it to the electiveWeight and electiveList instead
										// of the requiredWeight
										else if(string.includes("Area of Aplication") || string.includes("electives")){
											electiveCheck = true;
											program.electives.push(string);
										}
										else if(string.includes("credits from the following")){
											electiveCheck = true;
											program.electives.push(string);
										}
									})
								}
							}
							//program.courses = majorTable;
						}
					} else {
						// Course doesnt have a Major header
					}
				}
				return program;
			});
			list.degreeName = name; 
			list.degreeCode = dCode;
			await browser.close();
			resolve(list);
		} catch (e){
			console.log(e);
			await browser.close();
		}
	})
}
async function main(degreeProgramsListFileOut, degreeLinksFileOut, majorFileOut){

	await getDegreeRequirementsLink(degreeLinksFileOut, degreeProgramsListFileOut);
	
	const data = await readDegreeURLRequirements(degreeLinksFileOut)
	const jsonObj = JSON.parse(data)             // converting string object to JSON
	const result = []
	for(let i = 0; i < jsonObj.length;i++){
		for(let j = 0; j < jsonObj[i].links.length;j++){
			const url = jsonObj[i].links[j]
			const degreeCode = jsonObj[i].degreeCode;
			const name = jsonObj[i].name;
			if("Co-operative Education Programs" !== jsonObj[i].name){ // Removing Co-operative Education Programs
				const allCourses = await getDegreeCourses(degreeCode, url, name);
				result.push(allCourses);
				//result.push({'degreeName':jsonObj[i].name, 'courseName': allCourses.courseName, 'courses': allCourses.courses})
				console.log("done scraping " + jsonObj[i].links[j]);
			}

		}
	}

	// file = fs.openSync(majorFileOut, 'w')
	// fs.close(file, (err) => {
	// 	if (err)
	// 		console.error("Failed to close file,", err)
	// });
	//fs.writeFile('temp.json', JSON.stringify(result,null,4), (error) => {
	fs.writeFile(majorFileOut, JSON.stringify(result,null,4), (error) => {
		if (error) throw error;
	});
}

if (process.argv[2] == undefined || process.argv[3] == undefined || process.argv[4] == undefined) {
    console.error("Missing File Argument");
    exit(1);
}
else {
	main(process.argv[2], process.argv[3], process.argv[4])
}
