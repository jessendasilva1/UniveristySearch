class CreditSlider extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        credit: 1.0
      };
    }

    render() {
      return (
        <div id='creditSlider'>
        	<label htmlFor="customRange3" className="form-label">Credit Weight: {this.state.credit}</label>
        	<input type="range" className="form-range" min="0" max="1" step="0.25" id="customRange3" onInput={this.state.credit = this.value}></input>
        </div>
      );
    }
  }
//ReactDOM.render(<CreditSlider /> , document.getElementById('creditSlider'));

export default CreditSlider;