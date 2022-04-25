const { test, expect, request } = require('@playwright/test');

test.describe('Multiple Tests', () => {
	let page;
	test.beforeAll(async ({ browser }) => {
		const context = await browser.newContext();
		page = await context.newPage();
		await page.goto('https://131.104.49.113/');

	});
	
	test.afterAll(async ({ browser }, testInfo) => {
		console.log(`Finished ${testInfo.title} with status ${testInfo.status}`);
		
		if (testInfo.status !== testInfo.expectedStatus)
			console.log(`Did not run as expected, ended up at ${browser.url()}`);
	});

	test('#1, Test URL https://131.104.49.113/ works', async ({ page }) => {
		await page.goto('https://131.104.49.113/', {
			timeout: 10000
		});
	});

	test('#2, Testing if the Graph Button exists', async ({ page }) => {
		await page.goto('https://131.104.49.113/');
		const title = page.locator('#searchCoursesButton');
		await expect(title, "Should contain the text [Search Courses]").toContainText('Search Courses');
	});

	test('#3, Testing if the Search Button exists', async ({ page }) => {
		await page.goto('https://131.104.49.113/');
		const title = page.locator('#graphCoursesButton');
		await expect(title, "Should contain the text [Graph Courses]").toContainText('Graph Courses');
	});

	test('#4, Testing getting CIS*2750 with API request to /api/courses/', async ({ request }) => {
		const subjectsResponse = await request.get(`https://131.104.49.113/api/courses?is_ottawa=false&is_guelph=true&subject=CIS&course_num=2750`);
		expect(subjectsResponse.ok()).toBeTruthy();
		expect(await subjectsResponse.json(), "Should return course [CIS*2750]").toContainEqual(expect.objectContaining({
			subject: "CIS",
			course_num: 2750,
			course_name:  "Software Systems Development and Integration"
		}));
	});

	test('#5, Testing getting Univeristy of Guelph subjects through API request to /api/subjects/', async ({ request }) => {
		const subjectsResponse = await request.get(`https://131.104.49.113/api/subjects?is_ottawa=false&is_guelph=true&is_major=false`);
		expect(subjectsResponse.ok()).toBeTruthy();
		let subjectsArray = await subjectsResponse.json();
		subjectsArray.forEach((item) => {
			expect(item).toHaveProperty('is_guelph', true);
			expect(item).toHaveProperty('is_ottawa', false);
		});
	});

	test('#6, Testing getting Univeristy of Ottawa subjects through API request to /api/subjects/', async ({ request }) => {
		const subjectsResponse = await request.get(`https://131.104.49.113/api/subjects?is_ottawa=true&is_guelph=false&is_major=false`);
		expect(subjectsResponse.ok()).toBeTruthy();
		let subjectsArray = await subjectsResponse.json();
		subjectsArray.forEach((item) => {
			expect(item).toHaveProperty('is_guelph', false);
			expect(item).toHaveProperty('is_ottawa', true);
		});
	});

	test('#7, Searching for CIS*2750 through the UI', async ({ page }) => {
		await page.goto('https://131.104.49.113/');
		await page.locator('text=Select School:').click();
		await page.locator('[value=is_guelph]').click();
		await page.locator('text=Select Subject:').click();
		await page.locator('[value=CIS]').click();
		await page.fill('[name=course_num]', '2750');
		await page.locator('[name=searchSubmit]').click();
		let resultsName = await page.locator('td').first();
		await expect(resultsName, "Should display CIS*2750").toContainText("CIS*2750");
	});

	test('#8, Testing that all inputs associated with Searching courses are hidden when Graph Button is clicked', async ({ page }) => {
		await page.goto('https://131.104.49.113/');
		await page.click("button#graphCoursesButton");
		const inputs = await page.locator('.inputs .radioDivs');	
		const count = await inputs.count();
		for (let i = 0; i < count; ++i){
			expect(await inputs.nth(i).isHidden()).toBeTruthy();
		}
	});

	test('#9, Testing that all inputs associated with Searching courses are visible when Search Button is clicked', async ({ page }) => {
		await page.goto('https://131.104.49.113/');
		await page.click("button#searchCoursesButton");
		const inputs = await page.locator('.inputs .radioDivs');	
		const count = await inputs.count();
		for (let i = 0; i < count; ++i){
			expect(await inputs.nth(i).isVisible()).toBeTruthy();
		}
	});

	test('#10, Testing that /api/graph/ returns only a specific schools subject graph', async ({ request }) => {
		const graphResponse = await request.get(`https://131.104.49.113/api/courses/graph?is_ottawa=false&is_guelph=true&subject=cis`);
		expect(graphResponse.ok()).toBeTruthy();
		let subjectgraphArray = await graphResponse.json();
		subjectgraphArray.forEach((item) => {
			expect(item).toHaveProperty('is_guelph', true);
			expect(item).toHaveProperty('is_ottawa', false);
		});
	})
})





