// importing playwrite and fs module
const playwrite = require("playwright");
const fs = require("fs");
const { rejects } = require("assert");
const { stringify } = require("querystring");

async function scrapeAllCourseURLs() {
	const browser = await playwrite.chromium.launch({
		headless: true,
	});

	const page = await browser.newPage(); // creating new page
	await page.goto("https://catalogue.uottawa.ca/en/courses/");

	// goes to the above URL and grabs all the Degree programs URLs that uOttawa offers
	// Finds the div with class-name ".az_sitemap" and returns a list of all ul elements that contain
	// the links to each page
	const list = await page.$eval(".az_sitemap", (headerElm) => {
		const data = [];
		const ul_lists = [];
		const subject_names = new Object();
		// finds all the li elements that have the degree URLs
		const listElms = headerElm.getElementsByTagName("li");
		for (let key in listElms) {
			let element = {html: listElms[key].innerHTML, text: listElms[key].innerText}
			ul_lists.push(element);
		}
		// eliminate all unmatched list elements to get only the urls needed.
		ul_lists.forEach((elm) => {
			const domain = "https://catalogue.uottawa.ca";
			if (elm && elm.html && elm.html.includes('<a href="/en/courses/')) {
				let match = elm.text.match(/\((.*?)\)/);
				const subject_code = match ? match.pop() : "";
				const subject_name = elm.text.substring(0, elm.text.indexOf('(')).trim();
				subject_names[subject_code] = subject_name;
				data.push({url: domain + elm.html.split(/"([^;]+)"/)[1], subject: subject_names});
			}
		});
		return data;
	});
	await browser.close();
	return list;
}

async function scrapEachCourseURL(url) {
	return new Promise(async (resolve, reject) => {
		const browser = await playwrite.chromium.launch({
			headless: true,
			timeout: 60000,
		});

		const page = await browser.newPage();
		
		if(url){
			await page.goto(url);
		} else {
			return [];
		}
		

		try {
			const list = await page.$eval(".sc_sccoursedescs", (headerElm) => {
				// matches uOttawa course code pattern
				//const regexCourseCode = new RegExp(/([0-9]{4,4})/);
				//const regexCourseNum = new RegExp(/^([A-Z]{3,3})/);
				const regexCourse = new RegExp(/(?:([A-Z]{3,3})\u00A0([0-9]{4,4}))/);
				const frenchCreditWeight = new RegExp(/\d{1,1}\ crédit(s?)/gm);
				const englishCreditWeight = new RegExp(/\d{1,1}\ unit(s?)/gm);

				const data = [];
				const listElms = headerElm.getElementsByClassName("courseblock");
				// iterate through each course block element and push all the inner html to its own array
				// E.G --> CPT 5100 Advanced Competencies in Financial Accounting (3 units)
				for (i = 0; i < listElms.length; i++) {
					var programs = {
						subject: "",
						subject_name: "",
						course_num: "",
						course_name: "",
						description: "",
						prereqs: [],
						courseComponent: "",
						credits: 0,
						is_offered_fall: false,
						is_offered_winter: false,
						is_offered_summer: false,
						lectures: 0,
						labs: 0,
						credits: 0,
						description: "",
						offering: [],
						unknown: "",
						prereqs: [],
						co_reqs: [],
						equates: [],
						restrictions: [],
						dept: [],
						location: [],
						University: 'University of Ottawa'
					};
					const courseInfo = listElms[i].querySelectorAll("p");
					for (j = 0; j < courseInfo.length; j++) {
						// checks if nested <p> element has the class="courseblocktitle"
						if (courseInfo[j] && courseInfo[j].classList.contains("courseblocktitle")) {
							// grab the course code from the <p> element
							if (regexCourse.test(courseInfo[j].innerText)) {
								programs.subject = courseInfo[j].textContent;
								let tempCode = courseInfo[j].textContent.match(regexCourse);
								let tempString = tempCode[0].split("\u00A0");
								programs.subject = tempString[0];
								programs.course_num = tempString[1];
							}

							// grab the course code credit for english
							if (englishCreditWeight.test(courseInfo[j].textContent)) {
								let tempCredit = courseInfo[j].textContent.match(englishCreditWeight);
								if (tempCredit) {
									let tempStringCredit = tempCredit[0].split(" ");

									if (parseInt(tempStringCredit[0])) {
										programs.credits = parseInt(tempStringCredit[0]);
									} else {
										programs.credits = courseInfo[j].textContent;
									}
								}
								let tempCourseName = courseInfo[j].textContent.split(/\(\d{1,1}\ unit(s?)\)/gm);
								let tempString = tempCourseName[0].split(regexCourse);
								programs.course_name = tempString[3].trim();
							}
							// grab course credit weight for french
							else if (frenchCreditWeight.test(courseInfo[j].textContent)) {
								let tempCredit = courseInfo[j].textContent.match(frenchCreditWeight);
								if (tempCredit) {
									let tempStringCredit = tempCredit[0].split(" ");

									if (parseInt(tempStringCredit[0])) {
										programs.credits = parseInt(tempStringCredit[0]);
									} else {
										programs.credits = courseInfo[j].textContent;
									}
								}
								let tempCourseName = courseInfo[j].textContent.split(/\(\d{1,1}\ crédit(s?)\)/gm);
								let tempString = tempCourseName[0].split(regexCourse);
								programs.course_name = tempString[3].trim();
							}
						} else if (courseInfo[j] && courseInfo[j].classList.contains("courseblockdesc")) {
							programs.description = courseInfo[j].textContent.trim();
						} else if (courseInfo[j] && courseInfo[j].classList.contains("courseblockextra")) {
							if (courseInfo[j].textContent.includes("Course Component:") || courseInfo[j].textContent.includes("Volet :")) {
								let tempComponent = courseInfo[j].textContent.split(":");
								programs.courseComponent = tempComponent[1].trim();
							} else if (courseInfo[j].textContent.includes("Prerequisites:") || courseInfo[j].textContent.includes("Prerequisite:") || courseInfo[j].textContent.includes("Préalables :") || courseInfo[j].textContent.includes("Préalable:") || courseInfo[j].textContent.includes("Préalable :")) {
								programs.prereqs.push(courseInfo[j].textContent);
							}
						}
					}
					data.push(programs);
				}
				return data;
			});
			await browser.close();
			resolve(list);
		} catch (e) {
			resolve();
			console.log("No element with class .sc_sccoursedescs found.\n" + e);
			await browser.close();
		}
	});
}

async function main(fileOut) {
	// get all of uOttawa courses urls
	const courseURLs = await scrapeAllCourseURLs();
	const allCourses = [];
	const subject_name_list = [];

     courseURLs.forEach(elem => {
        subject_name_list.push(elem.subject);
    });
	
	const subjectJSON = JSON.parse(JSON.stringify(...subject_name_list));

	

	// const fileOut = 'degreeProgramCoursesOttawa.json';
	file = fs.openSync(fileOut, 'w')
	fs.close(file, (err) => {
		if (err)
			console.error("Failed to close file,", err)
	});

	for(let i = 0; i < courseURLs.length; i++){
		const eachCourse = await scrapEachCourseURL(courseURLs[i].url);
		if(eachCourse){
			for(j = 0; j < eachCourse.length; j++){
				eachCourse[j].subject_name = subjectJSON[eachCourse[j].subject];
				allCourses.push(eachCourse[j]);
			}
			console.log("done scraping " + courseURLs[i].url);
		}
	}

	// for(let i = 0; i < allCourses.length; i++) {
	// 	allCourses[i]["subject_name"] = ;
	// }
	
	fs.appendFileSync(fileOut, JSON.stringify(allCourses,null,4), {encoding: 'utf-8'}, (error) => {
		if (error) throw error;
	});
	
}

if (process.argv[2] == undefined) {
    console.error("Missing Input File Argument");
    exit(1);
}
else {
	main(process.argv[2])
}

