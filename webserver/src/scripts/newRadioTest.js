class NewRadio extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        name: "React"
      };

    }
    render() {
      return (
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
      );
    }
  }
//ReactDOM.render(<NewRadio /> , document.getElementById('newRadio'));

export default NewRadio;