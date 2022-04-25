class RadioTest extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: "React",
      selectedOption: '',
      serverResult: ''
    };
    this.onValueChange = this.onValueChange.bind(this);
    this.formSubmit = this.formSubmit.bind(this);
    this.courseSearch = this.courseSearch.bind(this);
  }

  courseSearch(){
    $.ajax({ 
      type: 'GET', 
      url: "https://131.104.49.113/" + this.state.selectedOption, 
      success: (result) =>{
          this.setState({ serverResult: result});
    }});
  }

  onValueChange(event) {
    this.setState({
      selectedOption: event.target.value
    });
  }

  formSubmit(event) {
    event.preventDefault();
    //console.log(this.state.selectedOption)
  }

  render() {
    return (
      <div id="searchButtons">
          <form onSubmit={this.formSubmit}>
          <div className="radio">
            <label>
              <input
                type="radio"
                value="guelphCourseSearch"
                id="guelphC"
                checked={this.state.selectedOption === "guelphCourseSearch"}
                onChange={this.onValueChange}
              />
              Guelph Course Search
            </label>
          </div>
          <div className="radio">
            <label>
              <input
                type="radio"
                value="guelphMajorSearch"
                id="guelphM"
                checked={this.state.selectedOption === "guelphMajorSearch"}
                onChange={this.onValueChange}
                data-toggle-value="guelphM"
              />
              Guelph Major Search
            </label>
          </div>
          <div className="radio">
            <label>
              <input
                type="radio"
                value="ottawaSubjectSearch"
                id="ottawaS"
                checked={this.state.selectedOption === "ottawaSubjectSearch"}
                onChange={this.onValueChange}
              />
              Ottawa Subject Search
            </label>
          </div>
          <button className='btn btn-primary' onClick={this.courseSearch}>Search</button>
          <div>
            Result : {this.state.serverResult}
          </div>
        </form>
        <div>
          <div className="form-check form-check-inline">
            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1"/>
            <label className="form-check-label" htmlFor="inlineRadio1">Summer</label>
          </div>
          <div className="form-check form-check-inline">
            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2"/>
            <label className="form-check-label" htmlFor="inlineRadio2">Winter</label>
          </div>
          <div className="form-check form-check-inline">
            <input className="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="option3"/>
            <label className="form-check-label" htmlFor="inlineRadio3">Fall</label>
          </div>
        </div>
      </div>
      
    );
  }
}

export default RadioTest;