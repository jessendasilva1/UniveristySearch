import SearchOutput from "./searchOutput.js"

class SearchFields extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			params: {
				is_ottawa: false,
				is_guelph: false
			},
			data: [],
			schoolSubjects: ['Select a school first'],
			selectedSubject: '',
			whichSchool: '',
			inputsHidden: false,
		};
		
		this.submitSearch = this.submitSearch.bind(this);
		this.handleInputChange = this.handleInputChange.bind(this);
		this.changeSearch = this.changeSearch.bind(this);
		this.handleSchoolSelection = this.handleSchoolSelection.bind(this);
		this.handleSubjectSelection = this.handleSubjectSelection.bind(this);
	}

	
	handleSubjectSelection(event){
		const value = event.target.value;
		const subjectName = event.target.innerText;
		if(event.target.innerText !== 'Select a school first'){}	
		this.setState(prevState => {
			let params = Object.assign({}, prevState.params);  // creating copy of state variable jasper
			params.subject = value;                     // update the name property, assign a new value                 
			return { selectedSubject: subjectName, params };    // return new object jasper object
		})	
	}

	handleInputChange(event){
		const target = event.target;
		const name = target.name;	
		const value = target.type === 'checkbox' ? !this.state.params[name] : target.value;
		
		this.setState(prevState => {
			let params = Object.assign({}, prevState.params);  // creating copy of state variable jasper
			params[name] = value;                     // update the name property, assign a new value                 
			return { params };                                 // return new object jasper object
		})
	}
	
	submitSearch(event){
		event.preventDefault();		
		const name = event.target.name;
		if(name === 'searchSubmit'){
			if(!this.state.params.is_guelph && !this.state.params.is_ottawa){
				alert("Please select a school to search courses from.");
			} else {
				this.getCourses();
			}
		} 
		else if(name === 'graphSubmit'){
			if(!this.state.params.is_guelph && !this.state.params.is_ottawa){
				alert('Please select a school name and subject to graph');
			} 
			else if(!this.state.selectedSubject){
				alert("Please select a subject to graph.");
			}
			else {
				//console.log("Graphing " + this.state.whichSchool + " " + this.state.selectedSubject + " courses.");
				this.getGraph();
			}
		}
	}

	getGraph(){
		let apiParams = {
			is_ottawa: this.state.params.is_ottawa,
			is_guelph: this.state.params.is_guelph,
			subject: this.state.selectedSubject.substring(this.state.selectedSubject.indexOf("(")+1, this.state.selectedSubject.indexOf(")")),
		};

		//console.log(JSON.stringify(apiParams, null, 2));

		//Temporarily here
		//let data = [{'is_guelph': true, 'is_ottawa': false, 'src': {'name': 'STAT*2040', 'type_id': 0}, 'dest': {'name': 'CIS*4020', 'type_id': 0}, 'link': {'link_type': true, 'label': null}}];
		//renderGraph(data);

		$.ajax({
            type: 'GET',
            url: 'https://131.104.49.113/api/courses/graph',
            data: apiParams,
            cache: true,
            success: (result) => {
                //this.setState({data: result});
                //console.log(this.state.data);
				let currGraph = document.getElementById("graphRender");
				if(currGraph){currGraph.remove()};
				if(listBlocked){listBlocked = []};
				renderGraph(result);
            },
            error: (err) => {
                console.log(err);
            }
        });

	}

	getCourses(){
		// TODO: parse state variables and generate param object
		// only need is_guelph or is_ottawa AND subject code
		let apiParams = {
			is_ottawa: this.state.params.is_ottawa,
			is_guelph: this.state.params.is_guelph,
		};
		//console.log(JSON.stringify(apiParams, null, 2));

		
		for(const [key, value] of Object.entries(this.state.params)) {
			if (value != "" && key != "data") {
				apiParams[key] = value;
			}
		}

        $.ajax({
			beforeSend: function() { $('.loadingModal').attr('style', 'display: block'); },
			complete: function() { $('.loadingModal').attr('style', 'display: none'); },
            type: 'GET',
            url: 'https://131.104.49.113/api/courses',
            data: apiParams,
            cache: true,
            success: (result) => {
                this.setState({data: result});
                //console.log(this.state.data);
            },
            error: (err) => {
				this.setState({data: [
					{
						course_name: err.responseJSON.message
					}
				]});
                console.log(err);
            }
        });
    }

	changeSearch(event){
		// false is search, true is graphing
		const value = event.target.value;
		this.setState({
			whichSchool: '',
			schoolSubjects: ['Select a school first'],
			selectedSubject: '',
			params: {
				is_ottawa: false,
				is_guelph: false,
				is_major: false,
				is_offered_fall: false,
				is_offered_winter: false,
				is_offered_summer: false,
			},
			inputsHidden: value === 'search' ? false : true
		});
		$('.inputs').val('');
		//console.log(JSON.stringify(this.state, null, 2));
		
	}

	handleSchoolSelection(event){
		const name = event.target.name;
		const value = event.target.innerText;
		const schoolName = event.target.value;
		$('.inputs').val('');
		if(schoolName === 'is_ottawa'){
			this.setState({
				[name]: value,
				params:{
					is_ottawa: true,
					is_guelph: false,
					is_offered_fall: false,
					is_offered_summer: false,
					is_offered_winter: false
				}
			});

			let apiParams = {
				is_guelph: false,
				is_ottawa: true,
				is_major: false
			}

			$.ajax({
				type: 'GET',
				url: 'https://131.104.49.113/api/subjects',
				data: apiParams,
				cache: true,
				success: (result) => {
					let uniqueSubjects = [...new Set(result.map(item => {
						return {name: item.name, code: item.code}
					}))];
					let sortedArray = uniqueSubjects.sort((a,b) =>{
						const nameA = a.name.toUpperCase();
						const nameB = b.name.toUpperCase();
						if (nameA < nameB) {
							return -1;
						  }
						  if (nameA > nameB) {
							return 1;
						  }
						
						  // names must be equal
						  return 0;
					});
					this.setState({
						schoolSubjects: sortedArray,
						params: {
							is_guelph: false,
							is_ottawa: true,
						},
						selectedSubject: ''
					});
				},
				error: (err) => {
					this.setState({data: [
						{
							course_name: err.responseJSON
						}
					]});
					console.log(err);
				}
			});
		} else if(schoolName === 'is_guelph'){
			this.setState({
				[name]: value,
				params:{
					is_ottawa: true,
					is_guelph: false,
					is_offered_fall: false,
					is_offered_summer: false,
					is_offered_winter: false
				}
			});

			let apiParams = {
				is_guelph: true,
				is_ottawa: false,
				is_major: false
			}

			$.ajax({
				type: 'GET',
				url: 'https://131.104.49.113/api/subjects',
				data: apiParams,
				cache: true,
				success: (result) => {
					let uniqueSubjects = [...new Set(result.map(item => {
						return {name: item.name, code: item.code}
					}))];
					let sortedArray = uniqueSubjects.sort((a,b) =>{
						const nameA = a.name.toUpperCase();
						const nameB = b.name.toUpperCase();
						if (nameA < nameB) {
							return -1;
						  }
						  if (nameA > nameB) {
							return 1;
						  }
						
						  // names must be equal
						  return 0;
					});
					this.setState({
						schoolSubjects: sortedArray,
						params: {
							is_guelph: true,
							is_ottawa: false,
						},
						selectedSubject: ''
					});
				},
				error: (err) => {
					this.setState({data: [
						{
							course_name: err.responseJSON
						}
					]});
					console.log(err);
				}
			});
		} else if (schoolName === 'is_both'){
			this.setState({
				[name]: value,
				params:{
					is_ottawa: true,
					is_guelph: true,
					is_offered_fall: false,
					is_offered_summer: false,
					is_offered_winter: false
				}
			});

			let apiParams = {
				is_guelph: true,
				is_ottawa: true,
				is_major: false
			}
			$.ajax({
				type: 'GET',
				url: 'https://131.104.49.113/api/subjects',
				data: apiParams,
				cache: true,
				success: (result) => {
					let uniqueSubjects = [...new Set(result.map(item => {
						return {name: item.name, code: item.code}
					}))];
					let sortedArray = uniqueSubjects.sort((a,b) =>{
						const nameA = a.name.toUpperCase();
						const nameB = b.name.toUpperCase();
						if (nameA < nameB) {
							return -1;
						  }
						  if (nameA > nameB) {
							return 1;
						  }
						
						  // names must be equal
						  return 0;
					});
					this.setState({
						schoolSubjects: sortedArray,
						params: {
							is_guelph: true,
							is_ottawa: true,
						},
						selectedSubject: ''
					});
				},
				error: (err) => {
					this.setState({data: [
						{
							course_name: err.responseJSON
						}
					]});
					console.log(err);
				}
			});
		}		
	}

	render() {
	  return (
				<div id='searchDiv'>

					<div id='searchGraphButtonsDiv'>
						<button id='searchCoursesButton' value='search' className='searchGraphButtons btn btn-info' onClick={this.changeSearch}>Search Courses</button>
						<button id='graphCoursesButton' value='graph' className='searchGraphButtons btn btn-info' onClick={this.changeSearch}>Graph Courses</button>
					</div>
								
					<form className='searchInputs' id='searchForm'>

						<div id='schoolDropdown' className="dropdown">

							<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenu2" data-bs-toggle="dropdown" aria-expanded="false">
								Select School:
							</button>

							<ul className="dropdown-menu" aria-labelledby="dropdownMenu2">
								<li><button className="dropdown-item" name='whichSchool' value='is_guelph' type="button" onClick={this.handleSchoolSelection}>University of Guelph</button></li>
								<li><button className="dropdown-item" name='whichSchool' value='is_ottawa' type="button" onClick={this.handleSchoolSelection}>Univeristy of Ottawa</button></li>
								<li><button className="dropdown-item" name='whichSchool' value='is_both' type="button" onClick={this.handleSchoolSelection}>Search both Schools</button></li>
							</ul>

							<div className='dropdownOutput' id='schoolDropdownOutput'>
								{this.state.whichSchool}
							</div>
						</div>

						<div id='subjectsDropdown' className='dropdown'>

							<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenu3" data-bs-toggle="dropdown" aria-expanded="false">
								Select Subject: 
							</button>
							
							<ul className="dropdown-menu" aria-labelledby="dropdownMenu3">
								{this.state.schoolSubjects.map((item, key) =>{
									return(
										<li key={key}><button key={key} value={item.code} className="dropdown-item" type="button" onClick={this.handleSubjectSelection}>({item.code}) {item.name}</button></li>
									);									
								})}
							</ul>

							<div className='dropdownOutput' id='subjectDropdownOutput'>
								{this.state.selectedSubject}
							</div>	

						</div>

						{/*<input className='inputs' name='subject' type="text" placeholder='Subject (eg. CIS)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>*/}
						<input className='inputs' name='course_num' type='number' placeholder='Course Number (eg. 2750)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>
						<input className='inputs' name='name' type="text" placeholder='Course Name (eg. Intro to Computer Science)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>
						<input className='inputs' name='lectures' type='number' placeholder='Lecture (eg. 2)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>
						<input className='inputs' name='labs' type='number' placeholder='Lab (eg. 3)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>
						<input className='inputs' name='credits' type='number' placeholder='Course Weight (eg. 0.5)' onChange={this.handleInputChange} hidden={this.state.inputsHidden}></input>
						<input className='inputs' name='prereqs' type="text" placeholder='Enter the Prereqs' disabled hidden={this.state.inputsHidden}></input>

						<div className='radioDivs' hidden={this.state.inputsHidden}>
							<div>
								<input className="radioInput form-check-input" type="checkbox" name="is_offered_summer" id="inlineRadio1" value="option1" checked={this.state.params.is_offered_summer} onChange={this.handleInputChange} />
								<label className="radioInput form-check-label" htmlFor="inlineRadio1" hidden={this.state.inputsHidden}>Summer</label>
							</div>
							<div>
								<input className="radioInput form-check-input" type="checkbox" name="is_offered_fall" id="inlineRadio2" value="option2" checked={this.state.params.is_offered_fall} onChange={this.handleInputChange} />
								<label className="radioInput form-check-label" htmlFor="inlineRadio2" hidden={this.state.inputsHidden}>Fall</label>
							</div>
							<div>
								<input className="radioInput form-check-input" type="checkbox" name="is_offered_winter" id="inlineRadio3" value="option3" checked={this.state.params.is_offered_winter} onChange={this.handleInputChange} />
								<label className="radioInput form-check-label" htmlFor="inlineRadio3">Winter</label>
							</div>
						</div>
					</form>

					<button id='submitFormButton' name='searchSubmit' type='submit' form="form1" className='btn btn-primary' hidden={this.state.inputsHidden} onClick={this.submitSearch}>Submit</button>
					<button id='submitFormButton' name='graphSubmit' type='submit' form="form1" className='btn btn-primary' hidden={!this.state.inputsHidden} onClick={this.submitSearch}>Submit</button>
					<div className="loadingModal"></div>

					{this.state.inputsHidden === true ? <div id='graphLoc'></div> : <SearchOutput data = { this.state.data } /> }
					{/*<SearchOutput data = { this.state.data } /> */}
				
			</div>
	
	  );
	}
  }
  
  export default SearchFields;
